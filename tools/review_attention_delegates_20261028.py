"""Record selected temporal/source protocol reviews after preserved publication."""
import ast,json
from pathlib import Path
import attention_delegate_reference_20261028 as exact
from record_attention_installer_recovery_20261028 import original,anchors,start,transition
from prepare_followup_program_20261028 import ROOT,ref,write
from run_followup_program_v2_20261028 import selected
from run_followup_program_20261028 import load


def main():
    base=selected();assert base.name=='followup-runtime-v5'
    assert load(ROOT,base)['active'] is None
    plan=json.loads((base/'delegate-acquisition-plan.json').read_text())
    originals={r['id']:original(r) for r in plan['requests']}
    evidence=[ref(base/'delegate-acquisition-plan.json','Five selected pinned delegates'),ref(Path(__file__),'Bounded source-only review')]
    witness=base/'delegate-exact-results.json';write(witness,exact.calculate())
    start(base,'TCDF.DELEGATE','tcdf-delegate',evidence)
    record=anchors(originals['exec28_tcdf_delegate_0'],[
        (6,12,'Right-edge chop uses :-chomp_size; zero yields empty slice under ordinary indexing semantics'),
        (14,53,'Stride1 grouped convolution with padding/chop and middle-block residual'),
        (55,72,'Final block includes a learned linear map across channels at each time'),
        (74,96,'Dilation grows as dilation_c**layer; padding is (kernel_size-1)*dilation')])
    out=base/'tcdf-delegate.json'
    write(out,dict(status='performed_bounded_primary_review',source_records=[record],
        supporting_originals=[ref(ROOT/'docs/literature/raw/exec28_tcdf_source_2.txt','Target-only one-step shift at14-28'),ref(ROOT/'docs/literature/raw/exec28_tcdf_source_3.txt','Feature gate and depthwise invocation at9-33')],
        exact=ref(witness,'Independent index/comparator reference'),reference=ref(Path(exact.__file__),'Authored calculation'),
        derivation='For stride1, p=(k-1)d and right chopping p, kernel index q reads t-p+qd. Hence no future index, but q=k-1 admits t. Across L layers the maximal lookback is (k-1)sum(dilation_c**l); target-only shifting adds one to target raw-history lags.',
        findings=['For k2,dilation2,L3 the convolutional time support can include lags0through7; shifted target raw-history lags1through8. Boundary padding must be part of the fixture.','No-future convolution does not exclude contemporaneous non-target predictors.','LastBlock mixes channels at each time; a kernel maximum alone does not summarize every learned path or establish intervention delay.','kernel_size1 implies zero padding; the selected unconditional :-0 chop empties the sequence. This is a static boundary condition,not observed native behavior.'],
        public_fixture_protocol=['Label variables/timestamps and compare impulse support against the exact index oracle,including first/last observations.','Validate kernel and level domains; explicitly test kernel1,zero levels and dilation edges before deciding reject/support semantics.','Keep target shift,contemporaneous non-target input and final channel mixing explicit in graph conversion.','Separate receptive field support from learned delay attribution and causal identification.'],
        remaining=['Native tensor-version execution and complete dependency rights not performed.','Unavailable TCDF scholarly original remains an omission; code does not substitute.'],native_execution=False,evidence=evidence))
    transition(base,'TCDF.DELEGATE','tcdf-delegate',out,[
        'Exact96-line original verified by collector SHA256/Git blob; padding,dilation,residual and channel-mixing anchors inspected.',
        'Independent time-index/zero-chop witness recorded with explicit proposed boundary fixtures and native/source limits.'
    ],'Integrate temporal support and boundary protocol; continue TACD source configuration review.',evidence)
    start(base,'TACD.PROTOCOL','tacd-protocol',evidence)
    spans={
        'exec28_tacd_delegate_0':[(3,49,'All four named dataset configurations explicitly set split_ratio1.0')],
        'exec28_tacd_delegate_1':[(8,25,'Reported confusion counts include diagonal; library metrics delegated to gCastle'),(28,49,'Threshold curve masks diagonal,selects F1 argmax and constructs final matrix with strict greater-than')],
        'exec28_tacd_delegate_2':[(1,5,'Imports data_mapto_es,not present in selected complete tree'),(7,42,'Three real-data branches load graph truth; no explicit simulation implementation before returning local variables')],
        'exec28_tacd_delegate_3':[(9,39,'CLI exposes data_name,simulation option,seed and topology settings'),(51,60,'Passes loaded graph into algorithm,then uses same graph again for threshold selection and printed Train metrics')],
    }
    records=[anchors(originals[k],ss) for k,ss in spans.items()]
    config=ast.parse((ROOT/'docs/literature/raw/exec28_tacd_delegate_0.txt').read_text())
    configs={n.targets[0].id:ast.literal_eval(n.value) for n in config.body if isinstance(n,ast.Assign)}
    assert len(configs)==4 and all(c['split_ratio']==1.0 for c in configs.values())
    tree=json.loads((ROOT/'docs/literature/raw/exec28_attention_tree_2.json').read_text());assert not tree['truncated']
    assert not any(r['path'].endswith('data_mapto_es.py') for r in tree['tree'])
    out=base/'tacd-protocol.json'
    write(out,dict(status='performed_bounded_primary_review',source_records=records,
        supporting_originals=[ref(ROOT/'docs/literature/raw/exec28_attention_code_2_0.txt','Selected method:config map1-18,truth-guided selection447-568,entrypoint586-621'),ref(ROOT/'docs/literature/raw/exec28_attention_code_2_1.txt','Wrapper passes graph truth'),ref(ROOT/'docs/literature/raw/exec28_attention_tree_2.json','Complete selected tree')],
        observed_split_ratios={k:c['split_ratio'] for k,c in configs.items()},
        findings=['All four inspected configurations choose shared train/validation pair lists in the previously reviewed >=1 branch; this is now source-confirmed,not merely an absent-key default.','Selected real-data entrypoints load graph truth,pass it into training/checkpoint selection,and optimize output threshold against it again. Results require oracle-assisted/in-sample labels until a disjoint protocol is run.','The source masks diagonals for threshold selection but manual confusion counts loop over all entries. Specify off-diagonal denominator and preserve any difference from delegated library metrics.','The final threshold comparison is strict >; tie-aware fixtures must compare it to the exact bound precision-recall library semantics. An exact inclusive/strict witness illustrates the risk without claiming native mismatch.','The selected tree lacks imported data_mapto_es; external provision is unresolved. The simulation CLI choice has no corresponding selected DataProcess branch assigning its returned locals.','Selected method chooses cuda:4 whenever CUDA is available and sets seed2025 internally; supported device inventory and effective seed must be explicit before native use.'],
        exact=ref(witness,'Independent threshold equality and empty-denominator requirements'),reference=ref(Path(exact.__file__),'Authored finite reference'),
        proposed_public_protocol=[
          'Freeze separate graph families/instances for training,tuning and evaluation; prevent evaluation truth from reaching training or threshold selectors.',
          'Bind the graph/event generator,all component versions and source/rights; preserve known,unknown and disputed graph truth as different denominators.',
          'Split independent realizations where possible; for temporal holdout declare history boundary/purge rule and whether graph stays fixed. Fit preprocessing only on allowed training observations.',
          'Select hyperparameters/checkpoints/thresholds only with permitted training/tuning truth or predeclared predictive loss; score untouched evaluation truth once.',
          'Use labelled off-diagonal edge universes,document > versus >= and ties; return unavailable for zero valid batches and log all requested/failed attempts.',
          'Qualify CLI argument names,truth-free mode,simulation branch,missing delegate,device choice and effective seed before any native comparison.',
          'Compare direct source route,thin adapter and a separately authored reference on matched inputs; account for full end-to-end data,fit,conversion,scoring and failed-run costs.'
        ],remaining=['No original scientific paper for this repository admitted; selected software-source findings only.','Native execution,scikit-learn/gCastle transitive scoring semantics,missing module and component rights unresolved.'],native_execution=False,evidence=evidence))
    transition(base,'TACD.PROTOCOL','tacd-protocol',out,[
        'All four selected config/scoring/data/main originals verified by hash/blob and inspected against method/wrapper branches.',
        'Actual split/truth/device/source boundaries separated from proposed untouched evaluation protocol; no native claim.'
    ],'Integrate specific temporal/selection protocol findings; disposition finite unavailable-original routes independently.',evidence)
    print(json.dumps(dict(status='pass',source_files=5,authored_reference='pass',states=load(ROOT,base)['states'])))


if __name__=='__main__':main()
