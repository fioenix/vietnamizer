"""Compact source-bound work accounting. No edit policy or prose generation."""
import hashlib
from .transport import encoded

ROLES = {'violation': 'violation', 'interpretation': 'interpretation',
         'evidence': 'evidence', 'degree': 'degree'}
# A missing group reports its most specific reason; budget exhaustion is the least specific.
PRECEDENCE = ['invalid_response', 'deadline_exceeded', 'cancelled', 'authentication_failed', 'service_failed',
              'permission_blocked', 'context_unresolved', 'context_too_large', 'budget_exhausted', 'incomplete']


def fingerprint(value):
    return hashlib.sha256(encoded(value)).hexdigest()


class Ledger:
    """Shared subject lists and sparse outcomes avoid a materialized check product."""
    def __init__(self, prepared, registry, model, only_pattern=None, selected=False):
        self.sections = prepared['sections']
        self.groups = []
        self.coverage = []
        self.outcomes = {}
        self.candidate_reviews = []
        self.mechanical = 0
        binding = {'source': prepared['source_digest'], 'input':prepared.get('binding_digest'), 'registry': fingerprint(registry),
                   'model': model, 'profile_version': prepared['segmentation_profile'], 'config': '2',
                   'scope': only_pattern, 'selected': selected}
        self.manifest_digest = fingerprint(binding)
        mechanical_needed = False
        for section in self.sections:
            subjects = section['sentences']
            structural = not selected and not subjects and section['kind']=='heading'
            if structural:
                subjects=[{'id':'unit','start':0,'end':len(section['text'])}]
            for p in registry:
                pid = p['id']
                if only_pattern and pid != only_pattern:
                    continue
                for q in p['questions']:
                    if q['key'] not in ROLES:
                        raise ValueError('registry_invalid')
                entry = {'section': section['id'], 'pattern': pid, 'status': 'pending'}
                self.coverage.append(entry)
                prefix = pid[0]
                reason = None
                if section['kind'] == 'protected' or not section.get('editable', True):
                    reason = 'protected_region'
                elif section['profile'] == 'typography-only' and prefix != 'T':
                    reason = 'genre_gate'
                elif prefix == 'B' and section['profile'] != 'blog' or prefix == 'K' and section['profile'] != 'technical':
                    reason = 'inactive_profile'
                if reason:
                    entry.update(status='excluded', reason=reason)
                    continue
                if p['mode'] == 'mechanical':
                    entry.update(status='mechanically_checked', scope='document')
                    mechanical_needed = True
                    continue
                target_scope = p['scope'] == 'target'
                group_subjects = subjects if target_scope else [None]
                if not group_subjects:
                    entry.update(status='excluded', reason='no_exact_editable_targets')
                    continue
                self.groups.append({'section': section['id'], 'pattern': pid,
                                    'scope': ('unit' if structural else 'sentence') if target_scope else 'paragraph',
                                    'subjects': group_subjects, 'recipes': p['questions'],
                                    'pattern_data': p, 'entry': entry, 'reason': None})
            for c in section.get('candidates', []):
                review = {'section': section['id'], 'candidate': c['id'], 'status': 'pending'}
                self.candidate_reviews.append(review)
                self.groups.append({'section': section['id'], 'pattern': 'edit_'+c['id'],
                                    'scope': 'candidate', 'subjects': [c],
                                    'recipes': [{'key': x} for x in ('meaning','new_claim','improvement','voice')],
                                    'entry': review, 'reason': None})
        self.mechanical = int(mechanical_needed)
        # Priority tiers 1-3 per (group, subject); every other check is tier 4. Reasons per check
        # record why a planned check failed; unplanned checks take their group's reason.
        self.tier = {}
        self.key_reason = {}
        self.by_section={}
        for i,g in enumerate(self.groups):
            self.by_section.setdefault(g['section'],[]).append((i,g))

    def checks(self, section_id):
        groups = self.by_section.get(section_id,[])
        for i,g in groups:
            if g['scope']=='paragraph':
                for r in g['recipes']:
                    yield (i,0,r['key'])
        # Subject lists are shared, not duplicated per pattern.
        sentence_groups = [(i,g) for i,g in groups if g['scope'] in ('sentence','unit')]
        count = len(sentence_groups[0][1]['subjects']) if sentence_groups else 0
        for n in range(count):
            for i,g in sentence_groups:
                for r in g['recipes']:
                    yield (i,n,r['key'])
        for i,g in groups:
            if g['scope']=='candidate':
                for r in g['recipes']:
                    yield (i,0,r['key'])

    def assign_tiers(self, focus, signals, editable, deadline=None):
        """1 candidate review, 2 host focus span, 3 local signal in the subject, 4 everything else.

        Past the deadline the remaining checks stay tier 4; planning then stops on the same deadline.
        """
        import re, time
        sections = {s['id']: s for s in self.sections}
        compiled = {pid: [re.compile(x, re.M) for x in xs] for pid, xs in signals.items()}
        hits = {}
        for i, g in enumerate(self.groups):
            if g['scope'] == 'candidate':
                self.tier[(i, 0)] = 1
                continue
            if deadline is not None and time.monotonic() >= deadline:
                continue
            section = sections[g['section']]; base = section.get('source_start', 0); pid = g['pattern']
            if pid in compiled and (section['id'], pid) not in hits:
                text = editable(section)
                hits[(section['id'], pid)] = [m.span() for c in compiled[pid] for m in c.finditer(text)]
            found = hits.get((section['id'], pid), [])
            for n, subject in enumerate(g['subjects']):
                a, b = (0, len(section['text'])) if subject is None else (subject['start'], subject['end'])
                if any(x < base + b and y > base + a and (names is None or pid in names) for x, y, names in focus):
                    self.tier[(i, n)] = 2
                elif any(x < b and y > a for x, y in found):
                    self.tier[(i, n)] = 3

    def tier_of(self, i, n):
        return self.tier.get((i, n), 4)

    def required(self, g):
        return len(g['subjects'])*len(g['recipes'])

    def credit(self, key, answer, receipt):
        i,n,r = key
        g = self.groups[i]
        if not 0 <= n < len(g['subjects']) or r not in {q['key'] for q in g['recipes']}:
            raise ValueError('invalid_check')
        if key in self.outcomes:
            raise ValueError('duplicate_check')
        self.outcomes[key] = {'answer': answer, 'receipt': receipt}

    def block(self, section_id, reason):
        for g in self.groups:
            if g['section']==section_id and g['reason'] is None:
                g['reason'] = reason

    def finalize(self, prepared, judgments, full_scope=True):
        validated_per = {}
        sentence_counts = {}
        context_bad = set()
        validated_keys={}
        for key,outcome in self.outcomes.items():
            i,n,r = key
            g = self.groups[i]
            validated_per[i] = validated_per.get(i,0)+1
            validated_keys.setdefault(i,[]).append([n,r])
            if g['scope']=='sentence':
                sk=(g['section'],g['subjects'][n]['id'])
                sentence_counts[sk]=sentence_counts.get(sk,0)+1
            answer=outcome['answer']
            role=ROLES.get(r,'candidate')
            if answer['type']=='choice' and (answer.get('choice')=='insufficient' or role=='evidence' and answer.get('choice')!='sufficient'):
                context_bad.add((g['section'],g['scope'],n,g['pattern']))
        for i,g in enumerate(self.groups):
            for n in range(len(g['subjects'])):
                if any(q['key']=='evidence' for q in g['recipes']) and (i,n,'evidence') not in self.outcomes:
                    context_bad.add((g['section'],g['scope'],n,g['pattern']))
            if g['reason'] in ('context_too_large','context_unresolved','permission_blocked') or g.get('oversized'):
                context_bad.add((g['section'],g['scope'],-1,g['pattern']))
        missing=[]
        for i,g in enumerate(self.groups):
            total=self.required(g);done=validated_per.get(i,0)
            if done==total:
                status='jev_evaluated'
            else:
                by_reason={};by_tier={}
                for n in range(len(g['subjects'])):
                    tier=str(self.tier_of(i,n))
                    for q in g['recipes']:
                        key=(i,n,q['key'])
                        if key in self.outcomes:continue
                        why=self.key_reason.get(key) or g['reason'] or 'incomplete'
                        by_reason[why]=by_reason.get(why,0)+1;by_tier[tier]=by_tier.get(tier,0)+1
                status=min(by_reason,key=lambda r:(PRECEDENCE.index(r) if r in PRECEDENCE else len(PRECEDENCE)-2,r))
                missing.append({'group':i,'section':g['section'],'pattern':g['pattern'],
                                'scope':g['scope'],'subject_range':[0,len(g['subjects'])],
                                'recipe_keys':[q['key'] for q in g['recipes']],
                                'validated_keys':validated_keys.get(i,[]),
                                'missing':total-done,'reason':status,
                                'missing_by_reason':by_reason,'missing_by_tier':by_tier})
            g['entry'].update(status=status,scheduled=total,validated=done)
        statuses={(e['section'],e.get('pattern','edit_'+e.get('candidate',''))):e['status']
                  for e in self.coverage+self.candidate_reviews}
        for j in judgments:
            j['coverage_status']=statuses[(j['section'],j['coverage_key'])]
        by_key={key:outcome['answer'] for key,outcome in self.outcomes.items()}
        for j in judgments:
            if j['answer']['type']=='score':
                i,n,_=j['_key']
                a=by_key.get((i,n,'evidence'))
                j['disposition']=('context_supported' if a and a['choice']=='sufficient' else
                                  'ignore_insufficient_context' if a and a['choice']=='insufficient' else 'ignore_unresolved_context')
            j.pop('_key',None)
        sentences=[]
        for s in self.sections:
            relevant=[g for _,g in self.by_section.get(s['id'],[]) if g['scope']=='sentence']
            per=sum(len(g['recipes']) for g in relevant)
            for n,t in enumerate(s['sentences']):
                done=sentence_counts.get((s['id'],t['id']),0)
                context_ok=s.get('context_reviewed',False) and not s.get('context_unresolved')
                context_ok=context_ok and not any(x[0]==s['id'] and (x[1]!='sentence' or x[2] in (-1,n)) for x in context_bad)
                sentences.append({'section':s['id'],'id':t['id'],'start':t['start'],'end':t['end'],
                                  'source_start':s['source_start']+t['start'],'source_end':s['source_start']+t['end'],
                                  'aliases':t.get('aliases',[]),'required':per,'validated':done,'answers_complete':done==per,
                                  'context_complete':bool(context_ok),
                                  'excluded':per==0})
        remote_required=sum(self.required(g) for g in self.groups)
        validated=len(self.outcomes)
        context_complete=all(s.get('context_reviewed',False) and not s.get('context_unresolved')
                             for s in self.sections if s.get('editable',True)) and not context_bad and bool(self.sections) and prepared['segmentation_complete']
        answer_complete=not missing
        scope_complete=bool(answer_complete and context_complete and prepared['segmentation_complete'] and prepared['source_accounted'])
        all_excluded=not remote_required and not self.mechanical and prepared['segmentation_complete'] and bool(self.sections)
        return {'manifest_digest':self.manifest_digest,'counts':{
            'sentences':len(sentences),'provisional':not prepared['segmentation_complete'],'required':remote_required+self.mechanical,
            'validated':validated,'mechanical':self.mechanical,'uncompleted':remote_required-validated},
            'missing':missing,'sentences':sentences,'source_accounted':prepared['source_accounted'],
            'segmentation_complete':prepared['segmentation_complete'],
            'answers_complete':answer_complete,'context_complete':bool(context_complete),
            'scope_complete':scope_complete and not all_excluded,
            'evaluation_complete':scope_complete and full_scope and not all_excluded,
            'all_excluded':all_excluded,'unresolved':prepared['unresolved'],
            'units':[{'id':s['id'],'start':s['source_start'],'end':s['source_end']} for s in self.sections],
            'work_groups':[{'group':i,'section':g['section'],'pattern':g['pattern'],'scope':g['scope'],
                            'subject_count':len(g['subjects']),'recipe_keys':[q['key'] for q in g['recipes']],
                            'candidate':g['subjects'][0]['id'] if g['scope']=='candidate' else None} for i,g in enumerate(self.groups)],
            'diagnostic_targets':[dict(section=s['id'],id=t['id'],start=t['start'],end=t['end'],disposition='not_checked_in_full_scope')
                                  for s in self.sections for t in s.get('targets',[])
                                  if not any((t['start'],t['end'])==(x['start'],x['end']) for x in s['sentences'])],
            'excluded_sentences':[dict(t,section=s['id'],reason='protected_region') for s in self.sections for t in s.get('excluded_sentences',[])]}


