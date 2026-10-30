"""Assemble a thematic reading edition without editing protected research sources."""
from collections import Counter
from hashlib import sha256
from pathlib import Path
import argparse
import json
import re
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
OLD = DOCS / 'causal_proposal_panel_runtime_reviewed_v2_2026-10-29.tex'
OUT = DOCS / 'reading-edition'
DRIVER = DOCS / 'causal_banking_reading_edition_2026-10-29.tex'
B = chr(92)
INPUT = re.compile(re.escape(B)+'input'+r'\{([^}]+)\}')
EDIT_LOG = []


def read(path):
    return path.read_text()


def resolve(name):
    return DOCS / (name if name.endswith('.tex') else name+'.tex')


def change(text, old, new, source, reason):
    if old not in text:
        pattern=r'\s+'.join(re.escape(x) for x in old.split())
        match=re.search(pattern,text)
        if not match:
            raise ValueError('Missing expected editorial passage: '+source+' / '+old[:65])
        old=match.group(0)
    EDIT_LOG.append(dict(source=source, reason=reason, before=old, after=new))
    return text.replace(old,new,1)


def edits(path,text):
    rel=str(path.relative_to(DOCS))
    def swap(old,new,reason='Replace authoring or engineering phrasing with the economic meaning'):
        nonlocal text
        text=change(text,old,new,rel,reason)
    titles={
      'Survey method and the common causal software contract':'Choosing software by the economic question',
      'Composing software without changing the scientific question':'What a shared service must preserve',
      'Causal software as a scientific interface':'Comparing methods by what they estimate',
      'Matched qualification and build, buy or integrate decisions':'Build, buy or combine existing methods?',
      'Agents, language boundaries and qualification':'Assistance and implementation choices',
      'Deriving a common causal-analysis product':'A shared service for economic analysis',
      'Data organization, execution and reusable interfaces':'From bank records to a reproducible study',
      'Investment, adoption and the independent product':'The investment case and its alternatives',
      'Information, uncertainty and executable limits':'What additional information buys',
      'Weak-audit projection for funding value':'Funding value when customer identity is uncertain',
      'Joint candidate information and calibration limits':'Using shared information to narrow uncertainty',
      'Linked outcome audits for a dependent funding decision':'Learning funding responses from verified histories',
      'Graph meaning and uncertainty through the computational path':'Keeping causal ambiguity in the estimated effect',
      'Histories, forest targets and the units of causal calculations':'Customer histories, heterogeneous effects and economic units',
      'Catalog context for causal observations':'Understanding the records behind an estimate',
      'Variable meaning, ontology and the observation that a causal claim needs':'Defining economic variables and measuring them',
      'Runtime versions, covariance order and metadata custody':'Why reported uncertainty must survive a change of software',
      'Preserving panel uncertainty across result schemas and numerical delegates':'Carrying uncertainty through a panel comparison',
      'Estimator internals and the meaning of a portable event study':'What an event-study estimate represents',
      'What the panel delegates preserve and what an adapter must add':'Keeping the population and comparison fixed',
      'Four different objects called causal reasoning':'Four different questions about cause and effect',
      'Decision meaning, alternatives and remaining obligations':'Financial interpretation and the information still needed',
      'Economics and the remaining obligations':'Financial value and unresolved evidence',
      'An admissible route before a preferred supplier':'Choose the method before the supplier',
      'The scientific request is larger than an estimator call':'Define the study before choosing an estimator',
      'A cutoff candidate is not an installed runtime':'Software versions and the scope of the evidence',
      'A bounded survey that can be extended without changing its claims':'The scope of the comparison',
      'Compare a scientific operation before comparing a package':'Start with the banking comparison',
      'The scientific object comes before the search algorithm':'Define the economic relationships before searching for them',
      'The data product is part of the statistical experiment':'What the bank records determines what can be learned',
      'What the product is entitled to return':'What the evidence allows us to conclude',
      'Result types follow the additional assumptions':'Additional assumptions change the answer',
      'Consequences for the shared learning layer':'Implications for estimation in the bank',
      'Which object needs to be recovered?':'Which economic quantity must be recovered?',
      'Structural equations supply the intervention semantics':'Structural equations define what an intervention changes',
      'Commercial alternatives, acquisition boundaries and the competitive capability gap':'Commercial alternatives and the capabilities still needed',
      'Causal operations and mathematical interchange contracts':'Keeping the economic question intact across methods',
      'Workspace consumers and complete banking workflows':'Using the analysis in other research applications',
      'Operating the local causal service and qualifying its limits':'Conducting a study with the proposed service',
      'Packages, model backends and auditable agent architecture':'Choosing tools for an accountable research assistant',
      'Choose the contract before the framework':'Define the research task before choosing the software',
      'Agents across the causal decision workflow':'Assistance from research design to interpretation',
      'Graph meaning and uncertainty through the computational path':'Keeping causal uncertainty through the calculation',
      'Banking studies as tests of the scientific construction':'What the banking studies establish',
      'An adapter maps mathematical objects as well as arrays':'Changing software must preserve the economic quantity',
      'Native identification engines and the joint meaning of a counterfactual':'Counterfactual comparisons in C++ libraries',
      'Java identification requires a typed scientific result':'Distinguishing identified effects from unresolved comparisons in Java',
      'Four questions that require four capability descriptions':'Four questions a commercial tool may answer',
      'What a commercial engine boundary would have to preserve':'What a commercial integration must retain',
      'Commercial staggered DID: compare the target before the coefficient':'Commercial difference-in-differences methods for staggered adoption',
      'Choosing an IV reference requires a declared model and a conversion boundary':'Choosing an instrumental-variable method for the stated model',
      'Panel software as a contract for timing, weighting and uncertainty':'Panel software: timing, weighting and uncertainty',
      'Reusable trend sensitivity requires the full statistical contract':'How departures from parallel trends change the conclusion',
      'Independent causal and scoring oracles for public agent qualification':'Evaluating assistance when the causal answer is known',
      'Enforcing a public discovery evaluation contract':'Comparing discovery methods on a defined public experiment',
      'Structured outputs, response states and scientific admission':'Interpreting structured answers from a language model',
      'Framework delegates, schema conversion and scientific completion':'When a completed software call leaves the research unfinished',
      'Qualifying the worker, custody and replay boundary':'Reproducing the calculation and its evidence',
      'Source closure and remaining obligations':'What the available evidence leaves unresolved',
      'Operations preserve meaning and evidence':'Keeping uncertainty visible in the reported result',
      'Public qualification and outstanding obligations':'Comparisons still needed',
      'Proposal acceptance and later\nqualification':'The evidence needed before investing',
    }
    # Exact heading substitutions only: scientific body terms retain their meanings.
    for old,new in titles.items():
        if old in text:
            heading=re.compile(r'(\\(?:chapter|section|subsection)(?:\[[^\]]*\])?\{)'+re.escape(old)+r'(\})')
            revised,n=heading.subn(lambda m:m.group(1)+new+m.group(2),text)
            if n:
                EDIT_LOG.append(dict(source=rel,reason='Reader-facing heading',before=old,after=new))
                text=revised
    # These exact recurring sentences concern manuscript administration, not a
    # statistical or product property. Keep the material native-evidence limit.
    boilerplate={
      'No native, visual or final acceptance is claimed.':'The packages have not been validated by execution in this comparison.',
      'Native qualification, independent review, visual and final acceptance remain open':'Package execution and independent validation remain to be performed',
      'Independent review, visual review and final acceptance remain open.':'The proposed integration still requires independent review.',
      'These local limits do not block independent proposal work.':'Other methodological comparisons can proceed independently.',
      'These follow-ups can proceed independently of prototype qualification and whole-manuscript acceptance.':'Each comparison can be developed independently of the others.',
      'The immediate deliverable is a reasoned, testable reuse proposal.':'The comparison supports a testable reuse recommendation.',
      'the immediate deliverable is a reasoned, testable reuse proposal.':'the evidence supports a testable reuse recommendation.',
      'The immediate deliverable is a reviewable product choice with an explicit path to a prototype.':'The evidence supports a provisional product choice and specifies the tests needed before integration.',
      'The immediate deliverable should be a conditional route decision, with a specific supported profile and a finite acceptance experiment.':'A provisional choice should specify the method, environment and comparison that could justify adoption.',
      'The Python IV/RD cell therefore receives an inconclusive coverage outcome.':'The comparison of Python instruments and discontinuities remains incomplete.',
      'All three language cells remain inconclusive.':'The comparisons in all three languages remain incomplete.',
      'Independent review and adoption remain separate from author completion.':'Independent review and the bank\'s adoption decision require their own evidence.',
      'Native, independent, bank, visual and final acceptance remain open.':'Execution of the package, independent validation and evaluation in a bank remain outstanding.',
      'Complete native, independent, bank, visual and final acceptance remain open':'Execution of the complete package, independent validation and evaluation in a bank remain outstanding',
      'Native, independent, bank, visual and final acceptance remain open':'Execution of the package, independent validation and evaluation in a bank remain outstanding',
      'This completes a reference-only proposal choice; native, rights, uncertainty and final acceptance remain open.':'The method is a reference candidate; execution, reuse rights and the validity of uncertainty estimates still require investigation.',
      'Native, visual, independent and final acceptance remain open.':'Execution and independent validation remain outstanding.',
      'The reference decision grants no native capability; independent, visual and final acceptance remain open.':'The source comparison does not establish an executed integration; independent validation is still needed.',
      'The reference decision gives no native, causal or enterprise acceptance; independent, visual and final acceptance remain open.':'The source comparison does not establish an executed causal integration or suitability for enterprise use; independent validation is still needed.',
      'Official provenance, complete rights, native implementation, independent review, current support, actual costs, visual and final acceptance remain open':'Official provenance, applicable rights, execution, independent review, current support and actual costs remain unresolved',
      'Independent, visual and final acceptance remain open.':'Independent validation remains outstanding.',
      'Authentic official identity and terms, native fixtures, complete surface coverage, independent review, visual and final acceptance remain open':'Official source identity and terms, executable comparisons, complete capability coverage and independent review remain unresolved',
      'The selected preprint inspection therefore advances the frontier survey while retaining final-version, native, bank, visual and independent acceptance limits.':'The selected preprint supports this comparison; the final version, package execution, independent validation and applicability to banking still require evidence.',
    }
    for old,new in boilerplate.items():
        if re.search(r'\s+'.join(re.escape(x) for x in old.split()),text):
            swap(old,new,'Remove repeated authoring status; retain scientific and implementation limits')
    if rel=='program/public-data-v15/survey.tex':
        start=text.index('The immediate deliverable is a product proposal:')
        end=text.index('\n\nPublic data can provide',start)
        old=text[start:end]
        swap(old,'A bank should invest in a causal-analysis service only when there is a\ncredible account of the decisions it could improve, the methods worth\nassembling and the experiments worth funding. Public evidence can establish\ntechnical promise and identify consequential uncertainties before a bank\npays to collect private assignment histories or commission a larger trial.\nThe proposed studies follow that investment sequence.')
        start=text.index('The three major manuscript repairs remain obligations:')
        end=text.index('\n\nLater bank qualification',start)
        swap(text[start:end],'Public evidence informs three choices: which existing methods to reuse,\nwhere language assistance is useful, and how analysts should conduct a\nreproducible study. A dataset can reveal a timing error or support a\ncontrolled comparison without settling every question about those choices.',
             'Remove internal manuscript obligations; retain scientific scope')
        start=text.index('Proposal acceptance means the scholarly argument is coherent,')
        end=text.index('\n\nPublic evidence informs',start)
        swap(text[start:end],'The investment decision requires a comparison of feasible alternatives,\ntheir costs and the evidence for their expected benefits. Reproducible\npublic and simulated studies can support that comparison within their\nstated assumptions. A restricted result may justify a narrow prototype\nwhile leaving broader research questions unresolved.')
        if 'The proposal therefore replaces a premature demand' in text:
            start=text.index('The proposal therefore replaces a premature demand')
            end=text.index('\n\n',start)
            old=text[start:end]
            # Retain the source paragraph's scientific qualification after removing history.
            swap(old,'Public studies can establish technical merit and identify a worthwhile\nnext experiment without estimating the effect of a policy in the adopting\nbank. An effect measured in another population is not the bank\'s effect.\nA negative comparison, an informative finding of nonidentification, or a\nnarrower useful capability can still improve the investment decision.',
                 'Replace retrospective programme framing with the role of public evidence')
    if rel.endswith('integrated-reader/chapters/weak_audit_projection.tex'):
        swap('The V10 funding interval refuses inference','The regular funding interval cannot support inference')
        swap('This supplement\ntests a different reporting design:','An alternative reporting design uses')
        swap('The frozen V10 monograph is unchanged;\nthis is an author-reviewed research supplement, not an implemented product.',
             'These findings concern constructed funding studies; their usefulness for a\nbank depends on the validity of the assumptions and the precision it needs.')
        swap('These are prospective designs, not results of this supplement.',
             'These alternatives require separate evaluation.')
    if rel.endswith('integrated-reader/chapters/weak_audit_sharpening.tex'):
        swap('The first weak-audit supplement retained rank ambiguity but produced broad\nfunding-value sets. This follow-up uses shared information in the two observed',
             'Separate response bands retain uncertainty about customer identity but can\nproduce broad funding-value sets. Shared information in the two observed')
        swap('candidate responses, forming average and difference scores before covariance\nestimation.',
             'candidate responses can narrow those sets by forming average and difference\nscores before covariance estimation.')
        swap('This is an\nauthor-reviewed research follow-up, not a bank-calibrated product.',
             'The study uses synthetic populations; performance for a particular bank\nrequires evidence about its assignment and observation processes.')
        swap('those in the preceding supplement.','those in Chapter~\\ref{integrated:weak_audit_projection}.')
        swap('The first supplement constructed four separate bands for the candidate\nresponses.','The separate-band method constructed four bands for the candidate\nresponses.')
        swap('This follow-up transforms','The alternative transforms')
        old='The frozen V10 monograph and first supplement retain their\nown identities. This follow-up is appended to a single reader PDF for\nconvenience; that assembly is not a claim of independent scientific approval\nor production readiness.'
        if old in text: swap(old,'Independent scientific review and bank validation remain necessary\nbefore adopting the method in a particular institution.')
        else:
            start=text.find('The frozen V10 monograph and first supplement')
            if start>=0:
                end=text.find('\n\n',start)
                if end<0:end=len(text)
                swap(text[start:end],'Independent scientific review and bank validation remain necessary\nbefore adopting the method in a particular institution.')
    if rel=='reconstruction/18_product.tex':
        old='The bank\'s recurring difficulty is that an analysis crosses several\nscientific representations.'
        swap(old,'A banking study must connect a business choice with a financial consequence\nthrough a defensible account of customer behaviour and observed data.')
        swap('built around the same scientific objects.','built around the same definitions of populations, interventions and outcomes.')
    if rel=='reconstruction/21_investment.tex':
        start=text.index('The proposed product owns repeated semantic work:')
        end=text.index('\n\nComparator costs',start)
        swap(text[start:end],'The proposed service would help analysts reconstruct what was known when\na decision was made, keep the population and outcome consistent, document\nwhy an effect is identified, and carry uncertainty into the financial\ncomparison. It would reuse existing numerical methods where their\nassumptions fit. Each business would still specify its products, costs and\nconstraints. A mortgage policy, an individual collections decision and a\nmacroeconomic shock need not share the same economic quantity of interest.')
    if rel=='reconstruction/07_time_series.tex':
        swap('The next chapter develops what causal discovery can contribute before\nthose restrictions are promoted into a fitted effect model.',
             'Chapter~\\ref{r3:discovery} examines what causal discovery can contribute\nbefore those restrictions are used to estimate an effect.',
             'Repair forward navigation after thematic reordering')
    if rel=='reconstruction/08_discovery.tex':
        swap("Chapter~\\ref{r3:graph-construction}'s construction of\nnodes, clocks and interventions precedes the statistical search.",
             'The variables, information dates and interventions in\nSection~\\ref{r3:graph-construction} must be defined before the statistical search.')
    if rel=='reconstruction/13_transport.tex':
        swap('A shared library can reproduce an estimator in another repository\nwithout making its original causal answer valid in another market.',
             'An estimate that is credible in one market may be misleading in another,\neven when the same statistical method is applied correctly.')
    if rel=='program/execution/2026-10-13/live-evaluation/evaluation.tex':
        swap('Final acceptance must jointly constrain useful resolution, availability, critical\nerrors and cost;',
             'An evaluation must consider useful answers, availability, critical\nerrors and cost together;')
    if rel=='program/execution/2026-10-19/census-retrieval-selfcorrection-v1/development.tex':
        swap('a final acceptance set','an independent evaluation set')
        swap('an independently specified final acceptance oracle','an independently specified reference answer for evaluation')
    if rel=='reconstruction/19_execution.tex':
        start=text.index('The mathematical operations of Chapter~')
        end=text.index('\n\n',start)
        swap(text[start:end],'An economist studying a bank policy needs to reconstruct what customers\nand decision makers knew at the time. Chapter~\\ref{r3:product} defines the\ncomparison; the data must preserve it through reporting delays, corrections\nand changes in customer identity. The same population, action and outcome\nshould be analysed whether the study runs in a research notebook, a scheduled\ncommand or an analytical application.')
    if rel=='program/repair-v12/work/LA07/frontier-chapter.tex':
        swap('The useful\nstarting point for evaluating language assistance is therefore the object\nbeing produced:',
             'Evaluating assistance therefore starts by distinguishing the task:')
        swap('Success at one object supplies no automatic guarantee for the\nothers.',
             'Success on one task does not establish success on the others.')
    if rel=='program/execution/2026-10-16/reporting-monitoring/development-v2.tex':
        swap('Reporting joins the earlier formulation, identification, estimation and artifact\ncontracts.',
             'The report brings together the economic question, the identification\nargument, the estimate and the evidence needed to reproduce it.')
    if rel=='program/execution/2026-10-17/s8/publication-v3/chapter.tex':
        swap('record linkage and missingness analysis from the preceding chapter',
             'the record-linkage and missing-data methods considered earlier',
             'Remove stale adjacency reference after reordering')
    if rel.endswith('weak_audit_sharpening.tex'):
        pattern=re.compile(r'The frozen V10\s+monograph.*?production readiness\.',re.S)
        m=pattern.search(text)
        if m:swap(m.group(0),'Bank use still requires independent review and evidence that the\nmethod applies to the institution and decision being considered.',
                  'Remove internal publication history; retain application limits')
        swap("It does not close D09's useful-precision gap:",
             'Its precision may still be inadequate for a financial decision:')
        swap('a separate D04/D09 limit','a separate identification limit')
    if rel.endswith('weak_audit_projection.tex'):
        start=text.index('The next scientific D09 step is')
        end=text.index('\n\n',start) if '\n\n' in text[start:] else len(text)
        swap(text[start:end],'A useful next study would derive a precision improvement before\nevaluating it on fresh data, including small audits, weak identification,\npersistence and violations of the assumed law. Bank use would also require\ncredible histories and audit labels, an economically meaningful precision\nthreshold, measured costs and operating evidence. The local experiment\nestablishes neither an adopted service nor institutional savings.',
             'Replace internal gap codes with the economic and statistical requirements')
    if rel.endswith('linked_funding.tex'):
        start=text.index('The frozen monograph and two prior supplements')
        end=text.index('The literature cutoff',start)
        swap(text[start:end],'The experiment preserves its specification, code, completed results\nand the failed partial run. These records distinguish the reported evidence\nfrom unperformed work. ',
             'Remove delivery machinery and preserve reproducibility and failure disclosure')
        start=text.index("The local advance concerns D01/D09's")
        end=text.index('\n\n',start)
        swap(text[start:end],'Resolving the actual customer history supplies information that\ncorrectness counts alone can miss. Finite intervals at exact identity rank\none are demonstrated for the specified funding model; their calibration and\nuseful precision for a bank remain uncertain. Valid assignment, known audit\ninclusion and accurate labels are essential. Independent origin audits do\nnot establish inference under arbitrary persistence of customer identity and\ncalendar shocks. Nonlinear policies, temporal graphs and other learners\nrequire their own arguments. Bank adoption also needs independent review,\nrelevant operating trials and measured costs.',
             'Replace internal gap codes while preserving all substantive limits')
    if rel=='program/execution/2026-10-28/attention-protocol-reader-v2/development.tex':
        start=text.index('This supplemental trace sharpens reuse decisions')
        end=text.index('\n\n',start) if '\n\n' in text[start:] else len(text)
        swap(text[start:end],'TCDF is a candidate for a comparison of temporal methods, subject to\ntests of its observation windows, padding and delay conversion. TACD addresses\nevent and topology information: results using a supplied graph must be\ndistinguished from results where the graph is unknown, and its four selected\nprofiles share their training and validation pairs. A recommendation to deploy\neither method needs a reproducible installation, applicable reuse rights and\na public comparison with known causal structure. The present evidence supports\nthese narrower comparisons, rather than general adoption.')
    if rel=='program/execution/2026-10-13/commercial-heterogeneity/master-execution-preserving.tex':
        swap('This extension connects funding response, sequential servicing, temporal graph effects and audited observations.',
             'Funding responses, sequential servicing, temporal relationships and verified customer histories reveal different limits on that information.')
        swap('These are author-reviewed research findings; independent review, bank truth, operating acceptance and economics remain separate gates.',
             'These are research findings from specified experiments. Their use in a bank requires independent review, credible assignment and observation information, suitable operating performance and a defensible economic case.')
        start=text.index('The standard is a connected argument')
        end=text.index('\n\nEvery table cell',start)
        swap(text[start:end],'The experiments ask whether changing the available information improves\na stated banking comparison. A negative result can explain which information\nis missing. An uncertainty set can be statistically defensible yet too wide\nto distinguish a profitable action from a loss. Scientific validity and\nuseful precision therefore need separate attention.',
             'Replace author-completion gates and reference-book history with the scientific question')
        start=text.index('D01 has a scoped added-identity route;')
        end=text.index('\n\n',start)
        swap(text[start:end],'Verified customer histories provide a restricted way to learn funding\nresponses, and the nonlinear servicing study supports one specified policy\ncomparison. Several causal graphs can still fit the same observations.\nAssignment, audit inclusion and label accuracy require substantive evidence.\nJoint dependence and high-dimensional learning retain adverse findings, while\nlocal computing results do not establish bank operating performance. Useful\nprecision and the full financial case depend on the institution and decision.',
             'Translate internal gap identifiers into substantive unresolved questions')
        start=text.find('Seven input groups remain:')
        if start>=0:
            end=text.find('\n\n',start)
            if end<0:end=len(text)
            swap(text[start:end],'A bank study would need the relevant decision makers and data owners\nto establish assignment rules, observation quality, required precision and\ncosts. The information requested should be specific to the proposed study.',
                 'Remove internal input-group administration')
        start=text.find('This extension is combined with the preserved 259-page predecessor')
        if start>=0:
            end=text.find('\n\n',start)
            if end<0:end=len(text)
            swap(text[start:end],'The selected experiments establish both useful information designs\nand adverse findings. They motivate a restricted prototype; they do not\nestablish performance or financial returns for an adopting bank.',
                 'Replace publication history with interpretation of results')
    if rel.endswith('weak_audit_projection.tex'):
        start=text.index('The registered plan, pre-execution challenge, code, fixed specification,')
        swap(text[start:],'The projection formula, bounded-memory implementation and synthetic\nfindings are project work. The cited sources support the specific technical\nsteps identified in the text; neither is presented as proving the new\nconstruction. The study specification, code and complete results are retained\nwith the research materials. The literature cutoff is 7 October 2026.\n',
             'Move repository-path and receipt administration out of reader prose')
    if rel.endswith('weak_audit_sharpening.tex'):
        start=text.index('The two inherited scholarly roles above use the genuine named PDFs,')
        swap(text[start:],'The transformation, repaired numerical check, observational example,\nregistered study and financial interpretation are project contributions.\nThe cited sources support only the technical results attributed to them.\nThe original failed run and the repaired comparison remain available with\nthe specification and code. The literature cutoff is 7 October 2026.\n',
             'Preserve attribution and failed evidence without manifest machinery')
    return text


