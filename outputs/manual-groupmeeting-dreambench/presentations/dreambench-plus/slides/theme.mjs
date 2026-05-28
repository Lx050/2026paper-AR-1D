export const palette = {
  ink: "#182235",
  muted: "#607086",
  paper: "#fff7df",
  cream: "#fffdf4",
  blue: "#6fb0c7",
  deepBlue: "#175b74",
  gold: "#edbd61",
  rose: "#e8948b",
  green: "#8daf78",
  violet: "#9d93cf",
  line: "#d9cdb5",
  white: "#ffffff",
};

export function bg(slide, ctx) {
  ctx.addShape(slide, { x: 0, y: 0, w: ctx.W, h: ctx.H, fill: palette.paper });
  ctx.addShape(slide, { x: -90, y: -80, w: 430, h: 270, geometry: "ellipse", fill: "#f5ce79", line: ctx.line("#00000000", 0) });
  ctx.addShape(slide, { x: 880, y: -70, w: 430, h: 310, geometry: "ellipse", fill: "#a9d0dc", line: ctx.line("#00000000", 0) });
  ctx.addShape(slide, { x: 835, y: 510, w: 520, h: 270, geometry: "ellipse", fill: "#efb0aa", line: ctx.line("#00000000", 0) });
  ctx.addShape(slide, { x: -120, y: 560, w: 520, h: 260, geometry: "ellipse", fill: "#d9e6c6", line: ctx.line("#00000000", 0) });
  ctx.addShape(slide, { x: 34, y: 32, w: ctx.W - 68, h: ctx.H - 64, fill: "#fffdf4", line: ctx.line("#ffffff", 1) });
}

export function title(slide, ctx, text, kicker = "PCA-B0 group meeting") {
  ctx.addText(slide, { x: 70, y: 52, w: 760, h: 28, text: kicker, size: 15, bold: true, color: palette.deepBlue, typeface: "Segoe UI" });
  ctx.addText(slide, { x: 68, y: 86, w: 1080, h: 72, text, size: 38, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
}

export function footer(slide, ctx, n) {
  ctx.addText(slide, { x: 70, y: 668, w: 760, h: 22, text: "DreamBench++ as subject gate · PCA-B0 / CTAS as perceptual activation", size: 12, color: palette.muted, typeface: "Segoe UI" });
  ctx.addText(slide, { x: 1168, y: 668, w: 42, h: 22, text: String(n).padStart(2, "0"), size: 13, bold: true, color: palette.deepBlue, align: "right", typeface: "Segoe UI" });
}

export function pill(slide, ctx, x, y, w, text, fill = "#ffffff", color = palette.deepBlue) {
  ctx.addShape(slide, { x, y, w, h: 34, fill, line: ctx.line("#ffffff", 1) });
  ctx.addText(slide, { x: x + 12, y: y + 7, w: w - 24, h: 22, text, size: 13, bold: true, color, typeface: "Microsoft YaHei" });
}

export function card(slide, ctx, x, y, w, h, accent = palette.blue) {
  ctx.addShape(slide, { x, y, w, h, fill: "#ffffff", line: ctx.line("#ffffff", 1) });
  ctx.addShape(slide, { x, y, w: 7, h, fill: accent, line: ctx.line("#00000000", 0) });
}

export function cardText(slide, ctx, x, y, w, titleText, bodyText, accent = palette.blue) {
  card(slide, ctx, x, y, w, 112, accent);
  ctx.addText(slide, { x: x + 22, y: y + 18, w: w - 42, h: 28, text: titleText, size: 18, bold: true, color: palette.ink, typeface: "Microsoft YaHei" });
  ctx.addText(slide, { x: x + 22, y: y + 52, w: w - 42, h: 48, text: bodyText, size: 13, color: palette.muted, typeface: "Microsoft YaHei" });
}

export function bullet(slide, ctx, x, y, text, color = palette.deepBlue) {
  ctx.addShape(slide, { x, y: y + 7, w: 9, h: 9, geometry: "ellipse", fill: color, line: ctx.line("#00000000", 0) });
  ctx.addText(slide, { x: x + 18, y, w: 510, h: 42, text, size: 15, color: palette.ink, typeface: "Microsoft YaHei" });
}
