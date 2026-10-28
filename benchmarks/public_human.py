"""Offline, provenance-bound analysis for the public human cohort; no model calls."""
from pathlib import Path
import argparse
import collections
import csv
import hashlib
import json
import random

from benchmarks import simple_forms as simple

BINDING_SCHEMA = 'public-human-analysis-v1'
EXPORT_SCHEMA = 'public-human-export-v1'
ARMS = ('bare', 'ordinary', 'vietnamizer', 'vietnamizer_jev')
QUESTIONS = simple.QUESTIONS
CATEGORIES = {'preservation': ['preserved','changed','uncertain','missing'],
              'readability': ['better','equivalent','worse','uncertain','missing']}
COMPARISONS = [('vietnamizer','ordinary'), ('vietnamizer','bare'),
               ('vietnamizer_jev','vietnamizer')]


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',',':')).encode()


def digest(value):
    return hashlib.sha256(value if isinstance(value, bytes) else encoded(value)).hexdigest()


def read(path):
    return json.loads(Path(path).read_text())


def save(path, value):
    Path(path).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def validate_binding(b):
    if b.get('schema') != BINDING_SCHEMA or b.get('arms') != list(ARMS):
        raise ValueError('Analysis binding schema/arms drift')
    if len(b['source_ids']) != 20 or len(set(b['source_ids'])) != 20 or set(b['forms']) != set('AB'):
        raise ValueError('Expected20sources and2fixed reviewers')
    if b['questions'] != QUESTIONS or b['analysis'] != {'bootstrap_draws':10000,'seed':25033}:
        raise ValueError('Question/analysis protocol drift')
    for form in b['forms'].values():
        ids = []; sources = []
        if len(form['groups']) != 20:
            raise ValueError('Group count')
        for n,g in enumerate(form['groups'],1):
            if g['id'] != f'Q{n:03}' or set(g['assignments']) != set('ABCD'):
                raise ValueError('Group/letter identity')
            assignments = list(g['assignments'].values())
            if {x['arm'] for x in assignments} != set(ARMS) or len({x['source_case_id'] for x in assignments}) != 1:
                raise ValueError('Nonmatched source/arm assignment')
            sources.append(assignments[0]['source_case_id'])
            ids += [g['page']] + [g['images'][l]['item_id'] for l in 'ABCD']
            ids += [g[k] for k in ('preservation','readability','notes')]
        if sorted(sources) != sorted(b['source_ids']) or ids != form['item_ids'] or len(set(ids)) != 160:
            raise ValueError('Source/item sequence identity')
        if any(type(i) is not int or i <= 0 for i in ids):
            raise ValueError('Item ID type')
    return b


def bind_groups(groups,contract,images,key,who):
    """Do not let an internally consistent cloud log substitute canonical text/image identity."""
    if len(groups)!=20 or len(contract['groups'])!=20:
        raise ValueError('Provider/canonical group count')
    result = []
    for g,c in zip(groups,contract['groups']):
        title = 'Đoạn '+c['id'][1:]+' · Đánh giá bốn bản sửa'
        help_text = 'Người đọc: '+c['audience']+'\nMục đích: '+c['purpose']
        if g.get('who')!=who or g['id']!=c['id'] or g['page_title']!=title or g['page_help']!=help_text:
            raise ValueError('Provider source context/reviewer/order drift')
        for letter in 'ABCD':
            if g['images'][letter]['input_sha256']!=images[c['id']][letter]['sha256']:
                raise ValueError('Provider/canonical image input drift')
        row = {k:g[k] for k in ('id','page','page_title','page_help','images','preservation','readability','notes')}
        row['assignments'] = key[g['id']]; result.append(row)
    return result


