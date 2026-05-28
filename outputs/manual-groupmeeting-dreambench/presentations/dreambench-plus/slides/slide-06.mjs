import { bg, cardText, footer, palette, title } from "./theme.mjs";

export async function slide06(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "CTAS：因果潜空间 × 扩散时间阶段");
  cardText(slide, ctx, 70, 188, 260, "S_id", "主体、身份、对象不变量。它失效后，后续审美和记忆都失去锚点。", palette.deepBlue);
  cardText(slide, ctx, 360, 188, 260, "S_aes", "颜色、构图、光影、质感、复杂度、风格流畅性。", palette.gold);
  cardText(slide, ctx, 650, 188, 260, "S_affect", "温暖、孤独、怀旧、庄严、震撼、被打动。", palette.rose);
  cardText(slide, ctx, 940, 188, 260, "S_mem", "个人经历、物件线索、时代感、文化符号和熟悉性。", palette.green);
  ctx.addShape(slide, { x: 92, y: 364, w: 1088, h: 150, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 126, y: 392, w: 1000, h: 28, text: "时间调制假设", size: 24, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
  const steps = [
    ["T_early", "锁主体结构和大轮廓", palette.deepBlue],
    ["T_mid", "调语义、构图和情绪", palette.rose],
    ["T_late", "调光影、材质和审美细节", palette.gold],
  ];
  for (let i = 0; i < steps.length; i++) {
    const x = 128 + i * 330;
    ctx.addShape(slide, { x, y: 448, w: 280, h: 42, fill: "#e9f4ef", line: ctx.line("#ffffff", 1) });
    ctx.addText(slide, { x: x + 14, y: 459, w: 90, h: 20, text: steps[i][0], size: 14, bold: true, color: steps[i][2], typeface: "Segoe UI" });
    ctx.addText(slide, { x: x + 94, y: 459, w: 170, h: 20, text: steps[i][1], size: 14, color: palette.ink, typeface: "Microsoft YaHei" });
  }
  ctx.addText(slide, { x: 126, y: 546, w: 980, h: 28, text: "要研究的不是四个分数相加，而是变量之间的冲突、因果关系和安全干预窗口。", size: 18, bold: true, color: palette.deepBlue, typeface: "Microsoft YaHei" });
  footer(slide, ctx, 6);
  return slide;
}
