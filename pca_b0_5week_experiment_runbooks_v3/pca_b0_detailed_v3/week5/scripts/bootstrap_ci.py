import numpy as np

def bootstrap_mean_ci(x, n=5000, seed=0):
    rng=np.random.default_rng(seed)
    x=np.asarray(x,dtype=float)
    vals=[]
    for _ in range(n):
        vals.append(rng.choice(x, size=len(x), replace=True).mean())
    return float(np.mean(x)), float(np.percentile(vals,2.5)), float(np.percentile(vals,97.5))
