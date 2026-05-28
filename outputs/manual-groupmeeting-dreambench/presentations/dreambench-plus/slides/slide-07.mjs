import { bg, footer, palette, title } from "./theme.mjs";

export async function slide07(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "2026 补充：说明看过最新，但不替代主线");
  ctx.addShape(slide, { x: 88, y: 188, w: 505, h: 270, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
  ctx.addShape(slide, { x: 88, y: 188, w: 505, h: 10, fill: palette.blue, line: ctx.line("#00000000", 0) });
  ctx.addText(slide, { x: 122, y: 230, w: 430, h: 32, text: "DSH-Bench", size: 28, bold: true, color: palette.ink, typeface: "Segoe UI" });
  ctx.addText(slide, { x: 122, y: 286, w: 420, h: 66, text: "2026 subject-driven T2I benchmark，可作为最新评估补充，帮助发现更细的 subject failure 类型。", size: 18, color: palette.muted, typeface: "Microsoft YaHei" });
  ctx.addText(slide, { x: 122, y: 390, w: 420, h: 28, text: "https://arxiv.org/abs/2603.08090", size: 13, bold: true, color: palette.deepBlue, typeface: "Segoe UI" });
  ctx.addShape(slide, { x: 687, y: 188, w: 505, h: 270, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
  ctx.addShape(slide, { x: 687, y: 188, w: 505, h: 10, fill: palette.rose, line: ctx.line("#00000000", 0) });
  ctx.addText(slide, { x: 721, y: 230, w: 430, h: 32, text: "Personalize Anything", size: 28, bold: true, color: palette.ink, typeface: "Segoe UI" });
  ctx.addText(slide, { x: 721, y: 286, w: 420, h: 66, text: "AAAI 2026 open-source personalized generation 方法，可作为新架构和 training-free personalization 的观察口。", size: 18, color: palette.muted, typeface: "Microsoft YaHei" });
  ctx.addText(slide, { x: 721, y: 390, w: 420, h: 28, text: "https://github.com/fenghora/personalize-anything", size: 13, bold: true, color: palette.deepBlue, typeface: "Segoe UI" });
  ctx.addShape(slide, { x: 190, y: 522, w: 900, h: 58, fill: "#fff1d0", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 220, y: 538, w: 840, h: 28, text: "汇报策略：DreamBench++ 负责稳定 subject gate；2026 工作负责说明趋势更新。", size: 18, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
  footer(slide, ctx, 7);
  return slide;
}
