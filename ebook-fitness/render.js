// Convierte metodo-define.html en PDF A4 y avisa si algún contenido se sale de su página.
// Uso: node render.js [--shots]
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 1200 } });
  const file = 'file://' + path.join(__dirname, 'metodo-define.html');
  await page.goto(file, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  // Comprobación de desbordes: contenido por debajo de la zona del pie de página
  const issues = await page.evaluate(() => {
    const mm = 96 / 25.4, out = [];
    document.querySelectorAll('.page').forEach(p => {
      const pr = p.getBoundingClientRect();
      const limit = pr.bottom - (p.querySelector('.foot') ? 13 : 8) * mm;
      let max = 0;
      p.querySelectorAll('*').forEach(el => {
        if (el.closest('.foot')) return;
        const r = el.getBoundingClientRect();
        if (r.height > 0 && r.bottom > max) max = r.bottom;
      });
      if (max > limit) out.push(`página ${p.dataset.n}: se sale ${((max - limit) / mm).toFixed(1)} mm`);
    });
    return out;
  });
  console.log(issues.length ? 'DESBORDES:\n' + issues.join('\n') : 'Sin desbordes');

  if (process.argv.includes('--shots')) {
    const n = await page.evaluate(() => document.querySelectorAll('.page').length);
    for (let i = 1; i <= n; i++) {
      const el = await page.$(`.page[data-n="${i}"]`);
      await el.screenshot({ path: path.join(__dirname, 'shots', `p${String(i).padStart(2, '0')}.png`) });
    }
  }

  await page.pdf({ path: path.join(__dirname, 'metodo-define.pdf'), printBackground: true, preferCSSPageSize: true });
  await browser.close();
  console.log('PDF generado');
})();
