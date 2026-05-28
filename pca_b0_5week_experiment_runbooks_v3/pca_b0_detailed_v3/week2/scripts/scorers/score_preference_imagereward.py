import argparse, pandas as pd
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_csv', required=True)
    parser.add_argument('--output_csv', required=True)
    args = parser.parse_args()
    import ImageReward as RM
    model = RM.load('ImageReward-v1.0')
    df = pd.read_csv(args.input_csv)
    rows = []
    for _, r in df.iterrows():
        path = Path(r['image_path'])
        if not path.exists():
            rows.append({**r.to_dict(), 'imagereward': None, 'error': 'missing image'})
            continue
        try:
            score = float(model.score(str(r['prompt']), [str(path)])[0])
            rows.append({**r.to_dict(), 'imagereward': score, 'error': ''})
        except Exception as e:
            rows.append({**r.to_dict(), 'imagereward': None, 'error': repr(e)})
    pd.DataFrame(rows).to_csv(args.output_csv, index=False)
if __name__ == '__main__':
    main()
