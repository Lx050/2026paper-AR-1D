import argparse, time
from pathlib import Path
import pandas as pd, torch
from diffusers import DiffusionPipeline

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--tasks_csv', required=True)
    ap.add_argument('--out_dir', default='outputs/candidates/raw')
    ap.add_argument('--model_id', default='stabilityai/stable-diffusion-xl-base-1.0')
    ap.add_argument('--num_seeds', type=int, default=4)
    ap.add_argument('--steps', type=int, default=30)
    ap.add_argument('--guidance', type=float, default=7.0)
    args=ap.parse_args()
    Path(args.out_dir).mkdir(parents=True, exist_ok=True)
    pipe = DiffusionPipeline.from_pretrained(args.model_id, torch_dtype=torch.float16, use_safetensors=True, variant='fp16')
    pipe.to('cuda')
    tasks=pd.read_csv(args.tasks_csv)
    rows=[]
    for _,t in tasks.iterrows():
        for s in range(args.num_seeds):
            seed = 1000 + s
            gen = torch.Generator(device='cuda').manual_seed(seed)
            t0=time.time()
            image = pipe(str(t['prompt']), num_inference_steps=args.steps, guidance_scale=args.guidance, generator=gen).images[0]
            cid=f"{t['task_id']}_raw_s{seed}"
            path=Path(args.out_dir)/f"{cid}.png"
            image.save(path)
            rows.append({**t.to_dict(), 'candidate_id':cid, 'image_path':str(path), 'intervention_level':'raw', 'seed':seed, 'model_id':args.model_id, 'steps':args.steps, 'guidance':args.guidance, 'seconds':time.time()-t0})
    pd.DataFrame(rows).to_csv(Path(args.out_dir)/'metadata.csv', index=False)
if __name__=='__main__': main()
