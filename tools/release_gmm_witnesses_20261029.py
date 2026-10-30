"""Exact authored GMM law and independent probability-derivative checks.

No historical panel draw or downloaded implementation is executed.
"""
from pathlib import Path
import hashlib,json
import numpy as np
import sympy as s
R=Path(__file__).resolve().parents[1];B=R/'docs/release/2026-10-29/source-windmeijer-032'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 G=s.Matrix([1,1]);b=s.Matrix([1,3]);t1=s.Integer(2);law=[]
 for u in [-1,1]:
  for v in [-1,1]:law.append((s.Matrix([1,1+s.Rational(u,2)]),s.Matrix([1+u,3+2*v])))
 residuals=[bi-gi*t1 for gi,bi in law]
 omega=sum((g*g.T/4 for g in residuals),s.zeros(2));W=omega.inv();H=(G.T*W*G)[0]
 t2=(G.T*W*b)[0]/H;r1=b-G*t1;r2=b-G*t2
 J=sum((-(gi*g.T+g*gi.T)/4 for (gi,bi),g in zip(law,residuals)),s.zeros(2))
 D=-(G.T*W*J*W*r2)[0]/H;psi1=[];psi2=[];naive=[];fixed=[]
 for (gi,bi),g in zip(law,residuals):
  p=((gi-G).dot(r1)+G.dot(g-r1))/G.dot(G);psi1.append(p)
  n=bi-gi*t2
  z=((gi-G).dot(W*r2)+G.dot(W*(n-r2))-G.dot(W*(g*g.T-omega)*W*r2))/H
  fixed.append(z);psi2.append(s.simplify(z+D*p));naive.append(G.dot(W*(n-r2))/H)
 assert sum(psi1)==sum(psi2)==0
 variance1=sum(z*z/4 for z in psi1);variance2=sum(z*z/4 for z in psi2)
 assert t2==s.Rational(5,3) and D==s.Rational(11,36)
 assert variance1==s.Rational(17,16) and variance2==s.Rational(5827,6912)
 centered=omega-r1*r1.T;tc=(G.T*centered.inv()*b)[0]/(G.T*centered.inv()*G)[0];assert tc==s.Rational(3,2)
 # Fresh independent probability differentiation of the estimator functional.
 gs=np.array([np.array(gi,dtype=float).ravel() for gi,bi in law]);bs=np.array([np.array(bi,dtype=float).ravel() for gi,bi in law])
 def estimate(p):
  gm=p@gs;bm=p@bs;one=np.dot(gm,bm)/np.dot(gm,gm);res=bs-gs*one
  om=np.einsum('i,ij,ik->jk',p,res,res);w=np.linalg.inv(om)
  two=np.dot(gm,w@bm)/np.dot(gm,w@gm)
  return np.array([one,two])
 derivative_errors=[]
 for j in range(4):
  direction=np.eye(4)[j]-np.ones(4)/4
  derivative=estimate(np.ones(4)/4+1j*1e-20*direction).imag/1e-20
  expected=np.array([float(psi1[j]),float(psi2[j])]);error=float(np.max(np.abs(derivative-expected)))
  assert error<1e-12;derivative_errors.append(error)
 # The inverse-weight functional is rational, despite quadratic Omega.
 x=s.symbols('x');Ox=sum(((bi-gi*x)*(bi-gi*x).T/4 for gi,bi in law),s.zeros(2));Wx=Ox.inv()
 Q=s.factor((G.T*Wx*r2)[0]/(G.T*Wx*G)[0]);fifth=s.simplify(s.diff(Q,x,5).subs(x,2))
 assert fifth==-s.Rational(725,31104) and s.diff(Q,x).subs(x,2)==D
 report=dict(status='pass',law='Independent fair U,V in{-1,1}; G_i=(1,1+U/2), b_i=(1+U,3+2V);g_i(theta)=b_i-G_i theta.',
  moments=dict(theta1=str(t1),theta2=str(t2),centered_theta2=str(tc),residual1=list(map(str,r1)),residual2=list(map(str,r2)),omega=[[str(v) for v in row] for row in omega.tolist()],weight_derivative=str(D)),
  influences=dict(stage1=list(map(str,psi1)),stage2=list(map(str,psi2)),variance1=str(variance1),variance2=str(variance2),fixed_Jacobian_and_weight_variance=str(sum(z*z/4 for z in naive)),efficient_formula=str(1/H),max_probability_derivative_error=max(derivative_errors)),
  proof_counterexample=dict(Omega=[[str(s.expand(v)) for v in row] for row in Ox.tolist()],Q=str(Q),Q_fifth_derivative_at_2=str(fifth),interpretation='The claimed implication quadratic Omega => fifth derivative of the inverse-weight Q vanishes is false for this finite law. Local smoothness/invertibility supplies a Taylor remainder bound; this does not refute the stated asymptotic theorem.'),
  illustrative_monetary_labels=dict(rule='100 theta-160; assumed reporting map only, no causal interpretation',one_step=str(100*t1-160),uncentered_two_step=str(100*t2-160),centered_two_step=str(100*tc-160)),
  source=dict(path='docs/papers/A Doubly Corrected Robust Variance Estimator for Linear GMM Hwang(2020).pdf',sha256=sha(R/'docs/papers/A Doubly Corrected Robust Variance Estimator for Linear GMM Hwang(2020).pdf')),
  generator=dict(path=str(Path(__file__).relative_to(R)),sha256=sha(Path(__file__))),
  scope='Exact authored law and independent complex-step probability derivatives; no new samples, coverage study, native execution or bank qualification.')
 (B/'exact-witnesses.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
