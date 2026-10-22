"""Lossless, bounded source preparation using the conservative vi-spans-1 profile.

All coordinates are Unicode code points. Source prose is internal state only.
"""
import bisect
import copy
import hashlib
import json
import re
import time
import unicodedata

from .transport import encoded

MAX_INPUT = 1024 * 1024
PROFILE_VERSION = 'vi-spans-1'
MAX_INVENTORY = 4096
# Absolute per-phase work bound; it keeps pathological inputs far inside the deadline.
WORK_LIMIT = 32768
ID = re.compile(r'[A-Za-z][A-Za-z0-9_-]{0,63}\Z')
PROFILES = {'blog', 'technical', 'typography-only'}
KINDS = {'prose', 'heading', 'list', 'protected'}


def _bad():
    raise ValueError('invalid_input')


def _digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def _id(value):
    if not isinstance(value, str) or not ID.fullmatch(value): _bad()
    return value


def _safe(text, n, budget=None):
    if n in (0, len(text)): return True
    if 0x1F1E6 <= ord(text[n]) <= 0x1F1FF and 0x1F1E6 <= ord(text[n-1]) <= 0x1F1FF:
        preceding=0; j=n-1
        while j>=0 and 0x1F1E6 <= ord(text[j]) <= 0x1F1FF:
            if budget is not None: budget.consume()
            preceding+=1; j-=1
        if preceding%2: return False
    return not (text[n-1:n+1] == '\r\n' or unicodedata.category(text[n]).startswith('M') or 0xE0020 <= ord(text[n]) <= 0xE007F or text[n] in '\ufe0f\u200d' or text[n-1] == '\u200d' or 0x1F3FB <= ord(text[n]) <= 0x1F3FF)


def _span(value, text, budget=None):
    if not isinstance(value, dict): _bad()
    a, b = value.get('start'), value.get('end')
    if type(a) is not int or type(b) is not int or not 0 <= a < b <= len(text) or not _safe(text, a, budget) or not _safe(text, b, budget): _bad()
    return a, b


def _review(value):
    if value is None: return False, []
    if not isinstance(value, dict) or type(value.get('reviewed')) is not bool: _bad()
    pending = value.get('unresolved', [])
    if not isinstance(pending, list) or not all(isinstance(x, str) for x in pending): _bad()
    # Do not propagate host free prose through ordinary diagnostics.
    return value['reviewed'], ['host_context_unresolved'] * len(pending)


def _unique_spans(records, text, cap=None, candidates=False, budget=None):
    if not isinstance(records, list) or cap is not None and len(records) > cap: _bad()
    seen = set(); ranges = []
    for rec in records:
        if budget is not None: budget.consume()
        a, b = _span(rec, text, budget)
        ident = _id(rec.get('id'))
        if ident in seen: _bad()
        seen.add(ident); ranges.append((a, b))
        if candidates and not isinstance(rec.get('replacement'), str): _bad()
    if not candidates and any(x[1] > y[0] for x, y in zip(sorted(ranges), sorted(ranges)[1:])): _bad()
    return ranges


def _protected(records, text, budget=None):
    if not isinstance(records, list): _bad()
    ranges = sorted(_span(x, text, budget) for x in records)
    if any(x[1] > y[0] for x, y in zip(ranges, ranges[1:])): _bad()
    return ranges


def _trim(text, a, b):
    while a < b and text[a].isspace(): a += 1
    while b > a and text[b-1].isspace(): b -= 1
    return a, b


class _PreparationStopped(Exception):
    def __init__(self, reason): self.reason=reason


class _WorkBudget:
    """One invocation-local ceiling for token work, boundaries and inventory."""
    def __init__(self, remaining, deadline=None):
        self.remaining = remaining
        self.deadline = deadline

    def check(self):
        if self.deadline is not None and time.monotonic() >= self.deadline:
            raise _PreparationStopped('preparation_deadline')

    def consume(self, amount=1):
        self.check()
        if self.remaining < amount:
            raise _PreparationStopped('preparation_limit')
        self.remaining -= amount

    def take(self, amount=1):
        if self.remaining < amount: return False
        self.remaining -= amount
        return True