def prepare():
    OUT.mkdir(exist_ok=True)
    (OUT/'sources').mkdir(exist_ok=True)
    original=read(OLD)
    body=original.split(B+'mainmatter',1)[1].split(B+'backmatter',1)[0]
    items=[resolve(x) for x in INPUT.findall(body)]
    assert len(items)==328,len(items)
    sources={}
    def collect(path):
        if path in sources:return
        text=read(path);sources[path]=text
        for name in INPUT.findall(text):
            child=resolve(name)
            if not child.exists():raise ValueError('Missing input '+name)
            collect(child)
    for p in items:collect(p)
    mapping={p:OUT/'sources'/('s_'+sha256(str(p.relative_to(DOCS)).encode()).hexdigest()[:14]+'.tex') for p in sources}
    records=[]
    for path,text in sources.items():
        revised=edits(path,text)
        def linked(m):
            return B+'input{'+str(mapping[resolve(m.group(1))].relative_to(DOCS))+'}'
        revised=INPUT.sub(linked,revised)
        mapping[path].write_text(revised)
        records.append(dict(original=str(path.relative_to(ROOT)),original_sha256=sha256(text.encode()).hexdigest(),
                            reading_copy=str(mapping[path].relative_to(ROOT)),reading_sha256=sha256(revised.encode()).hexdigest()))
    def inc(i):return B+'input{'+str(mapping[items[i]].relative_to(DOCS))+'}\n'
    used=[]; chunks=[]
    def take(*indices):
        for i in indices:
            if i in used:raise ValueError('Repeated section '+str(i))
            used.append(i);chunks.append(inc(i))
    def chapter(title,intro=''):
        chunks.append(B+'chapter{'+title+'}\n'+intro+'\n\n')
    def part(title,label,intro):
        chunks.append(B+'part{'+title+'}\n'+B+'label{reading:part-'+label+'}\n'+intro+'\n\n')
    def split_chapters(index):
        path=mapping[items[index]]; text=read(path)
        if index==327:
            pieces=re.split(r'(?=\\hypertarget\{pd15:(?:evidence|datasets|portfolio|investment)\})',text)
            pieces=[p for p in pieces if p.strip()]
            if len(pieces)!=4:
                # The original portfolio anchor is profile-specific; use chapter starts and retain wrappers.
                positions=[m.start() for m in re.finditer(r'\\hypertarget\{[^}]+\}\{%\s*\\chapter',text)]
                pieces=[text[a:b] for a,b in zip(positions,positions[1:]+[len(text)])]
        else:
            pieces=re.split(r'(?=\\chapter\{)',text)
            pieces=[p for p in pieces if p.strip()]
        paths=[]
        for n,piece in enumerate(pieces):
            target=OUT/'sources'/('split_'+str(index)+'_'+str(n)+'.tex');target.write_text(piece);paths.append(target)
        return paths
    split93=split_chapters(93);assert len(split93)==5
    split327=split_chapters(327);assert len(split327)==4
    splits_used={93:[],327:[]}
    def split_take(index,n):
        splits_used[index].append(n)
        chunks.append(B+'input{'+str((split93 if index==93 else split327)[n].relative_to(DOCS))+'}\n')

    part('The banking decision and the causal question','decision',
         'A bank earns a return by changing a decision, not by observing a correlation.\nThe first task is to define the action, the alternative and the financial outcome.\nIdentification then determines what the data and assumptions can reveal;\nestimation measures that quantity and its uncertainty.')
    chunks.append(B+'input{reading-edition/banking-decision}\n')
    take(0,1,2,3)
    part('Customers and institutions through time','time',
         'A decision changes the information available for the next one. Repeated\ncontacts, loan modifications and deposit offers therefore require a comparison\nof policies over time. Panel and time-series designs add the common shocks\nand selection problems faced by banks changing policy across branches or dates.')
    take(4,5,6,7,8,11,12)
    part('What the observations leave uncertain','uncertainty',
         'A large dataset can leave the causal question unresolved. Several mechanisms\nmay explain the same correlations, customer histories may be linked incorrectly,\nand a result from one population may fail in another. These limits determine\nwhich assumptions to defend and which additional information to seek.')
    take(9,10,13,14,15)
    part('Choosing methods for discovery and identification','methods',
         'Software is useful when its methods answer the economic question under\ncredible assumptions. The comparisons begin with the relationships that a\nmethod can discover and the effects it can identify. They distinguish a supplied\ncausal model from one learned from data and compare alternatives across languages.')
    take(16,17,18);split_take(93,0)
    take(19,20,21,94,95,96)
    chapter('Learning a causal model from observational data',
            'A discovery method can narrow the plausible economic relationships without\nsettling the effect of a proposed action. The comparisons here examine what\nchanges when the variables are continuous, relationships are nonlinear, or\nimportant customer circumstances are unobserved. The practical choice depends\non those assumptions as well as the computation.')
    take(97,98,100,101,102,104,105,106,107,186,200)
    chapter('From a learned graph to a defensible calculation',
            'A graph becomes useful to a bank when its statistical meaning survives\nthe next calculation. Directed, partially directed and mixed graphs encode\ndifferent information. The following comparisons ask which calculations each\nrepresentation supports and what is lost when a model passes between tools.')
    take(203,204,205,206,207,208)
    chapter('Learning relationships over time')
    take(113,114,115,116,117,118,44,45,46,47,48,49,55)
    take(22,23,56,57,58,59,60,91,199,202,128,131)
    part('Estimating effects and comparing existing tools','effects',
         'An identified effect still needs an estimator, a suitable comparison group\nand a defensible account of uncertainty. The choice differs for an invitation,\nan eligibility threshold, a repeated servicing rule and a branch rollout.\nCommercial and open-source alternatives are assessed against those distinctions.')
    take(61,62,66,70,71,72,73,74,75,99,176,190,201,270)
    chapter('Instruments, eligibility thresholds and the population affected',
            'An invitation or eligibility rule can create a useful comparison even\nwhen customers choose whether to participate. The effect for customers whose\nbehaviour changes at that margin need not equal the effect for every customer.\nSoftware choices must respect the instrument, cutoff and population that\nsupply the identifying information.')
    take(63,64,65,123,127,150,151)
    split_take(93,1)
    chapter('Channels, doses and sensitivity to assumptions')
    take(24,25,26,27,28,29,187,188,271,273)
    take(76,77,78,79,165,178,179,180,181,129);split_take(93,2)
    chapter('Choosing repeated actions')
    take(103,182,183,184,185,189,275,276,277,278)
    take(80,50,51,52,67,68,69,177,191,192,193,198,220,221)
    chapter('How much confidence should a rollout comparison command?',
            'Branch and customer weights determine whose benefit is being measured;\ncommon shocks determine how much independent information the study contains.\nReported uncertainty must reflect both. The calculations examine changes in\nweights, covariance and trend assumptions before interpreting an event-study\ncoefficient as a reliable financial comparison.')
    take(53,54,90)
    chapter('Synthetic controls and the choice of a comparison',
            'When one region or institution changes policy, a weighted combination\nof unaffected units may offer a comparison. Its usefulness depends on donor\ninformation, pre-intervention fit and the assumptions linking that fit to the\nuntreated future. The methods differ in how they extrapolate and how they\nrepresent uncertainty; those differences matter for the bank\'s decision.')
    take(88,89,146,147,148,149,194,195,196,197);split_take(93,3)
    chapter('Dynamic panels and structural funding shocks',
            'A deposit response evolves over time and may coincide with changes in\nmonetary conditions or customer demand. Dynamic-panel moments, restrictions\non structural shocks and state-space forecasts use different sources of\ninformation. A forecast alone does not establish the effect of changing the\nbank\'s policy.')
    take(152,153,154,155,156,225)
    take(81,30,31,32,33,34,82,86)
    chapter('Hidden states and Bayesian comparisons')
    take(35,84,87,279,280)
    take(130,85,157,158,159,160,161,218,132)
    take(83,108,109,110,111,112,119,120,121,122,124,125,126,209,210,211,212,213,144,145)
    take(92,136,143)
    chunks.append(B+'input{reading-edition/software-conclusions}\n')
    part('Language models as research assistants','language',
         'A useful assistant must help an economist ask a better question or examine\nits evidence. Fluency is a different achievement. The discussion follows the\nresearch task from business formulation and measurement to causal diagrams,\ndiscovery, estimation and interpretation, before examining performance and cost.')
    take(226,227,171,228,229,230,231,232,272,233,234,235,236,237,39,40,41,219,238,174,239,240,241,
         242,243,244,245,246,247,248,249,250,251,252,253,254,255,256,257,258,259,260,261,262,
         42,43,167,168,169,170,172,173,175,214,217)
    split_take(93,4)
    take(263,264,37,38,166,216,265,266,267,268,269,274)
    chapter('Comparing assistance with credible alternatives',
            'An assistant should be judged against the work an analyst could already\ndo. Evaluation therefore needs simple baselines, tasks with defensible answers,\nand a record of unresolved cases and correction costs. The following studies\nask what benchmarks, retrieval, code generation and simulated populations can\nestablish about that comparison.')
    take(281,282,283,284,285,286,287,288,289,290,291)
    chunks.append(B+'input{reading-edition/assistance-conclusions}\n')
    part('Putting a banking study into practice','practice',
         'The analyst should be able to follow the same study from source records\nto the financial conclusion. A research library, a command-line tool and an\nassistant using the Model Context Protocol are alternative ways to conduct that\nstudy. Their design follows from the population, timing, intervention and\nuncertainty established in the preceding parts.')
    take(293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,309,310,215,
         133,134,135,36,162,163,164,222,224)
    chapter('Running and comparing analytical studies')
    take(137,138,139,140,141,142,223)
    part('Public evidence and banking studies','evidence',
         'Public observations expose real measurement problems; controlled\nexperiments reveal errors when the causal truth is known. Neither replaces\nthe other. The studies compare useful quantities, preserve adverse results,\nand ask whether another measurement changes the decision more than another\nmethod applied to the same records.')
    split_take(327,0);split_take(327,1);split_take(327,2)
    take(311,312,313,314,315,316,317,318,319,320,321,322,323,324,325)
    part('The investment decision','investment',
         'The alternative to a shared service is a capable team using established\nmethods. The investment case must compare the quality and full cost of\nequivalent studies, including negative findings. Better information is worth\nbuying when it can change a consequential decision by more than it costs.')
    take(292,326);split_take(327,3)
    assert set(used)==set(range(328))-{93,327}, sorted(set(range(328))-set(used)-{93,327})
    assert splits_used=={93:list(range(5)),327:list(range(4))}
    prefix=original.split(B+'title{',1)[0]
    prefix+=r'''\title{\sffamily\bfseries\color{ink}Causal Inference for Banking\\[14pt]
\Large Decisions, evidence and the case for a shared analytical service}
\author{Research monograph and product proposal}
\date{29 October 2026\\Literature cutoff: 7 October 2026}
\setcounter{tocdepth}{0}
\hypersetup{pdftitle={Causal Inference for Banking: Decisions, Evidence and Investment}}
\begin{document}
\frontmatter
\maketitle
\input{reading-edition/opening}
\begingroup\setlength{\parskip}{0pt}\tableofcontents\endgroup
\mainmatter
'''
    suffix=B+'backmatter'+original.split(B+'backmatter',1)[1]
    DRIVER.write_text(prefix+''.join(chunks)+suffix)
    # Compare the manuscript bodies, excluding the intentionally replaced front matter.
    def signatures(text):
        citations=Counter()
        for m in re.finditer(r'\\cite\w*\*?(?:\[[^\]]*\])*\{([^}]+)\}',text):
            citations.update(k.strip() for k in m.group(1).split(','))
        equations=Counter(re.findall(r'\\begin\{((?:equation|align|gather|multline|eqnarray)\*?)\}',text))
        labels=Counter(re.findall(r'\\label\{([^}]+)\}',text))
        math=Counter(re.findall(r'(?s)(\\\[.*?\\\]|\\begin\{(?:equation|align|gather|multline|eqnarray)\*?\}.*?\\end\{(?:equation|align|gather|multline|eqnarray)\*?\})',text))
        return citations,equations,labels,math
    before=signatures('\n'.join(sources.values()))
    after=signatures('\n'.join(read(mapping[p]) for p in sources))
    comparison=dict(citation_occurrences_preserved=before[0]==after[0],equation_environments_preserved=before[1]==after[1],
                    labels_preserved=before[2]==after[2],displayed_math_preserved=before[3]==after[3],
                    source_files=len(sources),top_level_inputs=len(items),
                    unique_citation_keys=len(before[0]),citation_occurrences=sum(before[0].values()),
                    displayed_math_blocks=sum(before[3].values()),parts=9,
                    original_frontmatter='Replaced accumulated change history with economic introduction; preserved predecessor remains available',
                    prose_review='Targeted repairs; not a certification that every paragraph meets the desired voice',
                    final_visual_acceptance=False)
    assert all(comparison[k] for k in ['citation_occurrences_preserved','equation_environments_preserved','labels_preserved','displayed_math_preserved']),comparison
    (OUT/'source-map.json').write_text(json.dumps(records,indent=2)+'\n')
    (OUT/'editorial-changes.json').write_text(json.dumps(EDIT_LOG,indent=2)+'\n')
    (OUT/'content-comparison.json').write_text(json.dumps(comparison,indent=2)+'\n')
    (OUT/'reading-order.json').write_text(json.dumps(dict(order=used,split_inputs=splits_used),indent=2)+'\n')
    print(json.dumps(comparison))


