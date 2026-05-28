import { readFileSync } from "node:fs";
import { writeFile, mkdir } from "node:fs/promises";
import {
  Presentation,
  PresentationFile,
} from "file:///C:/Users/lab610/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/@oai/artifact-tool/dist/artifact_tool.mjs";

const ROOT =
  "G:/Lbx/paper/2026_5_25/outputs/019e64fd-ec27-7b82-92fe-cb68f472cad9/presentations/ar-eostok-baseline";
const PREVIEW_DIR = `${ROOT}/preview`;
const LAYOUT_DIR = `${ROOT}/layout`;
const OUTPUT_DIR = `${ROOT}/output`;
const FINAL_PPTX = `${OUTPUT_DIR}/ar-image-generation-eostok-bitdance-baseline.pptx`;
const EOSTOK_FIG2 = `${ROOT}/assets/eostok_figure2_pipeline.png`;
const BITDANCE_FIG4 = `${ROOT}/assets/bitdance_figure4_architecture.png`;

const W = 1280;
const H = 720;

const C = {
  bg: "#F7F8F4",
  bg2: "#EEF2EA",
  ink: "#17212E",
  muted: "#667085",
  line: "#CED7D1",
  panel: "#FFFFFF",
  eostok: "#287D6B",
  eostok2: "#CFE8DE",
  bit: "#D45F45",
  bit2: "#F6D8CC",
  blue: "#2F64B3",
  blue2: "#D8E5F8",
  amber: "#B98221",
  amber2: "#F3E2BC",
  violet: "#6956B7",
  violet2: "#E3DDF7",
  dark: "#253044",
};

const FONT = "Microsoft YaHei";

async function saveBlob(blob, path) {
  if (typeof blob.save === "function") {
    await blob.save(path);
    return;
  }
  const buf = Buffer.from(await blob.arrayBuffer());
  await writeFile(path, buf);
}

function addShape(slide, geometry, x, y, w, h, opts = {}) {
  return slide.shapes.add({
    geometry,
    position: { left: x, top: y, width: w, height: h },
    fill: opts.fill ?? { type: "none" },
    line: opts.line ?? { fill: { type: "none" }, width: 0 },
    shadow: opts.shadow,
  });
}

function addText(slide, text, x, y, w, h, opts = {}) {
  const shape = addShape(slide, "rect", x, y, w, h, {
    fill: opts.fill ?? { type: "none" },
    line: opts.line ?? { fill: { type: "none" }, width: 0 },
  });
  shape.text = text;
  shape.text.typeface = opts.font ?? FONT;
  shape.text.fontSize = opts.size ?? 22;
  shape.text.color = opts.color ?? C.ink;
  shape.text.bold = opts.bold ?? false;
  shape.text.alignment = opts.align ?? "left";
  shape.text.verticalAlignment = opts.valign ?? "top";
  shape.text.wrap = "square";
  shape.text.autoFit = opts.autoFit ?? "shrinkText";
  shape.text.insets = opts.insets ?? { top: 4, right: 4, bottom: 4, left: 4 };
  if (opts.lineSpacing) shape.text.lineSpacing = opts.lineSpacing;
  return shape;
}

function addBox(slide, text, x, y, w, h, opts = {}) {
  const shape = addShape(slide, opts.geometry ?? "roundRect", x, y, w, h, {
    fill: { type: "solid", color: opts.fill ?? C.panel },
    line: opts.line ?? { style: "solid", fill: opts.stroke ?? C.line, width: opts.strokeWidth ?? 1.2 },
    shadow: opts.shadow,
  });
  if (text) {
    shape.text = text;
    shape.text.typeface = FONT;
    shape.text.fontSize = opts.size ?? 18;
    shape.text.color = opts.color ?? C.ink;
    shape.text.bold = opts.bold ?? false;
    shape.text.alignment = opts.align ?? "center";
    shape.text.verticalAlignment = opts.valign ?? "middle";
    shape.text.wrap = "square";
    shape.text.autoFit = "shrinkText";
    shape.text.insets = opts.insets ?? { top: 10, right: 12, bottom: 10, left: 12 };
  }
  return shape;
}

function addPill(slide, text, x, y, w, h, color, fill) {
  return addBox(slide, text, x, y, w, h, {
    fill,
    stroke: color,
    strokeWidth: 1,
    size: 15,
    color,
    bold: true,
    insets: { top: 4, right: 10, bottom: 4, left: 10 },
  });
}

