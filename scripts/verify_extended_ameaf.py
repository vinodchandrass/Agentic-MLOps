"""Independent regression checks for AMEAF supplementary analyses.
Synthetic logical checks and conditional sensitivity, not empirical validation.
"""
from itertools import product
from fractions import Fraction as F
D='CEAN'
states=('S','P','U','X','NA')
rules=['C','CE','CEA','EN','CEAN']
profiles=list(product(states,repeat=4))
def valid(p,r): return all(p[D.index(d)]!='NA' for d in r)
def support(p,r): return valid(p,r) and all(p[D.index(d)]=='S' for d in r)
counts=[0,0,0,0]
totals=[0,0]
for r in rules:
    for p in profiles:
        if not valid(p,r): continue
        totals[0]+=1
        totals[1]+=support(p,r)
        for i,d in enumerate(D):
            if d in r and p[i]!='S':
                assert support(p[:i]+('S',)+p[i+1:],r)>=support(p,r)
                counts[0]+=1
            if d not in r:
                for v in states:
                    if v==p[i]: continue
                    assert support(p[:i]+(v,)+p[i+1:],r)==support(p,r)
                    counts[1]+=1
            if d in r and support(p,r):
                for v in ('P','U','X'):
                    assert not support(p[:i]+(v,)+p[i+1:],r)
                    counts[2]+=1
for r,t in product(rules,repeat=2):
    if set(r)<set(t):
        for p in profiles:
            if valid(p,t):
                assert not support(p,t) or support(p,r)
                counts[3]+=1
assert totals==[1876,181]
assert counts==[3063,13680,732,2064]
sets=[frozenset(x for i,x in enumerate('SPUX') if mask>>i&1) for mask in range(1,16)]
counts=[0,0,0]
for r in rules:
    for p in product(sets,repeat=len(r)):
        counts[0 if all(s=={'S'} for s in p) else 1 if all('S' in s for s in p) else 2]+=1
assert counts==[5,4739,49721]
# Record 397, Tables I and II, assigned costs, not monetary measurements.
strategies=[(F('0.9222'),95),(F('0.9074'),30),(F('0.8993'),12),(F('0.8929'),0)]
for penalty,expected in [('0.0001','0.00415'),('0.0003','0.00135'),('0.0005','0.00020')]:
    u=sorted((f-F(penalty)*c for f,c in strategies),reverse=True)
    assert (u[0]-u[1])/2==F(expected)
print('PASS: structural, uncertainty and selected operational sensitivity checks')
