"""Record reviewed energy study and preserve concurrent release work."""
from pathlib import Path
import datetime,hashlib,json,shutil
R=Path(__file__).resolve().parents[1];O=R/'docs/twelve-hour-closure/2026-10-29'
def read(p):return json.loads(p.read_text())
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def art(p):return dict(path=str(p.relative_to(R)),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def main():
    now=datetime.datetime.now(datetime.timezone.utc).isoformat()
    v=read(O/'energy-publication/revision-2/publication-1/verification.json');assert v['status']=='pass'
    p=O/'energy-author-review.json';assert not p.exists()
    review=dict(created_utc=now,status='pass_with_limits',scope='Author review only;not independent scientific or whole-book acceptance',
      publications=v['publications'],section='100.14',section_pdf_pages=list(range(1816,1822)),
      sources=art(O/'energy-source-support.json'),scoring=art(O/'energy-scoring-review.json'),
      experiment=art(O/'energy-study-attempt-1/result.json'),independent_check=art(O/'energy-study-attempt-1/independent-check.json'),
      mathematics=['Trapezoidal rational arithmetic andmeasurement boundaries','Poissonbatchmeanandvariancefromweightedgaps',
       'Ratioofaverages,positiveacceptanceandenergyconditions','Financialbreak-evenwithwhole-attemptcostandnoinventedprices'],
      visual=dict(short_pages=list(range(1,9)),integrated_pages=list(range(1815,1823)),
       method='Allv1short8andaffectedintegrated8pagesviewed;v2allbutshort6/integrated1820pixel-identical,changedpagesviewedseparately.',
       identity=art(O/'energy-visual/revision-2/image-comparison.json'),findings='Readable equations,tables,figure,citationsandentry/exit;noobservedclippingoroverlap.'),
      preservation=dict(inherited_files=506,inherited_inputs=464,changed_inherited_files=[]),
      repairs=['Explicit e_A>0 added before taking energy ratio;v1PDFpreserved.',
        'Default andminiforge Python lackedfitz;usedexistingPopplerforrendering.',
        'One malformedregex andthree incompleteJStransportcalls producednoedits;correctedandretried.'],
      limits=['900000generatedbatchesnotbanktraffic.','Syntheticpowertraceisnotmeasuredenergy.',
        'Staticdefectandprepublicationfileidentitydonotproveexactpublishedexecution.',
        'Comparatorquarantinedforjointqualityrankings;actualnativequalificationrequirespreservedoutputs.',
        'Noenergyprice,modelcost,staffprice,carbonorROIestimate.'])
    save(p,review)
    ip=R/'docs/scientific-gap-closure/2026-10-29/remaining-inventory.json';d=read(ip)
    backup=O/'inventory-before-energy.json';assert not backup.exists();shutil.copyfile(ip,backup)
    old=[x for x in d['frontier_unread']if x['id']=='LA01-candidate-218'];assert len(old)==1
    d['frontier_unread']=[x for x in d['frontier_unread']if x['id']!='LA01-candidate-218']
    counts=dict(d['current_frontier_counts']);assert counts['inspected']==90 and counts['unread']==23
    counts.update(inspected=91,retained_with_limits=90,unread=22,basis='docs/twelve-hour-closure/2026-10-29/energy-source-support.json',
       meaning='91 original-census dispositions:90retainedwithlimits,onequarantined. Separateenergycomparatoralsoquarantined;notaddedtothe113-candidatecensus.')
    d['current_frontier_counts']=counts
    d['energy_followup']=dict(source='LA01-candidate-218',prior_unread_record=old[0],disposition='retained_with_limits',
      source_support=str((O/'energy-source-support.json').relative_to(R)),review=str(p.relative_to(R)),publication=v['publications']['full'],
      separate_comparator='Husom2025accuracy/jointrankingsquarantinedpendingreconstruction;doesnotalteroriginalcensusdenominator.')
    save(ip,d)
    pp=R/'docs/program/scientific-priorities.json';s=read(pp);a=s['active_twelve_hour_campaign']
    a.update(last_completed='Energyperusefulcausalstudy:exactmeasurementcounterexample,900000generatedbatches,and164-testscoringauditintegrated',
      last_evidence=str(p.relative_to(R)),reader=v['publications']['full'],short_study=v['publications']['short'],
      next='Investigate partial recovery: bounds when second-stage follow-up fails;keep consequential source/software comparisons independent.')
    save(pp,s)
    cp=O/'checkpoint.json';c=read(cp);c.update(updated_utc=now,publications=v['publications'],counts=counts,last_completed=a['last_completed'],next=a['next'])
    c['do_not_repeat'].append('Completed energy study:900000Poissonbatches,exacttrace,164staticbenchmarktests;no native model/sensor run.')
    save(cp,c)
    mp=R/'docs/program/master-live.md';text=mp.read_text();start=text.index('<!-- financing-continuation:start -->');end=text.index('<!-- financing-continuation:end -->')+len('<!-- financing-continuation:end -->')
    block='''<!-- financing-continuation:start -->
## Scientific continuation: information, uncertainty and decision value

[Integrated scientific reader](../causal_banking_closure_integrated_v15_2026-10-30.pdf) · [Eight-page cost study](../causal_banking_useful_answer_cost_v2_2026-10-30.pdf) · [Recovery study](../causal_banking_outcome_recovery_v3_2026-10-30.pdf) · [Evidence](../twelve-hour-closure/2026-10-29/README.md).

The 1,916-page scientific reader preserves the batch015 lineage and all completed financing, discovery, text-signal, graph-confidence and missing-history recovery additions. Section100.14 (PDF1816–1821) now distinguishes energy per token from whole-study expense per independently useful answer. An exact synthetic trace exposes an idle-gap integration defect in a pinned measurement tool;900,000 generated batches verify the delay price of count batching. A separate comparator's164stored programming tests define but do not call their assertions. The scorer and task data are identical in a prepublication revision. Its accuracy and joint energy-quality rankings are quarantined pending exact reconstruction,without claiming all its measurements false.

The eight-page study and integrated pages1815–1822 have source-bound author review and visual inspection. All506 inherited files and464 input occurrences remain unchanged;references,layout andall-page text bounds pass. Frontier coverage is91inspected original-census dispositions:90retained with limits,onequarantined,and22unread. The additional comparator quarantine is separate from that census. Native qualification,actual energy and prices,independent acceptance andbank validation remain later obligations. Next: investigate bounds when randomly requested recovery is not completed. Concurrent release work retains its own lineage. This campaign remains active through30October2026,11:00:01Asia/Shanghai.
<!-- financing-continuation:end -->'''
    mp.write_text(text[:start]+block+text[end:])
    rp=O/'README.md';old=rp.read_text();rp.write_text('''## Latest scientific delivery: the cost of a useful answer

Scientific reader: docs/causal_banking_closure_integrated_v15_2026-10-30.pdf (1,916pages). Focused reading: docs/causal_banking_useful_answer_cost_v2_2026-10-30.pdf (eightpages). Section100.14,PDF1816–1821,contains exactmeasurement,arrival-delay andwhole-studyquality calculations,plus a source-bound benchmark-scoring exclusion. See energy-author-review.json,energy-source-support.json,energy-scoring-review.json andenergy-study-attempt-1/. This is proposal evidence,not measured bank energy orqualifiednativeintegration.

'''+old)
    print(json.dumps(dict(status='active',publications=v['publications'],counts=counts,review=str(p.relative_to(R)))))
if __name__=='__main__':main()