function addArrow(slide, from, to, color = C.dark, opts = {}) {
  return slide.shapes.connect(from, to, {
    kind: opts.kind ?? "straight",
    fromSide: opts.fromSide ?? "right",
    toSide: opts.toSide ?? "left",
    line: { style: opts.style ?? "solid", fill: color, width: opts.width ?? 2 },
    head: opts.head === false ? undefined : { type: "arrow", width: "med", length: "med" },
  });
}

function addRightArrow(slide, x, y, w, h, color) {
  return addShape(slide, "rightArrow", x, y, w, h, {
    fill: { type: "solid", color },
    line: { fill: color, width: 0.5 },
  });
}

function addBackground(slide, title, eyebrow, slideNo) {
  addShape(slide, "rect", 0, 0, W, H, {
    fill: { type: "solid", color: C.bg },
    line: { fill: { type: "none" }, width: 0 },
  });
  addShape(slide, "rect", 0, 0, W, 86, {
    fill: { type: "solid", color: "#FBFCF8" },
    line: { fill: C.line, width: 0.8 },
  });
  addText(slide, eyebrow, 54, 20, 500, 22, {
    size: 13,
    color: C.muted,
    bold: true,
  });
  addText(slide, title, 50, 42, 930, 40, {
    size: 25,
    color: C.ink,
    bold: true,
  });
  addText(slide, `0${slideNo}`, 1175, 27, 50, 38, {
    size: 18,
    color: C.muted,
    bold: true,
    align: "right",
  });
}

function footer(slide, source) {
  addShape(slide, "rect", 50, 664, 1180, 1, {
    fill: { type: "solid", color: "#D6DDD7" },
    line: { fill: { type: "none" }, width: 0 },
  });
  addText(slide, source, 52, 672, 980, 22, {
    size: 10.5,
    color: C.muted,
  });
  addText(slide, "AR图像生成与1D语义Token · 主体一致性调研", 980, 672, 250, 22, {
    size: 10.5,
    color: C.muted,
    align: "right",
  });
}

function metric(slide, value, label, x, y, color) {
  const box = addBox(slide, "", x, y, 162, 86, {
    fill: "#FFFFFF",
    stroke: color,
    strokeWidth: 1.5,
  });
  addText(slide, value, x + 14, y + 12, 134, 30, {
    size: 24,
    color,
    bold: true,
    align: "center",
  });
  addText(slide, label, x + 14, y + 45, 134, 26, {
    size: 12,
    color: C.muted,
    align: "center",
  });
  return box;
}

function addSourceFigure(slide, path, x, y, w, h, alt, stroke = C.line) {
  addBox(slide, "", x - 6, y - 6, w + 12, h + 12, {
    fill: "#FFFFFF",
    stroke,
    strokeWidth: 1.1,
  });
  const dataUrl = `data:image/png;base64,${readFileSync(path).toString("base64")}`;
  return slide.images.add({
    dataUrl,
    alt,
    position: { left: x, top: y, width: w, height: h },
    fit: "contain",
  });
}