def prepare(forms, amendment, out):
    from benchmarks import public_forms
    forms,amendment,out = map(Path,(forms,amendment,out))
    original = public_forms.verify(forms)
    am = read(amendment/'manifest.json'); after = read(amendment/'after.json')
    before = read(amendment/'before.json')
    if am['before_utf8_sha256'] != digest((amendment/'before.json').read_bytes()) or am['after_utf8_sha256'] != digest((amendment/'after.json').read_bytes()):
        raise ValueError('UI amendment snapshot drift')
    b = {'schema':BINDING_SCHEMA, 'cohort':simple.q.digest(original), 'is_fixture':False,
         'generation_digest':original['parent_digest'], 'ui_revision':'no-background-v2',
         'source_ids':[], 'arms':list(ARMS), 'questions':QUESTIONS, 'forms':{},
         'analysis':{'bootstrap_draws':10000,'seed':25033},
         'protocol_sha256':digest((simple.q.ROOT/'specs/014-editorial-benchmark/public-ai-human-protocol.md').read_bytes()),
         'amendment_manifest_sha256':digest((amendment/'manifest.json').read_bytes())}
    if b['cohort'] != am['parent_cohort']:
        raise ValueError('Amendment cohort drift')
    provider_audit = read(forms/'cloud/canonical-cloud-verification.json')
    image_inventory = read(forms/'images.json')
    for who in 'AB':
        log = forms/'cloud'/f'publish-paused-{who}.log'
        if digest(log.read_bytes()) != provider_audit[who]['audit_log_sha256']:
            raise ValueError('Provider mapping audit drift')
        lines = log.read_text().splitlines()
        groups = [json.loads(l[l.index('{'):]) for l in lines if '{"kind":"group_verified"' in l]
        key = read(forms/'private'/f'{who}-key.json')
        old = next(x for x in before if x['who']==who)
        current = next(x for x in after if x['who']==who)
        if current['items'] != old['items'][2:] or current['profile'] or current['state']['ui_revision'] != b['ui_revision'] or current['state']['contract_digest'] != original['contract_digests'][who]:
            raise ValueError('UI removal not bound')
        original_id = provider_audit[who]['published_paused_gate']['form_id']
        if old['state']['form_id']!=original_id or current['state']['form_id']!=original_id or old['state']['contract_digest']!=original['contract_digests'][who]:
            raise ValueError('Original/amended form identity drift')
        bound_groups = bind_groups(groups,read(forms/f'{who}-contract.json'),image_inventory[who],key,who)
        b['forms'][who] = {'form_id':current['state']['form_id'],
                           'contract_digest':original['contract_digests'][who],
                           'groups':bound_groups,'item_ids':[i['id'] for i in current['items']],
                           'responder_url':current['responder_url']}
    b['source_ids'] = sorted({v['source_case_id'] for g in b['forms']['A']['groups'] for v in g['assignments'].values()})
    validate_binding(b)
    out.mkdir(parents=True,exist_ok=False)
    save(out/'binding.json',b)
    save(out/'manifest.json',{'binding_sha256':digest(b), 'forms_manifest_sha256':digest((forms/'manifest.json').read_bytes()),
                              'code_sha256':digest(Path(__file__).read_bytes()),
                              'exporter_sha256':digest(Path(__file__).with_suffix('.gs').read_bytes()),
                              'chart_code_sha256':digest(Path(__file__).with_name('public_human_charts.py').read_bytes()),
                              'provider_audit_sha256':digest((forms/'cloud/canonical-cloud-verification.json').read_bytes()),
                              'human_labels_imported':0})
    template = Path(__file__).with_suffix('.gs').read_text()
    for who in 'AB':
        job = {'reviewer':who,'binding_digest':digest(b),'cohort':b['cohort'],
               'is_fixture':False,'ui_revision':b['ui_revision'],'questions':QUESTIONS,
               **{k:v for k,v in b['forms'][who].items() if k!='groups'},
               'groups':[{k:v for k,v in g.items() if k!='assignments'} for g in b['forms'][who]['groups']]}
        (out/f'export-{who}.gs').write_text(template.replace('/*__EXPORT_JOB__*/',json.dumps(job,ensure_ascii=False)))
    save(out/'selection-template.json',{'A':None,'B':None})
    return b


