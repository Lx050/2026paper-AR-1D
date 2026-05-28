import { bg, footer, palette, title } from "./theme.mjs";

export async function slide08(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "下一步：最小可复现实验，不急着堆大模型训练");
  const rows = [
    ["1", "候选生成", "DreamBooth LoRA / IP-Adapter / PhotoMaker / InstantID 生成同主体候选。", palette.blue],
    ["2", "Subject gate", "参考 DreamBench++：Concept Preservation + Prompt Following，VLM/人工抽查。", palette.deepBlue],
    ["3", "Activation ranking", "在通过 gate 的图里比较美感、情绪、记忆 proxy 和小样本人类偏好。", palette.rose],
    ["4", "时间调制", "调整 early/mid/late 的 adapter scale、attention 或风格注入强度。", palette.gold],
    ["5", "形成问题", "找到主体一致性和感知激活之间的可控 trade-off。", palette.green],
  ];
  for (let i = 0; i < rows.length; i++) {
    const y = 184 + i * 78;
    ctx.addShape(slide, { x: 84, y, w: 1040, h: 58, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
    ctx.addShape(slide, { x: 104, y: y + 11, w: 36, h: 36, geometry: "ellipse", fill: rows[i][3], line: ctx.line("#00000000", 0) });
    ctx.addText(slide, { x: 104, y: y + 17, w: 36, h: 24, text: rows[i][0], size: 17, bold: true, color: "#ffffff", align: "center", typeface: "Segoe UI" });
    ctx.addText(slide, { x: 164, y: y + 13, w: 190, h: 28, text: rows[i][1], size: 18, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
    ctx.addText(slide, { x: 360, y: y + 15, w: 720, h: 26, text: rows[i][2], size: 15, color: palette.muted, typeface: "Microsoft YaHei" });
  }
  footer(slide, ctx, 8);
  return slide;
}
