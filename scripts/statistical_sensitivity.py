from math import comb
import json

def mcnemar_bounds(n, a, b):
    if not (0 <= a <= n and 0 <= b <= n):
        raise ValueError("Invalid margins")
    results = []
    for x in range(max(0, a+b-n), min(a,b)+1):
        u,v = a-x,b-x
        d = u+v
        p = min(1., 2*sum(comb(d,k) for k in range(min(u,v)+1))/2**d)
        results.append(p)
    return {"feasible_tables":len(results),"min_p":min(results),"max_p":max(results),"tables_p_below_0_05":sum(p<.05 for p in results)}

def wilcoxon_min_exact_two_sided(n):
    if n < 1:
        raise ValueError("Positive nonzero pair count required")
    return 2/2**n

if __name__ == "__main__":
    print(json.dumps({"mcnemar":mcnemar_bounds(150,127,119),"wilcoxon_min_p_five_nonzero_pairs":wilcoxon_min_exact_two_sided(5),"warning":"Sensitivity bounds, not observed paired-test results."},indent=2))