def load_binding(folder):
    folder = Path(folder); b = read(folder/'binding.json')
    manifest = read(folder/'manifest.json')
    if digest(b) != manifest['binding_sha256']:
        raise ValueError('Prepared binding drift')
    for key,path in [('code_sha256',Path(__file__)),('exporter_sha256',Path(__file__).with_suffix('.gs')),
                     ('chart_code_sha256',Path(__file__).with_name('public_human_charts.py'))]:
        if manifest[key] != digest(path.read_bytes()):
            raise ValueError('Analysis implementation changed; freeze/review a new workspace')
    return validate_binding(b)


def validate_export(b,p):
    who = p.get('reviewer')
    if p.get('schema') != EXPORT_SCHEMA or who not in b['forms'] or p.get('form_id') != b['forms'][who]['form_id']:
        raise ValueError('Foreign export schema/form/reviewer')
    if p.get('binding_digest') != digest(b) or p.get('audit_complete') is not True or p.get('is_fixture') != b['is_fixture']:
        raise ValueError('Export binding/audit/fixture drift')
    allowed = {g[k] for g in b['forms'][who]['groups'] for k in ('preservation','readability','notes')}
    seen = set()
    if not isinstance(p.get('responses'),list):
        raise ValueError('Response list')
    for response in p['responses']:
        if not isinstance(response.get('id'),str) or not response['id'] or response['id'] in seen:
            raise ValueError('Missing/duplicate response ID')
        seen.add(response['id']); item_ids = []
        if not isinstance(response.get('timestamp'),str) or not isinstance(response.get('answers'),list):
            raise ValueError('Response timestamp/answers')
        for a in response['answers']:
            if type(a.get('item_id')) is not int or a['item_id'] not in allowed or a['item_id'] in item_ids:
                raise ValueError('Unknown/duplicate provider item')
            item_ids.append(a['item_id'])
    return p


def parse_export_log(text,b):
    if '\tError\t' in text:
        raise ValueError('Failed provider execution retained; not an accepted export')
    rows = []
    for line in text.splitlines():
        start = line.find('{')
        if start >= 0:
            try: row = json.loads(line[start:])
            except json.JSONDecodeError: continue
            if row.get('kind') in ('public_human_export_part','public_human_export_done'):
                rows.append(row)
    parts = [r for r in rows if r['kind']=='public_human_export_part']
    done = [r for r in rows if r['kind']=='public_human_export_done']
    if not parts or len(done)!=1:
        raise ValueError('Missing export completion/parts')
    end = done[0]
    if type(end.get('total')) is not int or end['total'] <= 0 or len(parts) != end['total']:
        raise ValueError('Incomplete chunk count')
    for p in parts:
        if type(p.get('index')) is not int or not isinstance(p.get('data'),str):
            raise ValueError('Chunk shape')
        if any(p.get(k)!=end.get(k) for k in ('reviewer','binding_digest','sha256','total')):
            raise ValueError('Mixed exports/chunk identity')
    parts.sort(key=lambda r:r['index'])
    if [p['index'] for p in parts] != list(range(end['total'])):
        raise ValueError('Missing/duplicate chunks')
    data = ''.join(p['data'] for p in parts)
    if digest(data.encode()) != end['sha256']:
        raise ValueError('UTF8 export digest mismatch')
    packet = json.loads(data)
    if packet.get('reviewer') != end['reviewer'] or packet.get('binding_digest') != end['binding_digest']:
        raise ValueError('Envelope/content drift')
    return validate_export(b,packet)


def test_log(packet):
    """Explicit test transport, never attests a Google export."""
    data = json.dumps(packet,ensure_ascii=False,separators=(',',':'))
    chunks = [data[i:i+1000] for i in range(0,len(data),1000)]
    common = {'reviewer':packet['reviewer'],'binding_digest':packet['binding_digest'],
              'sha256':digest(data.encode()),'total':len(chunks)}
    return '\n'.join([json.dumps({'kind':'public_human_export_part',**common,'index':i,'data':c},ensure_ascii=False)
                       for i,c in enumerate(chunks)]+[json.dumps({'kind':'public_human_export_done',**common})])+'\n'


def inventory(exports):
    return {w:[{'response_id':r['id'],'timestamp':r['timestamp'],'answered_items':len(r['answers'])}
               for r in p['responses']] for w,p in exports.items()}