function slide1(p) {
  const s = p.slides.add();
  addBackground(s, "AR图像生成技术路线图：从空间token到语义token", "TECH ROADMAP | subject consistency entry points", 1);
  addText(
    s,
    "核心判断：AR图像生成正在从“按空间格子预测”转向“按语义与高熵表征组织生成”；主体一致性的机会点出现在 tokenizer 排列、身份块注意力和可回写精炼。",
    54,
    98,
    1130,
    48,
    { size: 17, color: C.dark, lineSpacing: 1.05 }
  );

  const years = [
    { y: "2024", title: "AR追平扩散", papers: "VAR / LlamaGen / Emu3", color: C.blue, fill: C.blue2 },
    { y: "2025", title: "高分辨率与混合架构", papers: "SimpleAR / Infinity / OmniGen2", color: C.amber, fill: C.amber2 },
    { y: "2026", title: "Token范式重构", papers: "EOSTok / SemTok / BitDance / GRN", color: C.eostok, fill: C.eostok2 },
  ];
  const yearBoxes = years.map((item, i) => {
    const x = 78 + i * 382;
    addText(s, item.y, x, 165, 120, 28, { size: 21, color: item.color, bold: true, align: "center" });
    return addBox(s, `${item.title}\n${item.papers}`, x, 198, 292, 86, {
      fill: item.fill,
      stroke: item.color,
      color: C.ink,
      size: 17,
      bold: true,
    });
  });
  addArrow(s, yearBoxes[0], yearBoxes[1], C.dark, { width: 2.2 });
  addArrow(s, yearBoxes[1], yearBoxes[2], C.dark, { width: 2.2 });
  addRightArrow(s, 398, 228, 38, 20, C.dark);
  addRightArrow(s, 780, 228, 38, 20, C.dark);

  const lanes = [
    {
      label: "表征层",
      color: C.eostok,
      items: ["2D空间token", "1D语义token", "二值token / 连续头", "HBQ近无损latent"],
    },
    {
      label: "生成层",
      color: C.bit,
      items: ["next-token", "next-scale", "next-patch diffusion", "global refinement"],
    },
    {
      label: "一致性层",
      color: C.violet,
      items: ["无显式身份通道", "身份token可聚类", "容量/速度baseline", "漂移后可回写"],
    },
  ];

  lanes.forEach((lane, idx) => {
    const y = 332 + idx * 90;
    addPill(s, lane.label, 54, y + 18, 100, 34, lane.color, "#FFFFFF");
    let prev = null;
    lane.items.forEach((it, j) => {
      const node = addBox(s, it, 182 + j * 255, y, 196, 68, {
        fill: "#FFFFFF",
        stroke: j === 1 && idx !== 1 ? lane.color : C.line,
        strokeWidth: j === 1 && idx !== 1 ? 1.8 : 1,
        color: j === 1 && idx !== 1 ? lane.color : C.ink,
        size: 15,
        bold: j === 1 || j === 2,
      });
      if (prev) addArrow(s, prev, node, lane.color, { width: 1.5 });
      if (prev) addRightArrow(s, 390 + (j - 1) * 255, y + 24, 30, 16, lane.color);
      prev = node;
    });
  });

  addBox(
    s,
    "本汇报聚焦：EOSTok 作为语义token路线；BitDance 作为高熵二值token baseline",
    196,
    608,
    888,
    38,
    { fill: "#FFFFFF", stroke: C.dark, size: 16, color: C.dark, bold: true }
  );
  footer(s, "Sources: VAR arXiv:2404.02905; EOSTok arXiv:2605.00503; BitDance arXiv:2602.14041; GRN arXiv:2604.13030");
}

function slide2(p) {
  const s = p.slides.add();
  addBackground(s, "EOSTok 摘要：端到端 1D 语义 tokenizer 让 AR 看见语义结构", "PAPER ABSTRACT | main method", 2);

  addBox(s, "", 56, 112, 338, 452, { fill: "#FFFFFF", stroke: C.eostok, strokeWidth: 1.6 });
  addPill(s, "EOSTok", 82, 138, 116, 34, C.eostok, C.eostok2);
  addText(s, "End-to-End Autoregressive Image Generation with 1D Semantic Tokenizer", 82, 184, 262, 78, {
    size: 22,
    bold: true,
    color: C.ink,
  });
  addText(s, "ICML 2026 Spotlight\nByteDance Seed / Caltech / Stanford", 82, 276, 260, 48, {
    size: 15,
    color: C.muted,
  });
  metric(s, "FID 1.48", "ImageNet 256² / no guidance", 82, 348, C.eostok);
  metric(s, "1D token", "按语义组织视觉序列", 222, 348, C.eostok);
  addText(s, "研究位置：不是单纯换一个 codebook，而是让 tokenizer 在训练时直接感知下游 AR 生成目标。", 82, 462, 260, 62, {
    size: 15,
    color: C.dark,
  });

  const cards = [
    {
      t: "问题",
      body: "传统视觉 tokenizer 输出固定 2D 网格，AR 只能按光栅或尺度顺序预测；身份、姿态、背景在 token 序列里被混在一起。",
      c: C.bit,
      f: C.bit2,
    },
    {
      t: "方法",
      body: "EOSTok 将图像压缩成 1D 语义 token，并用端到端训练把重建目标与生成目标联合起来，让 tokenizer 受 AR 结果反馈。",
      c: C.eostok,
      f: C.eostok2,
    },
    {
      t: "创新",
      body: "相比先训 tokenizer 再训生成器，EOSTok 把 tokenizer 作为生成系统的一部分优化；同时利用视觉基础模型增强 1D token 的语义性。",
      c: C.blue,
      f: C.blue2,
    },
    {
      t: "一致性启示",
      body: "若身份 token 在 1D 序列中形成稳定块，AR 可增强身份块 attention，或将身份块前置来减轻长程衰减",
      c: C.violet,
      f: C.violet2,
    },
  ];
  cards.forEach((card, idx) => {
    const x = 438 + (idx % 2) * 372;
    const y = 120 + Math.floor(idx / 2) * 210;
    addBox(s, "", x, y, 330, 168, { fill: "#FFFFFF", stroke: card.c, strokeWidth: 1.3 });
    addPill(s, card.t, x + 22, y + 18, 78, 30, card.c, card.f);
    addText(s, card.body, x + 22, y + 62, 282, 78, {
      size: 17,
      color: C.dark,
      lineSpacing: 1.08,
    });
  });

  addBox(
    s,
    "汇报一句话：EOSTok 的价值不只是“FID更好”，而是把视觉token从空间索引变成语义单位，为主体一致性提供结构先验",
    438,
    554,
    702,
    58,
    { fill: "#FFFFFF", stroke: C.eostok, strokeWidth: 1.5, size: 16, color: C.ink, bold: true }
  );
  footer(s, "Source: EOSTok, arXiv:2605.00503, submitted 2026-05-01, ICML 2026 Spotlight");
}

