import argparse, pandas as pd

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--annotations_csv', required=True)
    ap.add_argument('--key_csv', required=True)
    ap.add_argument('--output_csv', required=True)
    args=ap.parse_args()
    ann=pd.read_csv(args.annotations_csv)
    key=pd.read_csv(args.key_csv)
    df=ann.merge(key,on=['annotation_item_id'],how='left')
    rows=[]
    for method in ['raw','preference_only','consistency_only','pca_b0']:
        rows.append({
            'method':method,
            'user_win_rate':(df['overall_best_method']==method).mean(),
            'core_retention_rate':(df['core_best_method']==method).mean(),
            'core_loss_rate':(df['core_loss_method']==method).mean(),
            'acceptable_deviation_rate':(df['acceptable_deviation_method']==method).mean()
        })
    pd.DataFrame(rows).to_csv(args.output_csv,index=False)
if __name__=='__main__': main()