def normalize(b,p,response_id):
    chosen = next((r for r in p['responses'] if r['id']==response_id),None)
    if chosen is None:
        raise ValueError('Selected response not present')
    who = p['reviewer']; groups = b['forms'][who]['groups']
    decoded = simple.decode({'groups':groups},{g['id']:g for g in groups},chosen['answers'])
    rows = []; notes = []
    for g,d in zip(groups,decoded):
        cid = g['assignments']['A']['source_case_id']
        notes.append({'reviewer':who,'response_id':response_id,'source_id':cid,'display_group':g['id'],'note':d['notes']})
        for letter in 'ABCD':
            row = {'reviewer':who,'response_id':response_id,'source_id':cid,
                   'arm':g['assignments'][letter]['arm'],'display_group':g['id'],'display_letter':letter}
            row.update({k:d['outputs'][letter][k] or 'missing' for k in CATEGORIES})
            rows.append(row)
    return rows,notes


def percentile(values,q):
    k = (len(values)-1)*q; lo = int(k); hi = min(lo+1,len(values)-1)
    return values[lo]+(values[hi]-values[lo])*(k-lo)


def cluster_interval(values,draws=10000,seed=25033):
    n = len(values); estimate = sum(values)/n if n else None
    result = {'estimate':estimate,'low':None,'high':None,'n_sources':n,
              'degenerate':bool(n and len(set(values))==1)}
    if n >= 2:
        rng = random.Random(seed)
        samples = sorted(sum(rng.choices(values,k=n))/n for _ in range(draws))
        result.update(low=percentile(samples,.025),high=percentile(samples,.975))
    return result


def agreement(pairs,categories):
    matrix = {a:{b:0 for b in categories} for a in categories}
    for a,b in pairs: matrix[a][b] += 1
    usable = [(a,b) for a,b in pairs if a not in ('uncertain','missing') and b not in ('uncertain','missing')]
    n = len(usable); observed = sum(a==b for a,b in usable)/n if n else None
    ca = collections.Counter(a for a,b in usable); cb = collections.Counter(b for a,b in usable)
    expected = sum(ca[k]*cb[k] for k in categories)/(n*n) if n else None
    kappa = (observed-expected)/(1-expected) if n and expected < 1 else None
    return {'matrix':matrix,'planned_pairs':len(pairs),'determinate_pairs':n,
            'missing_pairs':sum('missing' in p for p in pairs),
            'uncertain_pairs':sum('uncertain' in p for p in pairs),
            'exact_agreement':observed,'kappa':kappa,'description':'descriptive fixed-rater output pairs; no independent-pair CI'}


