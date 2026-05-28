import argparse, pandas as pd, torch
from PIL import Image
from pathlib import Path
import open_clip

EMOTIONS = ['amusement','anger','awe','contentment','disgust','excitement','fear','sadness']

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input_csv', required=True)
    ap.add_argument('--output_csv', required=True)
    args = ap.parse_args()
    model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='openai')
    tokenizer = open_clip.get_tokenizer('ViT-B-32')
    model.eval()
    text = tokenizer([f'a photo that evokes {e}' for e in EMOTIONS])
    with torch.no_grad():
        text_features = model.encode_text(text)
        text_features /= text_features.norm(dim=-1, keepdim=True)
    df = pd.read_csv(args.input_csv)
    out=[]
    for _, r in df.iterrows():
        p = Path(r['image_path'])
        if not p.exists():
            out.append({**r.to_dict(), 'emotion_top1':'', 'emotion_conf':None, 'error':'missing image'})
            continue
        image = preprocess(Image.open(p).convert('RGB')).unsqueeze(0)
        with torch.no_grad():
            im = model.encode_image(image)
            im /= im.norm(dim=-1, keepdim=True)
            probs = (100.0 * im @ text_features.T).softmax(dim=-1)[0]
        idx = int(probs.argmax())
        out.append({**r.to_dict(), 'emotion_top1':EMOTIONS[idx], 'emotion_conf':float(probs[idx]), 'error':''})
    pd.DataFrame(out).to_csv(args.output_csv, index=False)
if __name__ == '__main__':
    main()
