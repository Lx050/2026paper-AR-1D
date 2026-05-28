import { bg, footer, palette, pill } from "./theme.mjs";

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  pill(slide, ctx, 70, 62, 230, "组会汇报 · 2026-05-27", "#ffffff", palette.deepBlue);
  ctx.addText(slide, { x: 68, y: 142, w: 880, h: 122, text: "从保主体到打动人", size: 52, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
  ctx.addText(slide, { x: 74, y: 258, w: 770, h: 74, text: "主体一致性门槛下的审美、情绪与记忆激活生成", size: 25, color: palette.deepBlue, typeface: "Microsoft YaHei" });
  ctx.addShape(slide, { x: 74, y: 366, w: 692, h: 94, fill: "#e9f4ef", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 98, y: 388, w: 646, h: 56, text: "Good Output = Subject Consistency Gate + Causal-Temporal Perceptual Activation + Human Memory Calibration", size: 20, bold: true, color: palette.ink, typeface: "Segoe UI" });
  ctx.addShape(slide, { x: 850, y: 120, w: 300, h: 414, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 880, y: 154, w: 240, h: 40, text: "主论文押注", size: 22, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
  ctx.addText(slide, { x: 880, y: 214, w: 235, h: 112, text: "DreamBench++\nA Human-Aligned Benchmark for Personalized Image Generation", size: 20, bold: true, color: palette.deepBlue, typeface: "Segoe UI" });
  ctx.addText(slide, { x: 880, y: 350, w: 235, h: 112, text: "定位：不把主体一致性当终点，而是把它作为进入美感、情绪、记忆优化的 gate。", size: 16, color: palette.muted, typeface: "Microsoft YaHei" });
  footer(slide, ctx, 1);
  return slide;
}
