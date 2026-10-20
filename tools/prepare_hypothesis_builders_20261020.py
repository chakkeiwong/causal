from pathlib import Path
p=Path('tools/build_expert_averaging_reader_20261020.py')
s=p.read_text().replace('expert_averaging_reference_20261020','hypothesis_reference_20261020')
s=s.replace('census-expert-averaging-v1','census-hypothesis-v1').replace('census-validity-v1','java-effects-v1')
s=s.replace('causal_proposal_validity_measurement_reviewed','causal_proposal_java_effects_reviewed')
s=s.replace('causal_proposal_expert_averaging_reviewed','causal_proposal_hypothesis_generation_reviewed')
s=s.replace("LABELS = ['exec20:expert-'+x for x in ['scope','semantics','votes','majority','cycle','evidence','budget','identification','worlds','effects']]","LABELS = ['exec20:hypothesis-'+x for x in ['scope','claims','evidence','denominators','graph','jaccard','world','evaluation','anova','prototype']]")
s=s.replace('program/execution/2026-10-14/iid-discovery/publication/development.tex','program/gap-repair-v13/work/LA07/translation-extension.tex')
a=s.index("    write(BASE/'manuscript-plan-review.json'");b=s.index('    bibliography=[]',a)
s=s[:a]+'''    write(BASE/'manuscript-plan-review.json',dict(status='pass',
        scope='Preserve all earlier content; integrate source-critical hypothesis-generation argument',
        evidence=[ref(DEVELOPMENT,'Connected banking argument'),ref(BASE/'review.json','Inspected authentic article')],
        checks=['Preserve every earlier source identity, citation context and compiled content input.',
          'Distinguish source relation extraction, candidate generation, novelty evaluation and causal identification.',
          'Retain comparator selection, adverse ratings, printed statistical inconsistencies and unavailable supplement.',
          'Specify held-out public experiments and typed library/CLI/MCP outputs without claiming implementation.']))
    write(BASE/'mathematical-review.json',dict(status='pass_for_scoped_project_argument',issues=[],
        evidence=[ref(ROOT/'tools/hypothesis_reference_20261020.py','Independent arithmetic'),
          ref(BASE/'exact-results.json','Reproduced values'),ref(DEVELOPMENT,'Explicit causal construction')],
        findings=['Causal-label156/238 differs from relation-existence207/238; preserve their denominators.',
          'Ordinary F upper tail at5.25,3,116 is about.001967, independently checked by beta integral.',
          'Ordinary ANOVA identity at F84.1611,3,1652 implies R2about.132573, not printed.8696.',
          'Common cause and common consequence yield Jaccard1 but zero effect A on B in the displayed SCM.',
          'Assumed value100 and cost20 give invalid similarity-based80 versus stipulated causal-20.',
          'No raw-data reanalysis, native behavior, generic theorem or bank result inferred.'],
        native_execution=False,empirical_coverage=False,all_source_theorems_independently_verified=False))
    write(BASE/'copyedit-review.json',dict(status='pass',evidence=[ref(DEVELOPMENT,'Connected source-critical argument')],
        findings=['Define evidence objects and causal targets before presenting graph scores.',
          'Describe reported novelty ratings as source outcomes, not reproduced causal validation.',
          'Keep numerical inconsistencies conditional on ordinary stated ANOVA and request original analysis.',
          'Distinguish paper methods from proposed public experiments and unimplemented interfaces.'],rendered_review=False))
'''+s[b:]
s=s.replace('Population and attribution working successor','Hypothesis-generation working successor')
Path('tools/build_hypothesis_reader_20261020.py').write_text(s)
s=Path('tools/review_publish_expert_averaging_reader_20261020.py').read_text()
s=s.replace('build_expert_averaging_reader_20261020','build_hypothesis_reader_20261020').replace('expert_averaging_reference_20261020','hypothesis_reference_20261020').replace('review_expert_averaging_20261020','review_hypothesis_20261020')
s=s.replace('exec20_expert_averaging_reference','exec20_hypothesis_reference').replace('exec20_expert_averaging','exec20_hypothesis_generation')
s=s.replace('A bank building a diagram from several discovery algorithms','A bank translating a business question into a causal analysis')
s=s.replace('qualification of an intervention service requires its own evidence','qualification of a banking intervention still requires evidence about that intervention')
s=s.replace("['1012581','1048576','93.3','43.9','66.4','cached','USD 14','acyclic','printed','90%']","['43,312','65.55','86.97','0.001967','0.132573','USD 80','USD -20','Jaccard','hypothesis','60']")
s=s.replace("['exec20:expert-majority','exec20:expert-cycle','exec20:expert-worlds','exec20:expert-effects']","['exec20:hypothesis-denominators','exec20:hypothesis-jaccard','exec20:hypothesis-world','exec20:hypothesis-anova']")
s=s.replace('expert-guided discovery','hypothesis-generation').replace('expert_averaging_reader','hypothesis_reader')
a=s.index("            'All828 earlier");b=s.index('        limitations=LIMITS',a)
s=s[:a]+'''            'All845 earlier citation records and contexts and all preceding content inputs survive.',
            'One genuine July2024 article and one authored reference add two audited citations.',
            'Reported extraction, selection, novelty and utility findings retain their evidence limits.',
            'Printed statistical inconsistencies are checked conditionally; unavailable raw analysis is not reconstructed.',
            'A graph-similarity witness gives score1 with zero effect and assumed margins80/-20.',
            'Census advances to54 inspected/59 unread without coverage or native acceptance.'],
'''+s[b:]
s=s.replace('Integrate expert-guided graph discovery, source-critical benchmark comparison, query specification and intervention limits; census53/60.','Integrate literature-based hypothesis generation, source-critical evaluation and public prototype design; census54/59.')
a=s.index('    findings={');b=s.index('    for q,finding',a)
s=s[:a]+'''    findings={
        'Q2':f'All {checks["preserved_records"]} prior records and citation contexts survive. Genuine14-page July2024 v3 inspected, earlier v1 and failed publisher routes preserved. Revised supplement and raw analysis stay open.',
        'Q3':'Relation-label denominators, ordinary F/beta-tail and ANOVA R2 checks reproduce. A structural common-cause/common-consequence graph has Jaccard1 and effect0. Printed discrepancies do not establish corrected raw-data conclusions.',
        'Q4':'Assumed value100 and cost20 produce invalid score-based80 versus true stipulated-20. Proposed public experiments separate extraction, operational translation, novelty and interventions; full expert/model costs and bank return remain unmeasured.'}
'''+s[b:]
Path('tools/review_publish_hypothesis_reader_20261020.py').write_text(s)
print('Created preserving hypothesis reader builder and publisher.')

