// Renders the business cards: a print-ready PDF (91 x 55 mm + 3 mm bleed, front and back)
// and PNG previews trimmed to the final size. Usage: node meishi/build.mjs
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { fileURLToPath } from 'url';
import path from 'path';
const here = path.dirname(fileURLToPath(import.meta.url));
const pdfOut = path.join(here, '..', 'PDF', 'Sabri_Mohamadi_Meishi_v3_print_91x55.pdf');
const mm = 96 / 25.4;
const b = await chromium.launch();
const p = await b.newPage({ viewport: { width: Math.round(97 * mm), height: Math.round(122 * mm) }, deviceScaleFactor: 6 });
await p.goto('file://' + path.join(here, 'meishi.html'), { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: pdfOut, width: '97mm', height: '61mm', printBackground: true });
const cards = await p.$$('.card');
for (const [i, side] of ['front-en', 'back-ja'].entries()) {
  const box = await cards[i].boundingBox();
  await p.screenshot({ path: path.join(here, `preview-${side}.png`), clip: { x: box.x + 3 * mm, y: box.y + 3 * mm, width: 91 * mm, height: 55 * mm } });
}
await b.close();
console.log('ok', pdfOut);
