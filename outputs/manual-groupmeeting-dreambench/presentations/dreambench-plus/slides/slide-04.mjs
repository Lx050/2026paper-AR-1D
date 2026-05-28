import { bg, bullet, footer, palette, title } from "./theme.mjs";

export async function slide04(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "主押 DreamBench++：最适合做 subject gate");
  ctx.addShape(slide, { x: 70, y: 182, w: 510, h: 420, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 100, y: 216, w: 440, h: 70, text: "DreamBench++\nA Human-Aligned Benchmark for Personalized Image Generation", size: 23, bold: true, color: palette.deepBlue, typeface: "Segoe UI" });
  bullet(slide, ctx, 105, 320, "ICLR 2025 conference paper，用于 personalized image generation 评估。", palette.blue);
  bullet(slide, ctx, 105, 386, "核心拆分：Concept Preservation + Prompt Following。", palette.gold);
  bullet(slide, ctx, 105, 452, "强调 human-aligned evaluation，缓解 CLIP/DINO 与人类判断不一致。", palette.rose);
  ctx.addShape(slide, { x: 630, y: 182, w: 550, h: 420, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 664, y: 216, w: 470, h: 40, text: "可讲的关键数字", size: 25, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
  const xs = [664, 830, 996];
  const labels = [
    ["150", "high-quality reference images"],
    ["1,350", "prompts"],
    ["7", "modern models"],
  ];
  for (let i = 0; i < labels.length; i++) {
    ctx.addShape(slide, { x: xs[i], y: 294, w: 140, h: 124, fill: ["#e9f4ef", "#fff1d0", "#f7dfdc"][i], line: ctx.line("#ffffff", 1) });
    ctx.addText(slide, { x: xs[i] + 12, y: 318, w: 116, h: 38, text: labels[i][0], size: 28, bold: true, color: palette.ink, align: "center", typeface: "Segoe UI" });
    ctx.addText(slide, { x: xs[i] + 12, y: 368, w: 116, h: 32, text: labels[i][1], size: 12, color: palette.muted, align: "center", typeface: "Segoe UI" });
  }
  ctx.addText(slide, { x: 666, y: 462, w: 460, h: 80, text: "我的用法：DreamBench++ 不负责“动人”，但负责先判断主体有没有保住，以及 prompt 是否被执行。", size: 19, bold: true, color: palette.deepBlue, typeface: "Microsoft YaHei" });
  footer(slide, ctx, 4);
  return slide;
}