function slide3(p) {
  const s = p.slides.add();
  addBackground(s, "EOSTok 原论文图：端到端训练把 tokenizer 与 AR 生成器绑在一起", "SOURCE FIGURE | EOSTok Figure 2", 3);

  addSourceFigure(
    s,
    EOSTOK_FIG2,
    76,
    112,
    1128,
    362,
    "EOSTok Figure 2 overall training pipeline",
    C.eostok
  );
  addPill(s, "原论文 Figure 2", 90, 126, 136, 30, C.eostok, C.eostok2);
  addText(s, "图中关键：VFM(DINOv2)提供语义表征；1D causal ViT encoder 产出 latent token；AR Transformer 的 next-token loss 反向约束 tokenizer；APR/decoder alignment 把 AR 预测重新拉回像素空间。", 94, 488, 1092, 38, {
    size: 15.5,
    color: C.dark,
  });

  const levers = [
    ["为什么利于一致性", "tokenizer 被生成损失监督，语义 token 不只是重建压缩码。", C.eostok, C.eostok2],
    ["可研究的身份块", "若身份相关 token 稳定聚集，可做身份块前置或 attention 增强。", C.violet, C.violet2],
    ["区别于扩散控制", "一致性约束可前移到 token 排列，而非只在采样阶段补救。", C.bit, C.bit2],
  ];
  levers.forEach((l, i) => {
    const x = 90 + i * 374;
    addBox(s, "", x, 540, 326, 78, { fill: "#FFFFFF", stroke: l[2], strokeWidth: 1.3 });
    addPill(s, l[0], x + 18, 554, 136, 26, l[2], l[3]);
    addText(s, l[1], x + 18, 588, 284, 22, { size: 13.5, color: C.dark });
  });

  footer(s, "Source figure: EOSTok Figure 2, arXiv:2605.00503; Chinese callouts are interpretation for subject consistency");
}

function slide4(p) {
  const s = p.slides.add();
  addBackground(s, "BitDance 摘要：用高熵二值token做强AR baseline", "PAPER ABSTRACT | baseline model", 4);

  addBox(s, "", 56, 112, 340, 458, { fill: "#FFFFFF", stroke: C.bit, strokeWidth: 1.6 });
  addPill(s, "BitDance", 82, 138, 128, 34, C.bit, C.bit2);
  addText(s, "Scaling Autoregressive Generative Models with Binary Tokens", 82, 184, 262, 74, {
    size: 22,
    bold: true,
    color: C.ink,
  });
  addText(s, "2026.02 | ByteDance + CUHK + SJTU + CAS + NUS", 82, 276, 260, 44, {
    size: 15,
    color: C.muted,
  });
  metric(s, "FID 1.24", "ImageNet 256² / AR最优", 82, 348, C.bit);
  metric(s, "260M", "参数规模", 222, 348, C.bit);
  addText(s, "baseline 角色：检验“强 token 容量与高效解码”本身能否带来一致性，而不是语义分组带来的收益。", 82, 462, 260, 62, {
    size: 15,
    color: C.dark,
  });

  const rows = [
    ["问题", "VQ codebook 索引的词表容量有限；超大词表 softmax 代价高，长序列 AR 推理慢。"],
    ["方法", "把视觉 token 二值化：每个 token 是高维二进制向量，理论状态数最高可达 2^256。"],
    ["关键机制", "不用标准分类头，而用 binary diffusion head 在连续超立方体顶点附近预测二值 token。"],
    ["加速策略", "next-patch diffusion 并行预测多个 token，在保持质量的同时提升吞吐。"],
  ];
  rows.forEach((r, i) => {
    const y = 126 + i * 96;
    addPill(s, r[0], 440, y + 13, 92, 28, i === 2 ? C.blue : C.bit, i === 2 ? C.blue2 : C.bit2);
    addText(s, r[1], 560, y, 522, 56, { size: 18, color: C.dark, lineSpacing: 1.08 });
    addShape(s, "rect", 438, y + 78, 646, 1, {
      fill: { type: "solid", color: "#DCE3DD" },
      line: { fill: { type: "none" }, width: 0 },
    });
  });

  addBox(s, "为什么适合作 baseline", 438, 518, 220, 34, {
    fill: C.bit2,
    stroke: C.bit,
    size: 16,
    color: C.bit,
    bold: true,
  });
  addText(
    s,
    "BitDance 是“表征容量/效率”路线的代表；EOSTok 是“语义组织”路线的代表。两者对比能把主体一致性的来源拆开：语义排列 vs 高熵token表达。",
    684,
    510,
    438,
    58,
    { size: 17, color: C.ink }
  );
  footer(s, "Source: BitDance, arXiv:2602.14041, submitted 2026-02-15; reported FID 1.24, 260M params, 8.7x speedup");
}

