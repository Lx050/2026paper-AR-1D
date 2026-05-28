import argparse, pandas as pd
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--resource_matrix', required=True)
    ap.add_argument('--human_metrics', required=True)
    ap.add_argument('--out_dir', default='reports/tables')
    args=ap.parse_args()
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    pd.read_csv(args.resource_matrix).to_markdown(Path(args.out_dir)/'table_resources.md', index=False)
    pd.read_csv(args.human_metrics).to_markdown(Path(args.out_dir)/'table_human_metrics.md', index=False)
if __name__=='__main__': main()
