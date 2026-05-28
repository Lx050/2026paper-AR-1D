import { bg, footer, palette, title } from "./theme.mjs";

export async function slide09(presentation, ctx) {
  const slide = presentation.slides.add();
  bg(slide, ctx);
  title(slide, ctx, "资料入口：会后可直接点信息图打开链接");
  ctx.addShape(slide, { x: 76, y: 184, w: 1080, h: 370, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
  const sources = [
    ["DreamBench++ PDF", "papers/DreamBenchPlus_2406.16855_full.pdf"],
    ["DreamBench++ arXiv", "https://arxiv.org/abs/2406.16855"],
    ["DreamBench++ Project", "https://dreambenchplus.github.io/"],
    ["DreamBench++ GitHub", "https://github.com/yuangpeng/dreambench_plus"],
    ["DSH-Bench 2026", "https://arxiv.org/abs/2603.08090"],
    ["Personalize Anything", "https://github.com/fenghora/personalize-anything"],
    ["Clickable infographic", "PCA_B0_GROUP_MEETING_INFOGRAPHIC.html"],
    ["Verbatim script", "PCA_B0_GROUP_MEETING_VERBATIM_SCRIPT.md"],
  ];
  for (let i = 0; i < sources.length; i++) {
    const col = i < 4 ? 0 : 1;
    const row = i % 4;
    const x = col === 0 ? 116 : 650;
    const y = 222 + row * 74;
    ctx.addShape(slide, { x, y, w: 460, h: 50, fill: i % 2 === 0 ? "#e9f4ef" : "#fff1d0", line: ctx.line("#ffffff", 1) });
    ctx.addText(slide, { x: x + 18, y: y + 8, w: 180, h: 18, text: sources[i][0], size: 14, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
    ctx.addText(slide, { x: x + 18, y: y + 28, w: 418, h: 16, text: sources[i][1], size: 10.5, color: palette.deepBlue, typeface: "Segoe UI" });
  }
  ctx.addText(slide, { x: 116, y: 586, w: 980, h: 36, text: "说明：PPT 中保留可见 URL；真正可点击入口已放在 HTML 信息图里，适合本地浏览器直接打开。", size: 16, bold: true, color: palette.muted, typeface: "Microsoft YaHei" });
  footer(slide, ctx, 9);
  return slide;
}
