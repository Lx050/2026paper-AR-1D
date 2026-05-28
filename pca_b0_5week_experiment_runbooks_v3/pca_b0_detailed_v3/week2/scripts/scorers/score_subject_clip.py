import argparse, pandas as pd, torch
from pathlib import Path
from PIL import Image
import open_clip

def encode(path, model, preprocess):
    img = preprocess(Image.open(path).convert('RGB')).unsqueeze(0)
    with torch.no_grad():
        z = model.encode_image(img)
        z = z / z.norm(dim=-1, keepdim=True)
    return z

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input_csv', required=True)
    ap.add_argument('--output_csv', required=True)
    args=ap.parse_args()
    model,_,preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
    model.eval()
    df=pd.read_csv(args.input_csv)
    rows=[]
    for _,r in df.iterrows():
        ref = str(r.get('reference_image',''))
        img = str(r.get('image_path',''))
        if not ref or ref=='nan':
            rows.append({**r.to_dict(), 'subject_clip_sim':None, 'subject_error':'no reference'})
            continue
        if not Path(ref).exists() or not Path(img).exists():
            rows.append({**r.to_dict(), 'subject_clip_sim':None, 'subject_error':'missing image'})
            continue
        sim = float((encode(ref,model,preprocess) @ encode(img,model,preprocess).T)[0,0])
        rows.append({**r.to_dict(), 'subject_clip_sim':sim, 'subject_error':''})
    pd.DataFrame(rows).to_csv(args.output_csv,index=False)
if __name__ == '__main__':
    main()