def build():
    dest=OUT/'build';dest.mkdir(exist_ok=True)
    commands=[['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
               '-output-directory='+str(dest),DRIVER.name],
              ['bibtex',str((dest/DRIVER.stem).relative_to(DOCS))],
              ['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
               '-output-directory='+str(dest),DRIVER.name],
              ['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',
               '-output-directory='+str(dest),DRIVER.name]]
    records=[]
    for i,cmd in enumerate(commands):
        start=time.monotonic();log=dest/('pass-'+str(i+1)+'.log')
        with log.open('w') as f:
            result=subprocess.run(cmd,cwd=DOCS,stdout=f,stderr=subprocess.STDOUT,timeout=180)
        records.append(dict(command=cmd,exit_code=result.returncode,seconds=round(time.monotonic()-start,2),log=str(log.relative_to(ROOT))))
        (OUT/'build-results.json').write_text(json.dumps(records,indent=2)+'\n')
        print(json.dumps(records[-1]),flush=True)
        if result.returncode:
            print('\n'.join(log.read_text(errors='replace').splitlines()[-35:]),flush=True)
            raise SystemExit(result.returncode)
    pdf=dest/(DRIVER.stem+'.pdf')
    DRIVER.with_suffix('.pdf').write_bytes(pdf.read_bytes())
    print('PDF: '+str(DRIVER.with_suffix('.pdf').relative_to(ROOT)),flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['prepare','build'])
    args=parser.parse_args()
    prepare() if args.command=='prepare' else build()