def _scan(text, opaque, overrides, deadline, budget, inventory=None):
    """Linear token dispatch, then source-bound punctuation decisions.

    Regex searches only partition whitespace or find simple digit/punctuation runs.
    Token recognizers are anchored and selected by markers; no recognizer retries
    an expensive suffix at every character position. All phases share one budget.
    """
    def expired(): return deadline is not None and time.monotonic() >= deadline
    # Each emitted span costs work and one inventory slot.
    def emit(): return budget.take() and (inventory is None or inventory.take())
    def unfinished(reason, spans=None, start=0, unresolved=None):
        spans=[] if spans is None else spans
        unresolved=[] if unresolved is None else unresolved
        a,b=_trim(text,start,len(text))
        if a<b: unresolved.append({'start':a,'end':b,'reason':reason})
        return spans,unresolved
    if expired(): return unfinished('preparation_deadline')
    lexical=list(opaque); tokens=[]; url_ambiguous=False
    # Reserve work for recognition and emitting a safe prefix before token exhaustion.
    token_allowance=max(1,budget.remaining//4); scan_end=len(text)
    # Token traversal is linear even for one 1MiB token without an email marker.
    for match in re.finditer(r'\S+',text):
        if expired(): return unfinished('preparation_deadline')
        if len(tokens)>=token_allowance:
            scan_end=match.start(); break
        if not budget.take(): return unfinished('preparation_limit')
        a,b=match.span(); word=match[0]; tokens.append((a,b,word))
        left=len(word)-len(word.lstrip('"“«(\u2018[')); core=word[left:]
        if '](' in core:
            destination=core.split('](',1)[1]
            if destination.startswith(('https://','http://')):
                left+=core.index('](')+2; core=destination
        if core.startswith(('https://','http://')):
            end=len(core.rstrip('.,!?;:)]}”»"'))
            lexical.append((a+left,a+left+end))
            url_ambiguous = url_ambiguous or '(' in core or (')' in core and '](' not in word)
        if '@' in word:
            email=word.strip('"“«(\u2018[.,!?;:)]}”»"')
            if email.count('@')==1:
                local,domain=email.split('@')
                labels=domain.split('.')
                if local and re.fullmatch(r'[\w.+-]+',local) and len(labels)>1 and all(label and re.fullmatch(r'[\w-]+',label) for label in labels) and re.fullmatch(r'[A-Za-z]{2,}',labels[-1]):
                    at=word.find(email); lexical.append((a+at,a+at+len(email)))
        # The optional separator tail consumes a digit run once; it never requires
        # a missing separator and retries that suffix from every digit position.
        if any(c in word for c in '.,/') and any(c.isdigit() for c in word):
            for numeric in re.finditer(r'\d+(?:[.,/]\d+)*',word):
                if expired(): return unfinished('preparation_deadline')
                if not budget.take(): return unfinished('preparation_limit')
                if any(c in numeric[0] for c in '.,/'):
                    lexical.append((a+numeric.start(),a+numeric.end()))
        for place in ('TP.HCM','TP.HN'):
            if core.startswith(place): lexical.append((a+left,a+left+len(place)))
        if core in ('v.v.','v.d.'):
            lexical.append((a+left,b-1)) # final dot remains an ambiguous endpoint
    titles={'TS.','ThS.','PGS.','GS.','TP.'}
    temporal={'Hôm','Ngày','Cuộc','Nay','Tôi','Bạn'}
    for index,(a,b,word) in enumerate(tokens):
        if expired(): return unfinished('preparation_deadline')
        if not budget.take(): return unfinished('preparation_limit')
        title=word.lstrip('"“«(‘[')
        if title in titles and index+1<len(tokens):
            continuation=tokens[index+1][2].rstrip('.,!?;:)]}”»"')
            if continuation and continuation[0].isupper() and continuation not in temporal:
                lexical.append((a+len(word)-len(title),b))
        if re.fullmatch(r'[A-ZĐ]\.',word):
            j=index; initials=0
            while j<len(tokens) and initials<4 and re.fullmatch(r'[A-ZĐ]\.',tokens[j][2]):
                if not budget.take(): return unfinished('preparation_limit')
                initials+=1; j+=1
            if j<len(tokens):
                continuation=tokens[j][2].rstrip('.,!?;:)]}”»"')
                if len(continuation)>1 and continuation[0].isupper() and continuation not in temporal and re.fullmatch(r'[^\W\d_]+',continuation):
                    end=tokens[j][0]+len(continuation)
                    if not any(a<y and end>x for x,y in opaque): lexical.append((a,end))
    ordinal=re.match(r'\s*\d+\.(?=\s)',text)
    if ordinal: lexical.append(ordinal.span())
    merged=[]
    for a,b in sorted(lexical):
        if merged and a<=merged[-1][1]: merged[-1]=(merged[-1][0],max(b,merged[-1][1]))
        else: merged.append((a,b))
    starts=[a for a,b in merged]
    def inside(n):
        index=bisect.bisect_right(starts,n)-1
        return index>=0 and n<merged[index][1]
    for n in overrides:
        if not _safe(text,n) or any(a<n<b for a,b in lexical): _bad()
    whole_reason=None
    if text.count('"')%2 or text.count('“')!=text.count('”') or text.count('«')!=text.count('»'): whole_reason='unmatched_delimiter'
    if url_ambiguous: whole_reason='ambiguous_url_closer'
    if any(m.start()<b-a for a,b in opaque for m in re.finditer(r'[.!?…](?:[\"”»’)]*)\s+[A-ZĐÀ-Ỹ]',text[a:min(len(text),b+64)])): whole_reason='protected_boundary'
    if whole_reason:
        a,b=_trim(text,0,len(text))
        return [(a,b,'unresolved')],[{'start':a,'end':b,'reason':whole_reason}]
    # Searches jump across uninterpreted text in C; one giant alphabetic token
    # never incurs a Python allocation/check for each character.
    import heapq
    events=heapq.merge((m.start() for m in re.finditer(r'[.!?…()]',text[:scan_end])),(n-1 for n in sorted(overrides) if n<=scan_end))
    endpoints=set(overrides); spans=[]; unresolved=[]; start=0; cursor=0; uncertain=[]; paren_depth=0
    punctuation=re.compile(r'[.!?…]+'); closers=re.compile(r'["”»’\])}]*'); whitespace=re.compile(r'\s*')
    for i in events:
        if i<cursor: continue
        if expired(): return unfinished('preparation_deadline',spans,start,unresolved)
        if not budget.take(): return unfinished('preparation_limit',spans,start,unresolved)
        if i+1 in endpoints:
            a,b=_trim(text,start,i+1)
            if a<b:
                if not emit(): return unfinished('preparation_limit',spans,start,unresolved)
                spans.append((a,b,'unresolved' if uncertain else 'exact'))
                if uncertain: unresolved.append({'start':a,'end':b,'reason':uncertain[0]})
            start=i+1; uncertain=[]; cursor=i+1; continue
        if inside(i): continue
        if text[i]=='(': paren_depth+=1; continue
        if text[i]==')': paren_depth=max(0,paren_depth-1); continue
        if text[i] not in '.!?…': continue
        # A boundary decision runs several anchored matches; charge it accordingly.
        if not budget.take(3): return unfinished('preparation_limit',spans,start,unresolved)
        end_punct=punctuation.match(text,i).end(); j=closers.match(text,end_punct).end(); k=whitespace.match(text,j).end()
        punct=text[i:end_punct]; reason=None
        inside_paren=paren_depth>0
        paren_depth=max(0,paren_depth-text[end_punct:j].count(')'))
        if not _safe(text,j,budget) or k<len(text) and (k==j or not _safe(text,k,budget)):
            reason='unsafe_boundary'
        # An override after a closing delimiter still owns this exact endpoint.
        if j in endpoints:
            a,b=_trim(text,start,j)
            if a<b:
                if not emit(): return unfinished('preparation_limit',spans,start,unresolved)
                spans.append((a,b,'unresolved' if uncertain else 'exact'))
                if uncertain: unresolved.append({'start':a,'end':b,'reason':uncertain[0]})
            start=j; uncertain=[]; cursor=j; continue
        tail=text[max(start,i-64):i+1]
        if re.search(r'\b(?:TS|ThS|PGS|GS|TP)\.$',tail) or tail.endswith(('v.v.','v.d.')) or re.search(r'\b[A-ZĐ]\.$',tail) and not inside(i-1): reason='ambiguous_abbreviation'
        if '…' in punct or '...' in punct:
            if k<len(text) and not text[k].islower(): reason='ambiguous_ellipsis'
            elif k<len(text):
                cursor=j; continue
        if k<len(text) and j>end_punct and text[k].islower() and any(c in text[end_punct:j] for c in '"”»’'):
            cursor=j; continue
        if '.' in punct and k<len(text) and (k==j or text[k].islower()): reason=reason or 'ambiguous_period'
        if inside_paren: reason=reason or 'ambiguous_parenthesis'
        if reason: uncertain.append(reason); cursor=j; continue
        a,b=_trim(text,start,j)
        if a<b:
            if not emit(): return unfinished('preparation_limit',spans,start,unresolved)
            status='unresolved' if uncertain else 'exact'; spans.append((a,b,status))
            if uncertain: unresolved.append({'start':a,'end':b,'reason':uncertain[0]})
        start=j; uncertain=[]; cursor=j
    a,b=_trim(text,start,len(text))
    if scan_end<len(text): uncertain.append('preparation_limit')
    if a<b:
        if not emit(): return unfinished('preparation_limit',spans,start,unresolved)
        status='unresolved' if uncertain else 'exact'; spans.append((a,b,status))
        if uncertain: unresolved.append({'start':a,'end':b,'reason':uncertain[0]})
    return spans,unresolved


def _raw_units(text, layout, annotations, budget):
    lines=list(re.finditer(r'[^\r\n]+(?:\r\n|\r|\n)?|(?:\r\n|\r|\n)',text))
    units=[]; i=0
    while i<len(lines):
        budget.consume()
        m=lines[i]; a,b=_trim(text,m.start(),m.end())
        if a==b: i+=1; continue
        line=text[a:b]; kind='prose'; typography=False; unsupported=False
        if layout=='markdown':
            if re.match(r'(`{3,}|~{3,})',line):
                fence=re.match(r'(`{3,}|~{3,})',line)[0]; j=i+1
                while j<len(lines) and not re.match(r'\s*'+re.escape(fence[0])+'{'+str(len(fence))+r',}\s*$',text[lines[j].start():lines[j].end()].strip()): j+=1
                b=_trim(text,a,lines[min(j,len(lines)-1)].end())[1]; kind='protected'; unsupported=j==len(lines); i=min(j,len(lines)-1)
            elif re.match(r'#{1,6}\s',line): kind='heading'
            elif re.match(r'(?:[-+*]|\d+[.)])\s',line): kind='list'
            elif line.startswith('|') or re.match(r'<[!/A-Za-z]',line):
                typography=True; kind='heading'
                if line.startswith('|'):
                    j=i+1
                    while j<len(lines) and text[lines[j].start():lines[j].end()].lstrip().startswith('|'): j+=1
                    b=_trim(text,a,lines[j-1].end())[1]; i=j-1
            if kind in ('prose','list') and not typography:
                j=i+1
                while j<len(lines):
                    na,nb=_trim(text,lines[j].start(),lines[j].end()); nxt=text[na:nb]
                    if not nxt or re.match(r'(?:#{1,6}\s|[-+*]\s|\d+[.)]\s|`{3,}|~{3,}|\||<[!/A-Za-z])',nxt): break
                    if kind=='list' and not text[lines[j].start():lines[j].end()].startswith((' ','\t')): break
                    b=nb; j+=1
                i=j-1
        units.append({'start':a,'end':b,'kind':kind,'typography':typography,'unsupported':unsupported or bool(typography and not line.startswith('|'))}); i+=1
        if len(units)>=MAX_INVENTORY-1 and i<len(lines):
            a,b=_trim(text,lines[i].start(),len(text))
            if a<b: units.append({'start':a,'end':b,'kind':'heading','typography':True,'unprocessed':True})
            break
    parents=[x for x in annotations if x.get('paragraph') is True]
    for ann in parents:
        budget.check()
        a,b=ann['start'],ann['end']
        overlapping=[]
        for x in units:
            budget.consume()
            if x['start']<b and x['end']>a: overlapping.append(x)
        if any(x['kind']=='protected' for x in overlapping) and ann.get('kind')!='protected': _bad()
        if any(x['start']<a or x['end']>b for x in overlapping):
            # Explicit parents may split scanner prose, but never code blocks.
            for x in overlapping:
                if x['kind']=='protected': _bad()
        replacement=[]
        for x in units:
            budget.consume()
            if x not in overlapping: replacement.append(x); continue
            if x['start']<a: replacement.append(dict(x,end=a))
            if x['end']>b: replacement.append(dict(x,start=b))
        replacement.append({'start':a,'end':b,'kind':ann.get('kind','prose'),'typography':False})
        units=sorted(replacement,key=lambda x:x['start'])
        if len(units)>MAX_INVENTORY: raise _PreparationStopped('preparation_limit')
    return units


def prepare_document(document, deadline=None):
    """Validate and inventory a raw v2 source or bounded legacy sections.

    The return is internal and may contain original prose. Public callers must project
    only IDs, digests and source-bound diagnostics from this structure.
    """
    try:
        return _prepare(document,deadline)
    except _PreparationStopped as error:
        return _limited(document,error.reason)
    except (KeyError,TypeError,AttributeError,UnicodeError,OverflowError,RecursionError):
        raise ValueError('invalid_input') from None


def _prepare(doc,deadline):
    if not isinstance(doc,dict) or len(encoded(doc))>MAX_INPUT: _bad()
    raw=doc.get('schema_version')==2
    if 'schema_version' in doc and (type(doc['schema_version']) is not int or doc['schema_version'] not in (1,2)): _bad()
    annotations=[]; source=''; sourceid='legacy'; sections=[]; partition=[]
    budget=_WorkBudget(WORK_LIMIT,deadline)
    budget.check()
    for field in ('annotations','candidates','context_links','context_reviews','boundary_overrides'):
        records=doc.get(field,[])
        if not isinstance(records,list): _bad()
        budget.consume(len(records))
    review=doc.get('context_review')
    if isinstance(review,dict) and isinstance(review.get('unresolved'),list):budget.consume(len(review['unresolved']))
    reviewed,pending=_review(review)
    if raw:
        if 'sections' in doc: _bad()
        src=doc.get('source'); defaults=doc.get('defaults',{})
        if not isinstance(src,dict) or not isinstance(defaults,dict): _bad()
        sourceid=_id(src.get('id')); source=src.get('text'); layout=src.get('layout')
        if not isinstance(source,str) or layout not in ('paragraph-lines','markdown') or defaults.get('profile') not in PROFILES: _bad()
        for field in ('register','audience','purpose'):
            if field in defaults and not isinstance(defaults[field],str): _bad()
        annotations=doc.get('annotations',[])
        if not isinstance(annotations,list): _bad()
        for ann in annotations:
            budget.consume()
            _span(ann,source,budget)
            if ann.get('kind','prose') not in KINDS or ann.get('profile',defaults['profile']) not in PROFILES: _bad()
            for field in ('paragraph','protected'):
                if field in ann and type(ann[field]) is not bool: _bad()
        ordered=sorted(annotations,key=lambda x:(x['start'],x['end']))
        for i,x in enumerate(ordered):
            for y in ordered[i+1:]:
                budget.consume()
                if y['start']>=x['end']: break
                def nested_protection(parent,child):
                    return (parent.get('paragraph') is True and child.get('protected') is True
                            and parent['start']<=child['start']<child['end']<=parent['end']
                            and not any(k in child for k in ('kind','profile','paragraph')))
                nested=nested_protection(x,y) or nested_protection(y,x)
                if not nested: _bad()
        units=_raw_units(source,layout,annotations,budget)
        for unit in units:
            budget.consume()
            a,b=unit['start'],unit['end']; s={k:v for k,v in defaults.items() if k in ('profile','register','audience','purpose')}
            s.update(id='p_'+_digest([sourceid,a,b])[:24],text=source[a:b],kind=unit['kind'],source_start=a,source_end=b,protected_spans=[],targets=[],candidates=[])
            if unit['typography']: s['profile']='typography-only'
            if unit.get('unprocessed'): s['_unprocessed']=True
            if unit.get('unsupported'): s['_unsupported']=True
            for ann in annotations:
                budget.consume()
                x,y=ann['start'],ann['end']
                if x<b and y>a:
                    if ('kind' in ann or 'profile' in ann) and (x!=a or y!=b): _bad()
                    for field in ('kind','profile'):
                        if field in ann:
                            if field=='kind' and unit['kind']=='protected' and ann[field]!='protected': _bad()
                            s[field]=ann[field]
                    if ann.get('protected'): s['protected_spans'].append({'start':max(x,a)-a,'end':min(y,b)-a})
            if layout=='markdown' and s['kind']!='protected':
                runs=list(re.finditer(r'`+',s['text'])); index=0
                while index<len(runs):
                    budget.consume()
                    opening=runs[index]; slash=opening.start()-1
                    while slash>=0 and s['text'][slash]=='\\':
                        budget.consume(); slash-=1
                    open_start=opening.start(); width=len(opening[0])
                    if (opening.start()-1-slash)%2:
                        open_start+=1; width-=1
                        if not width:
                            index+=1; continue
                    closing=index+1
                    while closing<len(runs) and len(runs[closing][0])!=width:
                        budget.consume(); closing+=1
                    end=runs[closing].end() if closing<len(runs) else len(s['text'])
                    s['protected_spans'].append({'start':open_start,'end':end})
                    if closing==len(runs): s['_unsupported']=True
                    index=closing+1
            # Union nested/adjacent opaque fields, retaining exact original offsets.
            merged=[]
            for p in sorted(s['protected_spans'],key=lambda x:x['start']):
                if merged and p['start']<=merged[-1]['end']: merged[-1]['end']=max(p['end'],merged[-1]['end'])
                else: merged.append(dict(p))
            s['protected_spans']=merged
            if s['kind']=='list':
                line_start=max(source.rfind('\n',0,a),source.rfind('\r',0,a))+1
                s['_indent']=len(source[line_start:a].expandtabs(4))
            sections.append(s)
        candidates=doc.get('candidates',[]); _unique_spans(candidates,source,candidates=True,budget=budget)
        for c in candidates:
            budget.check()
            budget.consume(len(sections))
            owners=[s for s in sections if s['source_start']<=c['start']<c['end']<=s['source_end']]
            if len(owners)!=1: _bad()
            s=owners[0]; s['candidates'].append(dict(c,start=c['start']-s['source_start'],end=c['end']-s['source_start']))
    else:
        if 'source' in doc: _bad()
        supplied=doc.get('sections')
        if not isinstance(supplied,list) or not 1<=len(supplied)<=32: _bad()
        seen=set(); cursor=0
        for supplied_section in supplied:
            if not isinstance(supplied_section,dict): _bad()
            for field in ('targets','candidates','protected_spans','context'):
                records=supplied_section.get(field,[])
                if not isinstance(records,list): _bad()
                budget.consume(len(records))
            s=copy.deepcopy(supplied_section); ident=_id(s.get('id'))
            if ident in seen: _bad()
            seen.add(ident)
            if s.get('profile') not in PROFILES or s.get('kind') not in KINDS or not isinstance(s.get('text'),str) or not s['text'].strip(): _bad()
            for field in ('register','audience','purpose'):
                if field in s and not isinstance(s[field],str): _bad()
            _unique_spans(s.get('targets',[]),s['text'],16,budget=budget)
            _unique_spans(s.get('candidates',[]),s['text'],8,True,budget)
            s['source_start']=cursor; s['source_end']=cursor+len(s['text']); cursor=s['source_end']+1
            sections.append(s)
        source='\n'.join(s['text'] for s in sections)
    overrides=doc.get('boundary_overrides',[])
    if not isinstance(overrides,list) or any(type(n) is not int or not 0<n<=len(source) or not _safe(source,n,budget) for n in overrides) or len(set(overrides))!=len(overrides): _bad()
    if any(not any(s['source_start']<n<=s['source_end'] for s in sections) for n in overrides): _bad()
    source_digest=hashlib.sha256(source.encode()).hexdigest()
    unresolved=[]; cursor=0
    budget.consume(len(sections))
    for s in sections:
        budget.consume()
        a,b=s['source_start'],s['source_end']
        if cursor<a: partition.append({'start':cursor,'end':a,'kind':'separator'})
        partition.append({'start':a,'end':b,'kind':s['kind'],'section':s['id']}); cursor=b
        opaque=_protected(s.get('protected_spans',[]),s['text'],budget)
        if s['kind']=='protected': opaque=[(0,len(s['text']))]
        s['editable']=bool(s['text'].strip()) and not (s.get('_unprocessed') or s['kind']=='protected' or opaque==[(0,len(s['text']))])
        for c in s.get('candidates',[]):
            if s['kind']=='protected' or any(c['start']<y and c['end']>x for x,y in opaque): _bad()
        local=[n-a for n in overrides if a<n<=b]
        if local and s['kind'] not in ('prose','list'): _bad()
        s['_scan_opaque']=opaque; s['_scan_overrides']=local
        s['context_reviewed'],s['context_unresolved']=_review(s.get('context_review')) if 'context_review' in s else (reviewed,list(pending))
        s['contexts']=[]
        context=s.get('context',[])
        if not isinstance(context,list) or not all(isinstance(x,str) for x in context): _bad()
        for i,text in enumerate(context): s['contexts'].append({'id':'external_'+_digest([s['id'],i,text])[:24],'text':text,'role':'supplied','allowed':True})
    if cursor<len(source): partition.append({'start':cursor,'end':len(source),'kind':'separator'})
    # Complete neighboring parents and nearest heading ancestry. Never summarize them.
    headings=[]; list_stack=[]; list_leadin=None
    for i,s in enumerate(sections):
        budget.consume()
        members=[]
        if s['kind']=='list':
            indent=s.get('_indent',0)
            if not list_stack: list_leadin=sections[i-1] if i and sections[i-1]['kind']=='prose' else None
            list_stack=[m for m in list_stack if m.get('_indent',0)<indent]
            members.extend((m,'list_ancestry') for m in list_stack)
            if list_leadin is not None: members.append((list_leadin,'list_leadin'))
            list_stack.append(s)
        else: list_stack=[]; list_leadin=None
        for j,role in ((i-1,'previous'),(i+1,'next')):
            if 0<=j<len(sections): members.append((sections[j],role))
        if s['kind']=='heading':
            level=len(re.match(r'#+',s['text'])[0]) if re.match(r'#+',s['text']) else 1
            headings=[(h,l) for h,l in headings if l<level]; headings.append((s,level))
        else: members.extend((h,'heading_ancestry') for h,_ in headings)
        for member,role in members:
            budget.consume()
            if member['id']==s['id'] or any(x['id']==member['id'] for x in s['contexts']): continue
            if member.get('_unprocessed'):
                s['context_unresolved'].append('context_unprocessed'); continue
            s['contexts'].append({'id':member['id'],'text':member['text'],'role':role,'allowed':True,'source_start':member['source_start'],'source_end':member['source_end'],'protected_spans':member.get('protected_spans',[]),'kind':member['kind'],'editable':member['editable']})
    links=doc.get('context_links',[])
    if not isinstance(links,list): _bad()
    for link in links:
        budget.consume(len(sections))
        if not isinstance(link,dict): _bad()
        pa,pb=link.get('parent_start'),link.get('parent_end')
        if type(pa) is not int or type(pb) is not int or not 0<=pa<pb<=len(source): _bad()
        owners=[s for s in sections if (s['source_start'],s['source_end'])==(pa,pb)]
        has_span='source_start' in link or 'source_end' in link
        if has_span == ('text' in link or 'id' in link): _bad()
        role=link.get('role','linked'); allowed=link.get('allowed',True)
        if not isinstance(role,str) or type(allowed) is not bool: _bad()
        member=None
        if has_span:
            x,y=link.get('source_start'),link.get('source_end')
            if type(x) is not int or type(y) is not int or not 0<=x<y<=len(source): _bad()
            matches=[s for s in sections if (s['source_start'],s['source_end'])==(x,y)]
            if matches and not matches[0].get('_unprocessed'):
                m=matches[0]; member={'id':m['id'],'text':m['text'],'role':role,'allowed':allowed,'source_start':x,'source_end':y,'protected_spans':m.get('protected_spans',[]),'kind':m['kind'],'editable':m['editable']}
        else:
            ident=_id(link.get('id')); text=link.get('text')
            if not isinstance(text,str) or not text.strip(): _bad()
            member={'id':ident,'text':text,'role':role,'allowed':allowed}
        if not owners:
            for s in sections: s['context_unresolved'].append('context_parent_unresolved')
        else:
            s=owners[0]
            if member is None: s['context_unresolved'].append('context_link_unresolved')
            else:
                duplicate=next((m for m in s['contexts'] if m['id']==member['id']),None)
                if duplicate:
                    if duplicate['text']!=member['text']: _bad()
                    duplicate['allowed']=duplicate['allowed'] and allowed
                else: s['contexts'].append(member)
                if not allowed: s['context_unresolved'].append('context_permission_denied')
    reviews=doc.get('context_reviews',[])
    if not isinstance(reviews,list): _bad()
    review_seen=set()
    for review in reviews:
        budget.consume(len(sections))
        a,b=_span(review,source)
        if (a,b) in review_seen: _bad()
        review_seen.add((a,b)); owners=[s for s in sections if (s['source_start'],s['source_end'])==(a,b)]
        if len(owners)!=1: _bad()
        r,p=_review(review); owners[0]['context_reviewed']=r
        owners[0]['context_unresolved']=[x for x in owners[0]['context_unresolved'] if x!='host_context_unresolved']+p
    for s in sections:
        s['contexts'].sort(key=lambda x:(x.get('source_start',len(source)),x['id']))
    # No classification work follows scanning: scan exhaustion cannot erase a safe prefix.
    scan_budget=_WorkBudget(WORK_LIMIT,deadline)
    inventory=_WorkBudget(max(0,MAX_INVENTORY-len(sections)))
    for s in sections:
        a=s['source_start']
        if s.get('_unprocessed') or s.get('_unsupported'):
            spans=[]; problems=[{'start':0,'end':len(s['text']),'reason':'preparation_limit' if s.get('_unprocessed') else 'unsupported_structure'}]
        elif s['kind'] in ('prose','list'):
            try:
                spans,problems=_scan(s['text'],s['_scan_opaque'],s['_scan_overrides'],deadline,scan_budget,inventory)
            except _PreparationStopped as error:
                spans=[]; problems=[{'start':0,'end':len(s['text']),'reason':error.reason}]
        else: spans=[]; problems=[]
        aliases={(t['start'],t['end']):t['id'] for t in s.get('targets',[])}
        s['sentences']=[{'id':'s_'+_digest([sourceid,source_digest,s['kind'],a+x,a+y,PROFILE_VERSION,overrides])[:24],'aliases':([aliases[(x,y)]] if (x,y) in aliases else []),'start':x,'end':y,'boundary_status':status} for x,y,status in spans]
        for p in problems: unresolved.append(dict(p,start=a+p['start'],end=a+p['end'],section=s['id']))
    return {'sections':sections,'source_scope':'source_document' if raw else 'provided_sections','source_digest':hashlib.sha256(source.encode()).hexdigest(),'source_accounted':True,'segmentation_complete':not unresolved,'unresolved':unresolved,'partition':partition,'source':source,'segmentation_profile':PROFILE_VERSION}


def _limited(doc,reason):
    """Unknown metadata is never bypassed to send a partially classified source."""
    if not isinstance(doc,dict): _bad()
    raw=doc.get('schema_version')==2
    if raw:
        source=doc.get('source',{}).get('text')
        if not isinstance(source,str): _bad()
    else:
        sections=doc.get('sections',[])
        if not isinstance(sections,list) or not all(isinstance(s,dict) and isinstance(s.get('text'),str) for s in sections): _bad()
        source='\n'.join(s['text'] for s in sections)
    return {'sections':[],'source':source,'source_digest':hashlib.sha256(source.encode()).hexdigest(),
            'source_scope':'source_document' if raw else 'provided_sections','source_accounted':True,
            'segmentation_complete':False,'unresolved':[{'start':0,'end':len(source),'reason':reason}],
            'partition':[{'start':0,'end':len(source),'kind':'unprocessed'}] if source else [],
            'segmentation_profile':PROFILE_VERSION}
