import { bg, cardText, footer, palette, title } from "./theme.mjs";

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "主体一致性 baseline：不是找万能文章，而是找强路线");
  cardText(slide, ctx, 70, 188, 350, "Fine-tuning route", "DreamBooth / Custom Diffusion：少样本主体定制与多概念干扰。", palette.gold);
  cardText(slide, ctx, 465, 188, 350, "Token route", "Textual Inversion：用 learned token 表示新概念，成本低但表达有限。", palette.blue);
  cardText(slide, ctx, 860, 188, 350, "Adapter route", "IP-Adapter：图像提示接入 workflow，最适合作为 PCA-B0 第一批工程入口。", palette.green);
  cardText(slide, ctx, 70, 340, 350, "Identity route", "PhotoMaker / InstantID：人像身份保持强，但属于 identity 子域。", palette.rose);
  cardText(slide, ctx, 465, 340, 350, "Subject representation", "BLIP-Diffusion：用预训练 subject representation 连接理解和生成。", palette.violet);
  cardText(slide, ctx, 860, 340, 350, "Benchmark route", "DreamBench++：把主体一致性和 prompt following 拆开评估。", palette.deepBlue);
  ctx.addShape(slide, { x: 120, y: 532, w: 1040, h: 56, fill: "#e9f4ef", line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: 150, y: 548, w: 980, h: 26, text: "结论：主体一致性是底线约束，不是最终创新点；PCA-B0 的空间在 gate 之后。", size: 18, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
  footer(slide, ctx, 3);
  return slide;
}
