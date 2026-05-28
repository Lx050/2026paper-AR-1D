import argparse, pandas as pd
from functools import reduce

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--inputs', nargs='+', required=True)
    ap.add_argument('--output', required=True)
    args=ap.parse_args()
    dfs=[pd.read_csv(p) for p in args.inputs]
    for p,d in zip(args.inputs, dfs):
        if 'candidate_id' not in d.columns:
            raise ValueError(f'missing candidate_id in {p}')
    out=reduce(lambda l,r: pd.merge(l,r,on='candidate_id',how='outer',suffixes=('','_dup')), dfs)
    out.to_csv(args.output,index=False)
if __name__=='__main__': main()
