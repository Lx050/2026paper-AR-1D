import { bg, footer, palette, title } from "./theme.mjs";

export async function slide05(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "从 DreamBench++ 到 PCA-B0：地基之后继续建楼");
  const nodes = [
    { x: 70, y: 232, w: 230, h: 112, t: "Reference Image", b: "主体、身份、物件、用户记忆锚点", c: palette.gold },
    { x: 360, y: 232, w: 230, h: 112, t: "Personalized Generation", b: "DreamBooth / IP-Adapter / PhotoMaker", c: palette.blue },
    { x: 650, y: 232, w: 230, h: 112, t: "DreamBench++ Gate", b: "Concept Preservation + Prompt Following", c: palette.deepBlue },
    { x: 940, y: 232, w: 230, h: 112, t: "PCA-B0 / CTAS", b: "美感、情绪、记忆激活", c: palette.rose },
  ];
  for (const n of nodes) {
    ctx.addShape(slide, { x: n.x, y: n.y, w: n.w, h: n.h, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
    ctx.addShape(slide, { x: n.x, y: n.y, w: n.w, h: 8, fill: n.c, line: ctx.line("#00000000", 0) });
    ctx.addText(slide, { x: n.x + 18, y: n.y + 25, w: n.w - 36, h: 28, text: n.t, size: 17, bold: true, color: palette.ink, typeface: "Segoe UI" });
    ctx.addText(slide, { x: n.x + 18, y: n.y + 60, w: n.w - 36, h: 42, text: n.b, size: 13, color: palette.muted, typeface: "Microsoft YaHei" });
  }
  for (const x of [312, 602, 892]) {
    ctx.addText(slide, { x, y: 267, w: 34, h: 34, text: "→", size: 24, bold: true, color: palette.muted, align: "center", typeface: "Segoe UI" });
  }
  ctx.addShape(slide, { x: 170, y: 432, w: 940, h: 96, fill: "#e9f4ef", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 204, y: 454, w: 872, h: 52, text: "关键差异：DreamBench++ 问“有没有保住主体”；PCA-B0 继续问“保住之后，怎样更美、更动人、更能唤起记忆”。", size: 22, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
  footer(slide, ctx, 5);
  return slide;
}
