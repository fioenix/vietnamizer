#!/usr/bin/env python3
"""Regenerate shipped question definitions from recipes and canonical exclusions."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# English instructions are recipes; Vietnamese rules/exclusions remain canonical in source.
RECIPES = {
'V1': 'Does the intended result, capability or direction of the action require a missing complement such as được or ra? Distinguish deliberate refusal from inability.',
'V2': 'Does an omitted paired connective actually obscure the relation between clauses? A relation already clear in Vietnamese needs no extra thì or nên.',
'V3': 'Is là required to express this definition or selection, rather than an adjective predicate, action or legitimate label?',
'V4': 'Is a temporal/aspect marker missing or redundant in the established sequence of events? Preserve completion, continuation and timing.',
'V5': 'Is a classifier genuinely missing or inappropriate for this noun in its intended count/mass/generic sense and regional usage?',
'V6': 'Does the question/request frame conflict with the communicative intention supported by the supplied relationship and context?',
'V7': 'Is a particular của dispensable without losing ownership, source, subject or an unambiguous noun relation?',
'V8': 'Is a particular các/những unnecessary or wrong for the intended whole set, subset or generic scope?',
'V9': 'Does a long prepositional phrase add avoidable wording without contributing a necessary relation or genre convention?',
'V10': 'Does adverb placement create materially competing attachments not resolved by context?',
'V11': 'Does the introductory frame add no information or genuine warning, explanation or discourse function?',
'V12': 'Do repeated sentence-initial connectors unnecessarily duplicate relations already clear in this paragraph?',
'V13': 'Does rigid repetition of sentence openings break the old-to-new information flow of this paragraph?',
'V14': 'Is a noun phrase incorrectly presented as a complete prose sentence rather than a heading, label or intentional fragment?',
'V15': 'Do nominalizations and light verbs obscure an action without adding meaning, beyond legitimate fixed terminology?',
'V16': 'Is passive wording unnecessarily copied or cumbersome here, rather than expressing result, ability, benefit, adversity or a justified topic focus?',
'V17': 'Is the long expression replaceable by là/có without losing role, ownership, contrast or meaningful emphasis?',
'V18': 'Are subjects or referents materially unclear across clauses, rather than recoverable Vietnamese ellipsis?',
'V19': 'Is an English insertion inappropriate for the supplied audience and domain, rather than an established term or community usage?',
'V20': 'Is a lexical expression internally incomplete or an unnatural combination in its intended sense? Distinguish valid standalone words and community shortening from actual missing syllables.',
'V21': 'Does this sentence address the commissioning user as leftover assistant conversation instead of the intended document reader?',
'V22': 'Does a source-limitation disclaimer precede a concrete speculation unsupported by the supplied evidence? Do not infer truth from plausibility.',
'V23': 'Does the sentence rebut a position absent from the supplied discussion rather than make an informative contrast?',
'V24': 'Do possibility/uncertainty expressions duplicate the same scope, such that removing one preserves the exact epistemic commitment?',
'V25': 'Has a specific relation established in the supplied source become vague or lost its direction/type/certainty in this target?',
'T1': 'Is capitalization inappropriate for Vietnamese headings/common nouns, excluding proper and official names whose spelling must be preserved?',
'T2': 'Is a dash used contrary to the canonical typography rule, excluding protected text, valid en-dash ranges, dialogue and name pairs?',
'T3': 'Check quotation pairing and consistency mechanically.',
'T4': 'Is the comma before và dispensable here without losing list boundaries, clause distinction or intentional rhythm?',
'T5': 'Do repeated label-colon structures add no real classification, subtitle, lookup or data-field function?',
'T6': 'Are decorative emoji contrary to an explicit genre/user requirement, excluding informative symbols and accepted social usage?',
'B1': 'Does a claim of importance inflate significance without concrete information in the supplied text?',
'B2': 'Is an off-the-shelf metaphor or translated idiom replacing information or mixing incompatible imagery, rather than an established term or developed image?',
'B3': 'Does a generic opening delay the actual subject without specific context or a genuine teaching function?',
'B4': 'Is the optimistic closing generic and uninformative, excluding a genuine wish, concrete plan or required conclusion?',
'B5': 'Does the parallel contrast merely restate the first clause more strongly instead of adding distinct information?',
'B6': 'Is the opening question a formula delaying a direct explanation rather than a real question, useful rhetoric or FAQ?',
'B7': 'Does promotional praise lack concrete distinguishing observations in the supplied text?',
'B8': 'Is an unsubstantiated rank or anonymous authority being used to persuade, without supporting evidence in scope?',
'B9': 'Is an unnecessarily formal Sino-Vietnamese choice mismatched to this author/audience, excluding defined technical terminology?',
'B10': 'Is an idiom misused in meaning or is its density obstructing the paragraph? Do not invent an idiom origin or ignore regional variants.',
'B11': 'Does symmetrical triadic rhythm substitute for information rather than enumerate three genuinely distinct facts?',
'B12': 'Is a four-syllable slogan semantically empty here, excluding an established administrative/technical term?',
'B13': 'Does uniform sentence rhythm obscure changes of emphasis, excluding purposeful parallelism and supplied author habits?',
'B14': 'Does a request/advice/reassurance sound unintentionally harsh for the evidenced relationship because appropriate modality is missing?',
'B15': 'Are pronouns inconsistent or referentially unclear given the supplied roles? Never infer age or hierarchy.',
'B16': 'Is familiarity ungrounded in the relationship or concrete personal account, rather than the author’s legitimate voice?',
'B17': 'Does an unintentional register shift conflict with the established function/voice, rather than regional or purposeful variation?',
'K1': 'Does a description unnecessarily narrate its own diff rather than explain current behavior, excluding changelogs and progress reports?',
'K2': 'Does institutional wording add empty formality without a concrete object or content, excluding legitimate administrative language?',
'K3': 'Do symmetrical headings reflect a hollow template rather than the actual content or a required document structure?',
'K4': 'Is an abstract explanation difficult to understand because a relevant existing in-scope example is not shown nearby?',
'K5': 'Does the first sentence merely repeat its heading without scope, condition, warning or useful summary?',
'K6': 'Does this sentence describe producing this document for its commissioner rather than serve the intended reader, excluding meaningful ADR/workflow history?',
'K7': 'Does an anonymous appeal to expertise substitute for identifiable supporting evidence within the supplied sources?',
}
SCORES = {'V9','V11','V12','V13','V15','V18','V19','V20','B1','B3','B4','B7','B9','B10','B13','B14','B16','B17','K2','K4','K5'}
CHOICES = {
'V1':['ongoing_action','deliberate_refusal','failed_result_or_capability','direction'],
'V2':['causal','conditional','concessive','additive'],
'V3':['definition_or_selection','adjective_predicate','action','label'],
'V4':['completed','ongoing','continuing','not_yet','timeless'],
'V5':['count_individual','mass_or_abstract','generic','label_or_term'],
'V6':['yes_no_question','open_question','request','command','rhetorical'],
'V8':['whole_defined_set','subset','generic'],
'V10':['one_supported_attachment','competing_attachments'],
'V14':['prose_sentence','heading_or_label','intentional_fragment'],
'V16':['passive','capability_or_result','benefit_or_adversity'],
'V18':['clear_referent','context_licensed_ellipsis','competing_referents'],
'V19':['proper_name','established_term','community_usage','unhelpful_insertion'],
'V20':['standalone_word','community_shortening','internal_truncation','unnatural_collocation'],
'V21':['assistant_remnant','genuine_greeting_or_wish','quoted_or_discussed_content'],
'V22':['supported','contradicted','not_addressed','ambiguous'],
'V23':['present_opponent_or_alternative','informative_contrast','invented_opponent'],
'V24':['same_epistemic_scope','distinct_scopes'],
'V25':['relation_preserved','relation_weakened','relation_changed','source_unspecified'],
'T1':['heading','common_noun','proper_or_official_name'],
'T2':['incidental_aside','range','dialogue','name_pair','hyphen'],
'T4':['simple_list','complex_list_boundary','clauses','intentional_rhythm'],
'T5':['data_field','real_classification','subtitle','decorative_label'],
'T6':['informative_symbol','accepted_social_decoration','inappropriate_decoration'],
'B2':['established_term','developed_metaphor','stock_or_mixed_imagery'],
'B4':['concrete_plan','genuine_wish','required_conclusion','generic_closing'],
'B5':['distinct_information','repetition_or_inflation'],
'B6':['real_question','faq','useful_rhetoric','delaying_formula'],
'B8':['supported','contradicted','not_addressed','ambiguous'],
'B9':['defined_term','appropriate_register','unnecessary_formality'],
'B10':['supported_idiom_sense','possible_regional_variant','misused_sense'],
'B11':['distinct_facts','rhythm_without_information'],
'B12':['defined_term','ordinary_expression','empty_slogan'],
'B14':['request','advice','reassurance','information'],
'B15':['clear_roles','unresolved_roles','inconsistent_reference'],
'B17':['purposeful_shift','distinct_section_function','unintentional_mismatch'],
'K1':['current_description','necessary_change_history','unnecessary_diff_narration'],
'K3':['required_structure','content_led_structure','hollow_template'],
'K6':['subject_content','useful_history','production_metadata'],
'K7':['supported','contradicted','not_addressed','ambiguous'],
}

# These options describe the target's function/support, never support for a
# violation hypothesis. Noul remains the independent defect judgment.
CHOICE_DESCRIPTIONS = {
 'V14': {
  'complete_clause':'A complete Vietnamese clause, including context-licensed subject ellipsis.',
  'standalone_noun_phrase_sentence':'A noun phrase is punctuated as a complete prose sentence without a licensed predicate.',
  'heading_or_label':'A heading, label, lookup entry or table cell; no prose predicate is required.',
  'intentional_fragment':'An intentional fragment supported by its discourse function.'},
 'V16': {
  'justified_topic_or_genre_passive':'A true passive serving topic focus, result emphasis or an established administrative/technical convention.',
  'cumbersome_translated_passive':'A cumbersome passive copied from another language without a supported topic or genre function.',
  'capability_or_result':'Được expresses ability or achieved result rather than a passive construction.',
  'benefit_or_adversity':'Được/bị expresses benefit or adversity appropriate to the intended meaning.'},
 'V22': {
  'claim_supported_by_source':'The target factual assertion is supported by actual supplied source passages, not merely by a disclaimer.',
  'claim_contradicted_by_source':'The actual supplied source contradicts the target factual assertion.',
  'claim_not_addressed_by_source':'A source is supplied but does not establish the target factual assertion.',
  'licensed_forecast_or_limit':'Explicit forecast/risk scenario, grounded estimate, data cutoff or research limitation; not an unsupported assertion presented as fact.',
  'ambiguous_claim_or_scope':'The target assertion or its source relation has multiple readings; do not infer external truth.'},
 'T1': {
  'ordinary_sentence_case':'Heading/common-noun capitalization follows Vietnamese sentence case.',
  'unmotivated_title_case':'Common words have unsupported English-style Title Case.',
  'proper_or_official_name':'Capitalization belongs to a proper or official name and must be preserved.',
  'intentional_design_caps':'All-caps typography is an intentional design/format requirement.'},
}
for _ident in ('B8','K7'):
 CHOICE_DESCRIPTIONS[_ident] = {
  'claim_supported_by_source':'Actual supplied identifiable evidence supports the target authority, attribution or ranking claim.',
  'claim_contradicted_by_source':'Actual supplied evidence contradicts that specific claim.',
  'claim_not_addressed_by_source':'A source is supplied but does not support that specific claim; its mere presence is not support.',
  'licensed_attribution_or_example':'An attributed view, illustrative quotation or domain-specific convention has a legitimate evidenced function.',
  'ambiguous_claim_or_scope':'The target claim or evidence relation is ambiguous. Missing source evidence belongs to insufficient, not inferred truth.'}


def _alternatives(expression):
    """Top-level alternatives, with one capturing group of plain alternatives split into variants."""
    parts=[];depth=0;current=''
    for i,ch in enumerate(expression):
        escaped=i>0 and expression[i-1]=='\\'
        if ch=='(' and not escaped:depth+=1
        if ch==')' and not escaped:depth-=1
        if ch=='|' and depth==0:
            parts.append(current);current='';continue
        current+=ch
    parts.append(current)
    variants=[]
    for part in parts:
        group=re.fullmatch(r'(.*?)\(([^()]*)\)(.*)',part)
        if group and '|' in group.group(2):
            variants.extend(group.group(1)+'(?:'+x+')'+group.group(3) for x in group.group(2).split('|'))
        else:
            variants.append(part)
    return variants


def signals(skill_text):
    """Tier 3 ordering signals: scan-tells.sh alternatives that their own SKILL.md section supports."""
    sections={m.group(1):m.group(0) for m in re.finditer(r'^### ([VT]\d+)\..*?(?=^### |\Z)',skill_text,re.M|re.S)}
    kept={};dropped=[]
    for line in (ROOT/'scripts/scan-tells.sh').read_text(encoding='utf-8').splitlines():
        m=re.match(r"""scan "([VTBK]\d+) [^"]*" '([^']*)'""",line.strip())
        if not m:continue
        # grep matches line by line: keep that in Python, or `\s`/`[^x]` cross newlines and backtrack.
        expression=m.group(2).replace('[[:space:]]',r'[ \t]').replace('[^','[^\\n')
        ident=m.group(1)
        for variant in _alternatives(expression):
            re.compile(variant,re.M)
            # Grounding ignores line anchors and case: the section quotes signs inside sentences.
            if re.search(variant.lstrip('^'),sections.get(ident,''),re.I):kept.setdefault(ident,[]).append(variant)
            else:dropped.append((ident,variant))
    return kept,dropped


