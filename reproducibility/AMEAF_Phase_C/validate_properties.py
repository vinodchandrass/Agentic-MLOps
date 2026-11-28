from itertools import product, combinations
import json
D='CEAN'; states=('S','P','U','X','NA'); rules=['C','CE','CEA','EN','CEAN']
profiles=list(product(states,repeat=4))
def valid(p,r): return all(p[D.index(d)]!='NA' for d in r)
def support(p,r): return valid(p,r) and all(p[D.index(d)]=='S' for d in r)
counts=dict(upgrades=0,irrelevant_changes=0,required_downgrades=0,nested_implications=0)
summary=[]
for r in rules:
 a=[p for p in profiles if valid(p,r)]; s=[p for p in a if support(p,r)]
 summary.append(dict(rule=r,admissible=len(a),supported=len(s),invalid=625-len(a)))
 for p in a:
  for i,d in enumerate(D):
   if d in r and p[i]!='S':
    q=p[:i]+('S',)+p[i+1:]; assert support(q,r)>=support(p,r); counts['upgrades']+=1
   if d not in r:
    for v in states:
     if v==p[i]: continue
     q=p[:i]+(v,)+p[i+1:]; assert support(q,r)==support(p,r); counts['irrelevant_changes']+=1
   if d in r and support(p,r):
    for v in ('P','U','X'):
     q=p[:i]+(v,)+p[i+1:]; assert not support(q,r); counts['required_downgrades']+=1
for r,t in product(rules,repeat=2):
 if set(r)<set(t):
  for p in profiles:
   if valid(p,t):
    assert not support(p,t) or support(p,r); counts['nested_implications']+=1
out={'summary':summary,'checks':counts,'scope':'Synthetic profiles; nested implications assume identical evidence profile and evaluation context; not empirical validation.'}
print(json.dumps(out,indent=2))
