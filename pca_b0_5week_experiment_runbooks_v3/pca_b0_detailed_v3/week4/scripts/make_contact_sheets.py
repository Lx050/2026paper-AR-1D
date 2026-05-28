from PIL import Image, ImageDraw
from pathlib import Path
import pandas as pd, argparse

def make_sheet(paths, labels, out):
    imgs=[Image.open(p).convert('RGB').resize((384,384)) for p in paths]
    canvas=Image.new('RGB',(768,820),'white')
    draw=ImageDraw.Draw(canvas)
    pos=[(0,30),(384,30),(0,425),(384,425)]
    for im,lab,xy in zip(imgs,labels,pos):
        canvas.paste(im,xy)
        draw.text((xy[0]+10,xy[1]-24),lab,fill=(0,0,0))
    canvas.save(out)

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--annotation_items_csv', required=True)
    ap.add_argument('--out_dir', default='outputs/contact_sheets')
    args=ap.parse_args()
    Path(args.out_dir).mkdir(parents=True,exist_ok=True)
    df=pd.read_csv(args.annotation_items_csv)
    for _,r in df.iterrows():
        paths=[r['option_A_path'],r['option_B_path'],r['option_C_path'],r['option_D_path']]
        make_sheet(paths, ['A','B','C','D'], Path(args.out_dir)/f"{r['annotation_item_id']}.jpg")
