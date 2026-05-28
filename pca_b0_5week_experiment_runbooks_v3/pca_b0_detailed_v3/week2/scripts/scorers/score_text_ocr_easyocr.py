import argparse, pandas as pd
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input_csv', required=True)
    ap.add_argument('--output_csv', required=True)
    args=ap.parse_args()
    import easyocr
    reader=easyocr.Reader(['en'], gpu=False)
    df=pd.read_csv(args.input_csv)
    rows=[]
    for _,r in df.iterrows():
        p=Path(r['image_path'])
        expected=str(r.get('expected_text','')).strip()
        if not p.exists():
            rows.append({**r.to_dict(), 'ocr_text':'', 'ocr_pass':None, 'ocr_error':'missing image'})
            continue
        result=reader.readtext(str(p), detail=0)
        text=' '.join(result)
        if expected and expected != 'nan':
            passed = expected.lower() in text.lower()
        else:
            passed = None
        rows.append({**r.to_dict(), 'ocr_text':text, 'ocr_pass':passed, 'ocr_error':''})
    pd.DataFrame(rows).to_csv(args.output_csv,index=False)
if __name__ == '__main__': main()
