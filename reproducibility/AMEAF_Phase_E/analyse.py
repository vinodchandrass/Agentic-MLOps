from fractions import Fraction as F
import json
D={k:(F(v),F(c)) for k,v,c in [('RL','0.9222',95),('Periodic','0.9074',30),('ADWIN','0.8993',12),('Static','0.8929',0)]}
# independent symmetric absolute F1 perturbations, fixed reported cost
out=[]
for l in map(F,['0','0.0001','0.0002','0.0003','0.0004','0.0005','0.0006','0.001']):
 u={k:f-l*c for k,(f,c) in D.items()}; w=max(u,key=u.get); gap=u[w]-max(v for k,v in u.items() if k!=w)
 out.append(dict(lambda_=float(l),winner=w,margin=float(gap),max_symmetric_F1_error_for_strict_preference=float(gap/2)))
# worst-case regret under independent F1 intervals; fixed cost
reg=[]
for e in map(F,['0','0.001','0.005','0.01']):
 for l in map(F,['0.0001','0.0003','0.0005','0.001']):
  u={k:f-l*c for k,(f,c) in D.items()}; r={k:max(F(0),max(v-u[k]+2*e for j,v in u.items() if j!=k)) for k in u}; w=min(r,key=r.get)
  assert w==max(u,key=u.get)
  reg.append(dict(error=float(e),lambda_=float(l),minimax=w,worst_regret=float(r[w])))
# minimum mean F1 constraint, cheapest feasible strategy
floors=[]
for t in map(F,['0.89','0.90','0.91','0.92','0.93']):
 for e in map(F,['0','0.005']):
  feasible=[k for k,(f,c) in D.items() if f-e>=t]; w=min(feasible,key=lambda k:D[k][1]) if feasible else None
  floors.append(dict(floor=float(t),error=float(e),cheapest=w))
res=dict(source='Menezes and Filho (2025), Tables I and II, pp.45–46',assumptions='Hypothetical independent symmetric absolute F1 perturbations; fixed assigned costs; not confidence intervals or observed capability retention.',margins=out,regret=reg,floors=floors)
print(json.dumps(res,indent=2))