def analyze(b,exports,selection,test_data=False):
    validate_binding(b)
    if b['is_fixture'] and not test_data:
        raise ValueError('Synthetic data requires explicit test_data mode')
    for who,p in exports.items():
        validate_export(b,p)
        if p['reviewer'] != who: raise ValueError('Reviewer map drift')
    if set(selection)-set('AB'): raise ValueError('Unknown selection reviewer')
    result = {'schema':'public-human-results-v1','binding_digest':digest(b),
              'is_fixture':b['is_fixture'],'status':'awaiting_human','inventory':inventory(exports),
              'planned_sources':20,'fixed_reviewers':['A','B'],'human_labels_imported':0,
              'categorical_labels_observed':0,'output_reviews_with_any_label':0,
              'before_after':[],'study_design':{'version':'within-agent-before-after-v2',
              'runtime':'Codex gpt-6.1-sol / medium','reference':'frozen original public AI source',
              'primary':'Vietnamizer readability relative to original, alongside preservation',
              'mode_contrasts':'secondary exploratory; within this runtime only',
              'cross_runtime_pooling':False},
              'quality_chart_allowed':False,'rows':[],'notes':[],'rates':[],'comparisons':[], 'agreement':{},
              'analysis':b['analysis'],'limits':['One curated public SFT publisher; generator model unattested.',
              'Intervals condition on20sources and two fixed reviewers, not a population of Vietnamese readers.',
              'All20sources retained in label counts; paired CI excludes and reports missing/uncertain source pairs.',
              'Jev advice was scope-complete in1/20sources; partial/failure cases stay in the primary cohort.',
              'No confirmatory significance tests; secondary comparisons exploratory; no equivalence claim from a null difference.',
              'No bootstrap CI with fewer than2complete sources; degenerate observed bootstrap is not certainty about a population.']}
    if not any(p['responses'] for p in exports.values()):
        return result
    if any(w not in exports or not selection.get(w) for w in 'AB'):
        result['status'] = 'selection_required'; return result
    for who in 'AB':
        rows,notes = normalize(b,exports[who],selection[who])
        result['rows'] += rows; result['notes'] += notes
    result['status'] = 'synthetic_test_only' if b['is_fixture'] else 'two_selected_human_reviews'
    result['categorical_labels_observed'] = sum(r[k]!='missing' for r in result['rows'] for k in CATEGORIES)
    result['output_reviews_with_any_label'] = sum(any(r[k]!='missing' for k in CATEGORIES) for r in result['rows'])
    result['quality_chart_allowed'] = result['categorical_labels_observed'] > 0
    result['human_labels_imported'] = 0 if b['is_fixture'] else result['categorical_labels_observed']
    lookup = {(r['source_id'],r['reviewer'],r['arm']):r for r in result['rows']}
    for who in 'AB':
        for arm in ARMS:
            for dimension,categories in CATEGORIES.items():
                count = collections.Counter(lookup[(cid,who,arm)][dimension] for cid in b['source_ids'])
                result['rates'].append({'reviewer':who,'arm':arm,'dimension':dimension,'planned_sources':20,
                    'counts':{k:count[k] for k in categories},'answered':20-count['missing'],
                    'determinate':20-count['missing']-count['uncertain']})
    # The questions directly compare each edited output to its frozen original.
    # No invented original score and no use of the bare arm as the original.
    for arm in ARMS:
        for dimension,categories in CATEGORIES.items():
            for positive in (c for c in categories if c not in ('missing','uncertain')):
                for who in ('A','B','pooled'):
                    values=[]; missing=uncertain=0
                    for cid in b['source_ids']:
                        raters='AB' if who=='pooled' else who
                        labels=[lookup[(cid,w,arm)][dimension] for w in raters]
                        missing += 'missing' in labels
                        uncertain += 'uncertain' in labels
                        if any(x in ('missing','uncertain') for x in labels): continue
                        values.append(sum(x==positive for x in labels)/len(labels))
                    result['before_after'].append({'arm':arm,'reference':'original',
                        'dimension':dimension,'metric':positive,'reviewer':who,
                        'primary':arm=='vietnamizer' and positive=='better',
                        **cluster_interval(values,b['analysis']['bootstrap_draws'],b['analysis']['seed']),
                        'planned_sources':20,'excluded_sources':20-len(values),
                        'excluded_missing':missing,'excluded_uncertain':uncertain,
                        'exclusion_counts_may_overlap':True,
                        'units':'fraction of determinate original-relative ratings; display percent'})
    for a,b_arm in COMPARISONS:
        for metric,dimension,positive in [('better','readability','better'),('changed','preservation','changed')]:
            for who in ('A','B','pooled'):
                values = []; missing = uncertain = 0
                for cid in b['source_ids']:
                    raters = 'AB' if who=='pooled' else who
                    labels = [(lookup[(cid,w,a)][dimension],lookup[(cid,w,b_arm)][dimension]) for w in raters]
                    flat = [x for pair in labels for x in pair]
                    missing += 'missing' in flat; uncertain += 'uncertain' in flat
                    if any(x in ('missing','uncertain') for x in flat): continue
                    values.append(sum(int(x==positive)-int(y==positive) for x,y in labels)/len(labels))
                result['comparisons'].append({'a':a,'b':b_arm,'metric':metric,'reviewer':who,
                    'primary':False,'role':'secondary exploratory within-agent mode contrast',
                    **cluster_interval(values,b['analysis']['bootstrap_draws'],b['analysis']['seed']),
                    'planned_sources':20,'excluded_sources':20-len(values),
                    'excluded_missing':missing,'excluded_uncertain':uncertain,
                    'exclusion_counts_may_overlap':True,'units':'fraction difference a-minus-b; display percentage points'})
    for dimension,categories in CATEGORIES.items():
        pairs = [(lookup[(cid,'A',a)][dimension],lookup[(cid,'B',a)][dimension]) for cid in b['source_ids'] for a in ARMS]
        result['agreement'][dimension] = agreement(pairs,categories)
    return result


