"""Menezes and Filho, DOI 10.1109/ISCMI67495.2025.11358475, Tables I and II.
Illustrative utility only: aggregation compatibility and cost calibration unverified.
"""
from fractions import Fraction as F
rows = [('RL',9222,45,95),('Periodic',9074,10,30),('ADWIN',8993,4,12),('Static',8929,0,0)]
def analyze():
    front = [a[0] for a in rows if not any(b[1]>=a[1] and b[3]<=a[3] and (b[1]>a[1] or b[3]<a[3]) for b in rows)]
    thresholds = [F(a[1]-b[1],10000*(a[3]-b[3])) for a,b in zip(rows,rows[1:])]
    assert thresholds == sorted(thresholds) and len(front)==4
    bounds = [F(0)]+thresholds+[F(1)]
    for a,b,r in zip(bounds,bounds[1:],rows):
        m=(a+b)/2
        assert max(rows,key=lambda x:F(x[1],10000)-m*x[3])==r
    return {"pareto_front":front,"thresholds":[str(x) for x in thresholds],"conditional_wilcoxon_min":str(F(2,32))}
if __name__=='__main__':
    print(analyze())