def build():
    entries = []
    kept,_ = signals((ROOT/'SKILL.md').read_text(encoding='utf-8'))
    for source in ['SKILL.md','profiles/blog-ca-nhan/rules.md','profiles/ky-thuat-doanh-nghiep/rules.md']:
        text = (ROOT/source).read_text()
        matches = list(re.finditer(r'^### ([VTBK]\d+)\. (.+)$', text, re.M))
        for i, m in enumerate(matches):
            ident, title = m.groups()
            block = text[m.end():matches[i+1].start() if i+1<len(matches) else len(text)]
            no_flag = re.search(r'\*\*Không flag:\*\*\s*(.*?)(?=\n\n(?:##|---)|\Z)', block, re.S).group(1).strip()
            scope = 'paragraph' if ident in {'V12','V13','T5','B3','B4','B7','B10','B11','B13','B15','B16','B17','K3','K4','K5','K6'} else 'target'
            qs = [{'key':'violation','type':'noul','instructions':RECIPES[ident]}]
            if ident in CHOICES:
                options = dict(CHOICE_DESCRIPTIONS[ident]) if ident in CHOICE_DESCRIPTIONS else {x: x.replace('_',' ') for x in CHOICES[ident]}
                options.update({'none_fit':'None of these interpretations fits.','insufficient':'The supplied evidence cannot resolve this interpretation.'})
                qs.append({'key':'interpretation','type':'choice','instructions':f'Classify the target expression’s own function or source-support relation, not whether a violation hypothesis is supported. Which supplied interpretation fits the target in context? {RECIPES[ident]}','criteria':options})
            if ident in SCORES:
                qs.append({'key':'evidence','type':'choice','instructions':f'Can the supplied context establish the intended meaning, reference, audience and exceptions needed to judge this issue? {RECIPES[ident]}','criteria':{'sufficient':'The necessary context is supplied; the issue may be present or absent.','insufficient':'A necessary fact, intended referent or context is missing.','none_fit':'These context dispositions do not fit the supplied evidence.'}})
                qs.append({'key':'degree','type':'score','instructions':f'Rate ONLY the degree of the specific issue described in this question, not overall writing quality: {RECIPES[ident]} Context insufficiency is not a middle score.','criteria':['No established instance of this issue in the target context.','A slight instance; little effect on the relevant reading function.','A clear instance affecting the relevant reading function.','A pronounced instance substantially obstructing the relevant reading function.']})
            entries.append({'id':ident,'title':title,'source':source,'scope':scope,'mode':'mechanical' if ident=='T3' else 'semantic','no_flag':no_flag,'questions':[] if ident=='T3' else qs})
            if ident in kept:entries[-1]['signals']=kept[ident]
    expected = {f'{p}{i}' for p,n in [('V',25),('T',6),('B',17),('K',7)] for i in range(1,n+1)}
    assert len(entries)==55 and {e['id'] for e in entries}==expected==set(RECIPES)
    return {'version':'1','model':'jev-1.14.0','patterns':entries}


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--check',action='store_true'); args=parser.parse_args()
    target=ROOT/'jev/registry.json'; content=json.dumps(build(),ensure_ascii=False,indent=2)+'\n'
    for ident,variant in signals((ROOT/'SKILL.md').read_text(encoding='utf-8'))[1]:
        print(f'signal not in canonical {ident} section, not shipped: {variant}')
    if args.check:
        if not target.exists() or target.read_text()!=content:
            raise SystemExit('Registry is stale; run scripts/build-jev-registry.py')
        print('55 pattern definitions match canonical sources')
    else:
        target.write_text(content)


if __name__=='__main__': main()
