from itertools import product
from math import comb
import json
D='CEAN'; states='SPUX'; rules=['C','CE','CEA','EN','CEAN']
rows=[]
for r in rules:
 k=len(r); counts=[0]*(k+1); false_support=0; uncertain=0; total=0
 for p in product(states,repeat=k):
  m=sum(x!='S' for x in p); counts[m]+=1
  # illustrative compensatory rule: S=1,P=.5,U=X=0; threshold .75
  if m and sum({'S':1,'P':.5,'U':0,'X':0}[x] for x in p)>=.75*k: false_support+=1
  assert m==sum(x!='S' for x in p)
 assert counts==[comb(k,j)*3**j for j in range(k+1)]
 # uncertainty sets: singleton S, singleton non-S (3), mixed S/non-S (7), non-S-only multisets (4)
 sets=[frozenset(x for i,x in enumerate(states) if mask>>i&1) for mask in range(1,16)]
 robust=possible=impossible=0
 for p in product(sets,repeat=k):
  lo=all(s=={'S'} for s in p); hi=all('S' in s for s in p)
  if lo: robust+=1
  elif hi: possible+=1
  else: impossible+=1
 assert (robust,possible,impossible)==(1,8**k-1,15**k-8**k)
 rows.append(dict(rule=r,required=k,repair_distance_counts=counts,compensatory_disagreements=false_support,uncertainty_profiles=15**k,robust=robust,contingent=possible,impossible=impossible))
print(json.dumps(rows,indent=2))