def csv_file(path,rows):
    if not rows: return
    fields = list(dict.fromkeys(k for row in rows for k in row))
    def safe(x):
        if isinstance(x,str) and (x.startswith(('\t','\r','\n')) or x.lstrip().startswith(('=','+','-','@'))): return "'"+x
        return x
    with Path(path).open('w',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=fields); writer.writeheader()
        writer.writerows({k:safe(v) for k,v in row.items()} for row in rows)


def write_report(out,result,exports,selection,raw_sources=None):
    out = Path(out); out.mkdir(parents=True,exist_ok=False); (out/'raw').mkdir()
    save(out/'raw/exports.json',exports); save(out/'raw/selection.json',selection)
    for name,raw in (raw_sources or {}).items():
        if Path(name).name != name: raise ValueError('Raw filename')
        (out/'raw'/name).write_bytes(raw if isinstance(raw,bytes) else raw.encode())
    save(out/'summary.json',result)
    csv_file(out/'ratings.csv',result['rows']); csv_file(out/'notes.csv',result['notes'])
    csv_file(out/'before-after.csv',result['before_after'])
    csv_file(out/'paired-differences.csv',result['comparisons'])
    rates = [{k:v for k,v in r.items() if k!='counts'} | r['counts'] for r in result['rates']]
    csv_file(out/'label-counts.csv',rates)
    matrix = [{'dimension':d,'A':a,'B':b,'count':n} for d,r in result['agreement'].items() for a,cols in r['matrix'].items() for b,n in cols.items()]
    csv_file(out/'agreement.csv',matrix)
    save(out/'receipt.json',{'status':result['status'],'binding_digest':result['binding_digest'],
                            'result_sha256':digest((out/'summary.json').read_bytes()),
                            'is_fixture':result['is_fixture'],'raw_source_sha256':{p.name:digest(p.read_bytes()) for p in (out/'raw').iterdir()},
                            'code_sha256':digest(Path(__file__).read_bytes())})
    return out


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command',required=True)
    p = sub.add_parser('prepare'); p.add_argument('--forms',type=Path,required=True); p.add_argument('--amendment',type=Path,required=True); p.add_argument('--output',type=Path,required=True)
    for command in ('inventory','analyze'):
        p = sub.add_parser(command); p.add_argument('--workspace',type=Path,required=True); p.add_argument('--logs',type=Path,nargs='*',default=[])
        if command=='analyze':
            p.add_argument('--selection',type=Path); p.add_argument('--output',type=Path,required=True); p.add_argument('--test-data',action='store_true'); p.add_argument('--charts',action='store_true')
    a = parser.parse_args()
    if a.command=='prepare': prepare(a.forms,a.amendment,a.output); print('Prepared immutable analysis binding and read-only A/B exporters'); return
    b = load_binding(a.workspace); exports = {}; raws = {}
    for n,path in enumerate(a.logs):
        raw = path.read_bytes(); p = parse_export_log(raw.decode(),b)
        if p['reviewer'] in exports: raise ValueError('Duplicate reviewer exports; choose one exact snapshot')
        exports[p['reviewer']] = p; raws[f'{n:02}-{path.name}'] = raw
    if a.command=='inventory': print(json.dumps(inventory(exports),ensure_ascii=False,indent=2)); return
    selection = read(a.selection) if a.selection else {}
    result = analyze(b,exports,selection,a.test_data)
    if a.charts and not result['quality_chart_allowed']: raise ValueError('No selected human quality data; charts withheld')
    write_report(a.output,result,exports,selection,raws)
    if a.charts:
        from benchmarks.public_human_charts import charts
        charts(a.output)
    print(json.dumps({'status':result['status'],'human_labels_imported':result['human_labels_imported'],'quality_chart_allowed':result['quality_chart_allowed']}))


if __name__=='__main__': main()
