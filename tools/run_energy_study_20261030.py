"""Authored arithmetic and Poisson arrivals; no sensor code or model calls."""
from pathlib import Path
import csv, hashlib, json, math, platform, sys
from fractions import Fraction as F
import numpy as np

R = Path(__file__).resolve().parents[1]
O = R / 'docs/twelve-hour-closure/2026-10-29/energy-study-attempt-1'
SEED = 202610300218
N = 100_000

def save(p, data):
    p.write_text(json.dumps(data, indent=2, allow_nan=False) + '\n')

def trap(t, p):
    return sum((t[i+1]-t[i])*(p[i+1]+p[i])/2 for i in range(len(t)-1))

def main():
    assert not O.exists(), 'Preserve the existing experiment'
    O.mkdir(parents=True)
    trace = dict(seconds=[0,1,2,3,4,5,6], watts=[100,100,10,10,10,100,100],
                 utilization_percent=[50,50,0,0,0,50,50])
    t = [F(x) for x in trace['seconds']]
    p = [F(x) for x in trace['watts']]
    a = [u > 0 for u in trace['utilization_percent']]
    full = trap(t,p)
    zero_idle = trap(t,[x if active else F(0) for x,active in zip(p,a)])
    retained = trap([x for x,y in zip(t,a) if y],[x for x,y in zip(p,a) if y])
    # Independent interval-area reconstruction, keeping the original timeline.
    explicit = [F(100),F(55),F(10),F(10),F(55),F(100)]
    assert full == sum(explicit) == 330
    assert zero_idle == 300 and retained == 600
    assert trap([F(0)],[F(100)]) == 0
    assert trap(t,[F(100)]*7) == 600
    # A util=0 measurement does not identify incremental power above idle.
    baseline_excess = trap(t,[x-F(10) for x in p])
    assert baseline_excess == 270
    save(O/'power-trace.json',dict(trace=trace,full_linear_interpolation_j=float(full),
         zero_idle_samples_linear_interpolation_j=float(zero_idle),
         active_samples_removed_before_trapezoid_j=float(retained),
         measured_baseline_subtraction_illustration_j=float(baseline_excess),
         explicit_interval_areas_j=[float(x) for x in explicit],
         limitations=['Authored synthetic trace, not measured hardware.',
         'Linear interpolation is a declared convention, not recovered truth between samples.',
         'Zeroing idle utilization differs from subtracting a baseline.',
         'Active-only trapezoid mirrors one pinned source branch, not the 2024 paper method.',
         'Single/no sample zero is insufficient measurement, not proof of zero energy.']))
    rows=[]
    child_seeds=np.random.SeedSequence(SEED).spawn(9)
    for k,(b,rate) in enumerate((b,l)for b in [1,4,20]for l in [1,10,60]):
        rng=np.random.default_rng(child_seeds[k])
        gaps=rng.exponential(60/rate,size=(N,b-1))
        times=np.column_stack([np.zeros(N),np.cumsum(gaps,axis=1)])
        waits=times[:,-1,None]-times
        batch_mean=waits.mean(axis=1)
        exact_mean=(b-1)*60/(2*rate)
        exact_var=(60/rate)**2*(b-1)*(2*b-1)/(6*b)
        mean=float(batch_mean.mean())
        se=float(batch_mean.std(ddof=1)/math.sqrt(N))
        discrepancy=abs(mean-exact_mean)
        assert discrepancy<=6*math.sqrt(exact_var/N)+1e-10
        if b==1: assert np.all(waits==0)
        if b>1:
            # Sum each interarrival once per earlier waiting customer.
            scalar=(gaps[:100]*np.arange(1,b)[None,:]).sum(axis=1)/b
            assert np.allclose(scalar,batch_mean[:100],atol=1e-12)
        np.savez_compressed(O/f'batch-{b}-rate-{rate}.npz',gaps_seconds=gaps)
        rows.append(dict(batch=b,arrivals_per_minute=rate,independent_batches=N,
             mean_wait_seconds=mean,exact_mean_seconds=exact_mean,mcse_seconds=se,
             exact_mcse_seconds=math.sqrt(exact_var/N),
             customer_wait_p95_seconds=float(np.quantile(waits,.95)),
             first_customer_mean_seconds=float(waits[:,0].mean()),
             exact_first_customer_mean_seconds=(b-1)*60/rate,
             customer_wait_zero_fraction=float((waits==0).mean())))
    with (O/'batching.csv').open('w',newline='')as f:
        w=csv.DictWriter(f,fieldnames=rows[0]);w.writeheader();w.writerows(rows)
    # Exact illustrative whole-attempt accounting; deliberately not empirical.
    # Attempt = complete capped research workflow, including unsuccessful paths.
    e_a,e_b=F(100),F(60)
    p_a,p_b=F(4,5),F(2,5)
    assert e_a/p_a==125 and e_b/p_b==150
    assert (e_b/e_a)==F(3,5)
    assert (p_b/p_a)==F(1,2)
    save(O/'quality-break-even.json',dict(classification='PROJECT_ILLUSTRATION',
       abstract_energy_units_per_complete_attempt=[float(e_a),float(e_b)],
       accepted_useful_result_probabilities=[float(p_a),float(p_b)],
       energy_per_accepted_result=[float(e_a/p_a),float(e_b/p_b)],
       break_even_quality_ratio=float(e_b/e_a),observed_illustrative_quality_ratio=float(p_b/p_a),
       scope='Ratios of expectations for repeatable whole attempts, not expectation of a finite random ratio. No bank prices or measured model rates.',
       result='40 percent lower attempt energy nevertheless costs 20 percent more energy per useful accepted result.',
       assumptions=['Positive success probability','Comparable task populations and acceptance rules','All failed attempts and internal retries counted','IID or an appropriate law of large numbers across complete attempts']))
    save(O/'result.json',dict(status='pass',classification='PROJECT_DERIVATION_AND_GENERATED_ARRIVALS',
       seed=SEED,independent_batches_per_cell=N,cells=len(rows),rows=rows,
       checks=['Exact rational integration','Independent interval sums','Scalar interarrival weighting',
               'Sample mean within six theoretical Monte Carlo errors','Exact quality arithmetic'],
       limits=['No native package execution','No sensor measurement','No bank traffic model',
               'Collection waiting excludes service, backlog, timeout batching and cancellation',
               'Customer waits within a batch are dependent; mean MCSE clusters by independent batch',
               'Quantiles are descriptive estimates; no quantile confidence claim'],
       environment=dict(python=sys.version,numpy=np.__version__,platform=platform.platform()),
       runner_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()))
    print(json.dumps(dict(status='pass',cells=9,independent_batches=9*N,power_j=[330,300,600,270],
                    sparse_b20_seconds=rows[6]['mean_wait_seconds'])))

if __name__=='__main__':main()
