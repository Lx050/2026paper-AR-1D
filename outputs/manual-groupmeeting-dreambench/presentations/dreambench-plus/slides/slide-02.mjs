import { bg, bullet, footer, palette, title } from "./theme.mjs";

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "我的问题不是“更像”，而是“保住后更动人”");
  ctx.addShape(slide, { x: 70, y: 190, w: 500, h: 390, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 100, y: 222, w: 420, h: 42, text: "两层任务", size: 25, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
  ctx.addShape(slide, { x: 104, y: 292, w: 390, h: 72, fill: "#e9f4ef", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 128, y: 310, w: 340, h: 36, text: "第一层：主体一致性是门槛", size: 19, bold: true, color: palette.deepBlue, typeface: "Microsoft YaHei" });
  ctx.addText(slide, { x: 270, y: 384, w: 60, h: 38, text: "↓", size: 28, bold: true, color: palette.muted, align: "center", typeface: "Segoe UI" });
  ctx.addShape(slide, { x: 104, y: 438, w: 390, h: 82, fill: "#fff1d0", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 128, y: 456, w: 340, h: 42, text: "第二层：美感、情绪、记忆激活", size: 19, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
  ctx.addShape(slide, { x: 620, y: 190, w: 560, h: 390, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 652, y: 222, w: 470, h: 42, text: "研究核心", size: 25, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
  bullet(slide, ctx, 660, 292, "Reference image 不是复制模板，而是主体、价值和记忆的锚点。", palette.blue);
  bullet(slide, ctx, 660, 356, "主体 gate 通过后，才比较“哪一张更美、更动人、更像记忆”。", palette.rose);
  bullet(slide, ctx, 660, 420, "创新点从“保主体”后移到“如何安全激活感知变量”。", palette.green);
  footer(slide, ctx, 2);
  return slide;
}
