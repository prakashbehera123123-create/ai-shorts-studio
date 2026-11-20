// Deterministic frame renderer: loads studio/motion/engine.html in headless system Chrome (via the globally installed
// Playwright package), calls renderAt(t) for every frame and pipes JPEG screenshots into FFmpeg.
// Usage: node scripts/render_motion.cjs <spec.json> <out.mp4> [--channel chrome|msedge] [--frames N] [--still t1,t2 --still-dir DIR]
"use strict";
const fs = require("fs");
const path = require("path");
const { spawn } = require("child_process");

function loadPlaywright() {
  try { return require("playwright"); } catch (_) {}
  const { execSync } = require("child_process");
  const root = execSync("npm root -g", { encoding: "utf8" }).trim();
  // Playwright ships inside the globally installed @playwright/cli; reuse it instead of installing a second copy.
  for (const candidate of [path.join(root, "playwright"), path.join(root, "@playwright", "cli", "node_modules", "playwright")]) {
    if (fs.existsSync(candidate)) return require(candidate);
  }
  throw new Error("Playwright not found (expected inside the global @playwright/cli install)");
}

function arg(name, def) {
  const i = process.argv.indexOf(name);
  return i > 0 ? process.argv[i + 1] : def;
}

async function main() {
  const [specPath, outPath] = process.argv.slice(2, 4);
  if (!specPath || !outPath) throw new Error("usage: render_motion.cjs <spec.json> <out.mp4>");
  const spec = JSON.parse(fs.readFileSync(specPath, "utf8"));
  const fps = spec.fps || 30;
  const total = Math.round(spec.duration * fps);
  const limit = Number(arg("--frames", total));
  const stills = (arg("--still", "") || "").split(",").filter(Boolean).map(Number);
  const engine = path.resolve(__dirname, "..", "studio", "motion", "engine.html");

  const { chromium } = loadPlaywright();
  const browser = await chromium.launch({ channel: arg("--channel", "chrome"), headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
    await page.goto("file:///" + engine.replace(/\\/g, "/"));
    await page.evaluate(s => window.loadSpec(s), spec);
    await page.evaluate(() => document.fonts.ready);
    const stage = await page.$("#stage");

    if (stills.length) {
      const dir = arg("--still-dir", path.dirname(outPath));
      fs.mkdirSync(dir, { recursive: true });
      for (const t of stills) {
        await page.evaluate(x => window.renderAt(x), t);
        await stage.screenshot({ path: path.join(dir, `still_${t.toFixed(2)}.jpg`), type: "jpeg", quality: 88 });
      }
      process.stdout.write(`stills: ${stills.length}\n`);
      return;
    }

    const ff = spawn(process.env.FFMPEG || "ffmpeg", [
      "-hide_banner", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", String(fps), "-c:v", "mjpeg", "-i", "-",
      "-c:v", "libx264", "-preset", spec.preset || "medium", "-crf", String(spec.crf || 20), "-pix_fmt", "yuv420p",
      "-r", String(fps), outPath,
    ], { stdio: ["pipe", "inherit", "inherit"] });
    const ffDone = new Promise((res, rej) => ff.on("close", c => (c === 0 ? res() : rej(new Error(`ffmpeg exit ${c}`)))));
    const started = Date.now();
    for (let f = 0; f < Math.min(total, limit); f++) {
      await page.evaluate(x => window.renderAt(x), f / fps);
      const buf = await stage.screenshot({ type: "jpeg", quality: 92 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once("drain", r));
      if (f % (fps * 10) === 0) process.stdout.write(`frame ${f}/${total} (${((Date.now() - started) / 1000).toFixed(0)} s)\n`);
    }
    ff.stdin.end();
    await ffDone;
    process.stdout.write(`done: ${Math.min(total, limit)} frames in ${((Date.now() - started) / 1000).toFixed(0)} s\n`);
  } finally {
    await browser.close();
  }
}

main().catch(e => { process.stderr.write(`render_motion failed: ${e.stack || e}\n`); process.exit(1); });