function slide5(p) {
  const s = p.slides.add();
  addBackground(s, "BitDance 原论文图：binary token baseline 的训练与解码架构", "SOURCE FIGURE | BitDance Figure 4", 5);

  addSourceFigure(
    s,
    BITDANCE_FIG4,
    62,
    110,
    830,
    408,
    "BitDance Figure 4 architecture",
    C.bit
  );
  addPill(s, "原论文 Figure 4", 78, 124, 140, 30, C.bit, C.bit2);

  addBox(s, "", 930, 112, 276, 406, {
    fill: "#FFFFFF",
    stroke: C.dark,
    strokeWidth: 1.2,
  });
  addBox(s, "baseline 读法", 962, 132, 142, 30, {
    fill: C.bg2,
    stroke: "#D6DDD7",
    size: 14.5,
    color: C.dark,
    bold: true,
  });
  addText(s, "BitDance 原图给出三件事：", 958, 180, 210, 28, {
    size: 17,
    color: C.bit,
    bold: true,
  });
  addText(s, "1. 多模态 token 序列仍按 AR 方式训练\n2. vision token 变成 binary latents\n3. binary diffusion head 支持 parallel pred.", 958, 222, 210, 96, {
    size: 14.5,
    color: C.dark,
  });
  addShape(s, "rect", 958, 338, 200, 1, {
    fill: { type: "solid", color: "#D6DDD7" },
    line: { fill: { type: "none" }, width: 0 },
  });
  addText(s, "和 EOSTok 的差别", 958, 360, 180, 26, {
    size: 17,
    color: C.eostok,
    bold: true,
  });
  addText(s, "EOSTok：语义组织与端到端 tokenizer\nBitDance：二值容量与并行解码效率", 958, 402, 210, 54, {
    size: 14.5,
    color: C.dark,
  });

  const claim = addBox(s, "汇报结论", 98, 548, 118, 34, {
    fill: C.dark,
    stroke: C.dark,
    size: 15,
    color: "#FFFFFF",
    bold: true,
  });
  addText(
    s,
    "BitDance 证明 AR 的 token 容量和速度可以非常强；EOSTok 则提供语义可控性。二者合起来，指向“高熵表征 + 语义排序 + 可回写精炼”的下一代 AR 主体一致性路线。",
    238,
    536,
    892,
    60,
    { size: 18, color: C.ink, bold: true }
  );
  footer(s, "Source figure: BitDance Figure 4, arXiv:2602.14041; comparison proposal is inferred from EOSTok and BitDance mechanisms");
}

async function main() {
  await mkdir(PREVIEW_DIR, { recursive: true });
  await mkdir(LAYOUT_DIR, { recursive: true });
  await mkdir(OUTPUT_DIR, { recursive: true });

  const p = Presentation.create();
  slide1(p);
  slide2(p);
  slide3(p);
  slide4(p);
  slide5(p);

  const layout = await p.inspect({ include: "slides elements" });
  await writeFile(`${LAYOUT_DIR}/layout-inspect.json`, JSON.stringify(layout, null, 2), "utf8");

  for (let i = 0; i < p.slides.count; i += 1) {
    const slide = p.slides.getItem(i);
    const blob = await slide.export({ format: "png", scale: 1 });
    await saveBlob(blob, `${PREVIEW_DIR}/slide-${String(i + 1).padStart(2, "0")}.png`);
  }
  const montage = await p.export({ format: "png", montage: true, scale: 0.5 });
  await saveBlob(montage, `${PREVIEW_DIR}/contact-sheet.png`);

  const pptx = await PresentationFile.exportPptx(p);
  await pptx.save(FINAL_PPTX);
  console.log(FINAL_PPTX);
}

await main();
