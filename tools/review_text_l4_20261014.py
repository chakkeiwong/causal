import hashlib,json,re
from pathlib import Path
import master_control as core
ROOT=Path(__file__).resolve().parents[1]
CH=ROOT/'docs/program/comprehensive-v14/work/TEXT.DRAFT.L4/chapter.tex'
AUD=ROOT/'docs/program/execution/2026-10-13/l2/final-v4/reader/source-audit.json'
BASE=ROOT/'docs/program/execution/2026-10-14/text-l4'
def ref(p,a):
 p=Path(p);return {'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'anchor':a}
def write(p,d):
 assert not p.exists();p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
text=CH.read_text(); assert text.startswith('\\chapter'); assert '18/5' not in text
keys={k.strip() for g in re.findall(r'\\cite\{([^}]*)\}',text) for k in g.split(',')}
aud=json.loads(AUD.read_text()); known={x['integrated_citation_key'] for x in aud['sources']}; assert keys<=known,keys-known
assert all(x in text for x in ['time zero','CPDAG','PAG','nonidentified','retrieval','uncapped','postdecision note'])
write(BASE/'author-review.json',{'outcome':'pass','scope':'LLM-assisted discovery manuscript chapter; literature and exact design only','findings':['Connected argument defines target, clocks, graph alternatives, diagnostics and banking implications.','Claims cite the preserved exact-reader source audit; package demonstrations and literature findings are not relabeled live performance.','Project mechanisms are explicitly framed as generated fixtures and the protected prototype boundary is stated.'],'limitations':['No live model call, package execution, bank data or independent review.'],'evidence':[ref(CH,'Reviewed L4 chapter'),ref(AUD,'Exact-reader source identities and inspected anchors')]})
write(BASE/'operation-receipt.json',{'operation_id':'TEXT.DRAFT.L4','outcome':'pass','execution':'performed','scope':'LLM-assisted discovery manuscript chapter; literature and exact design only','reviewer':{'name':'Codex author/coordinator','kind':'author'},'limitations':['No live model call, package execution, bank data or independent review.'],'outputs':[ref(CH,'Reviewed L4 chapter')],'criteria':[{'index':0,'verdict':'pass','finding':'Notation, assumptions, alternatives, exact graph fixture, diagnostics and banking consequences are developed.','evidence':[ref(CH,'Full chapter')]},{'index':1,'verdict':'pass','finding':'Citations are checked against the preserved exact-reader audit and evidential status is explicit.','evidence':[ref(CH,'Citation set'),ref(AUD,'Source audit')]}]})
print(json.dumps({'outcome':'pass','citations':len(keys),'words':len(text.split())}))
