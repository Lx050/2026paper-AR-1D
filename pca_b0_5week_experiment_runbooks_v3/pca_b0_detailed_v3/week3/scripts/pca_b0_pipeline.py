import argparse, pandas as pd

def norm(s):
    s = pd.to_numeric(s, errors='coerce')
    if s.notna().sum() < 2:
        return s.fillna(0.0)
    return (s - s.min()) / (s.max() - s.min() + 1e-8)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--scores_csv', required=True)
    ap.add_argument('--output_csv', required=True)
    ap.add_argument('--subject_thr', type=float, default=0.25)
    args=ap.parse_args()
    df=pd.read_csv(args.scores_csv)
    has_ref = df['reference_image'].fillna('').astype(str).ne('') if 'reference_image' in df else False
    subj = pd.to_numeric(df.get('subject_clip_sim', 1.0), errors='coerce').fillna(1.0)
    df['gate_subject_pass'] = (~has_ref) | (subj >= args.subject_thr)
    if 'structure_pass' in df.columns:
        df['gate_structure_pass'] = df['structure_pass'].fillna('unknown').isin(['true','True','pass','unknown', True])
    else:
        df['gate_structure_pass'] = True
    if 'forbidden_loss_detected' in df.columns:
        df['gate_forbidden_pass'] = ~df['forbidden_loss_detected'].fillna(False).astype(bool)
    else:
        df['gate_forbidden_pass'] = True
    df['accepted_by_gate'] = df['gate_subject_pass'] & df['gate_structure_pass'] & df['gate_forbidden_pass']
    df['activation_rank_score'] = 0.50*norm(df.get('imagereward',0.0)) + 0.20*norm(df.get('emotion_conf',0.0)) + 0.10*norm(df.get('memorability_score',0.0)) + 0.20*norm(df.get('culture_score',0.0))
    df.loc[~df['accepted_by_gate'], 'activation_rank_score'] = -999
    df['rank_in_task'] = df.groupby('task_id')['activation_rank_score'].rank(ascending=False, method='first')
    df.to_csv(args.output_csv, index=False)
if __name__=='__main__': main()
