// Renders the CV HTML files to PDF (and PNG previews) with Playwright's Chromium.
// Usage: node build.mjs   (from this folder; run a static server isn't needed, file:// is fine)
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { fileURLToPath } from 'url';
import path from 'path';
const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(here, '..', 'docs', 'assets', 'cv');
const jobs = [
  ['cv-en.html', 'Sabri_Mohamadi_CV_EN.pdf'],
  ['shokumu-ja.html', 'Sabri_Mohamadi_Shokumu_Keirekisho_JA.pdf'],
];
const b = await chromium.launch();
for (const [src, pdf] of jobs.filter(([s]) => process.argv.length < 3 || process.argv.includes(s))) {
  const p = await b.newPage({ viewport: { width: 794, height: 1123 } });
  await p.goto('file://' + path.join(here, src), { waitUntil: 'networkidle' });
  await p.evaluate(() => document.fonts.ready);
  const over = await p.evaluate(() => [...document.querySelectorAll('.page')].map(pg => pg.scrollHeight - pg.clientHeight));
  await p.pdf({ path: path.join(out, pdf), format: 'A4', printBackground: true, preferCSSPageSize: true });
  await p.screenshot({ path: path.join(here, 'preview-' + path.basename(src, '.html') + '.png'), fullPage: true });
  console.log(pdf, 'overflow(px) per page:', over);
  await p.close();
}
await b.close();