def compact_report(report, force=False):
    """Lossless templates for large ledgers; small v2 reports retain flat lists."""
    for field in ('coverage','work_groups','missing'):
        records=report.get(field)
        if not isinstance(records,list) or not records or not force and len(records)<=8192:
            continue
        varying=[key for key in ('group','section') if any(key in r for r in records)]
        templates=[]; indices={}; rows=[]; sections=[]; section_index={}
        for record in records:
            shared={k:v for k,v in record.items() if k not in varying}
            binding=encoded(shared)
            if binding not in indices:
                indices[binding]=len(templates); templates.append(shared)
            values=[]
            for key in varying:
                value=record[key]
                if key=='section':
                    if value not in section_index:
                        section_index[value]=len(sections); sections.append(value)
                    value=section_index[value]
                values.append(value)
            rows.append([indices[binding],*values])
        report[field]={'encoding':'templates-v1','varying':varying,'sections':sections,
                       'templates':templates,'rows':rows}
        report['ledger_encoding']='templates-v1'
    return report


def expand_records(records):
    """Expand trusted local templates-v1 output for consumers and reconciliation."""
    import copy
    if isinstance(records,list): return copy.deepcopy(records)
    if records.get('encoding')!='templates-v1': raise ValueError('invalid_ledger_encoding')
    expanded=[]
    for index,*values in records['rows']:
        record=copy.deepcopy(records['templates'][index])
        for key,value in zip(records['varying'],values):
            record[key]=records['sections'][value] if key=='section' else value
        expanded.append(record)
    return expanded
