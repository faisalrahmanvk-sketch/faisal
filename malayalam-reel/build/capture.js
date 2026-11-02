const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [,, outDir, fpsArg, tsArg] = process.argv;
  const fps = +fpsArg || 30, dur = process.env.TIMING ? JSON.parse(fs.readFileSync(process.env.TIMING)).duration : 81.5;
  fs.mkdirSync(outDir, { recursive: true });
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 720, height: 1280 } });
  await p.goto('file://' + path.resolve('index.html')); await p.waitForTimeout(500);
  const timing = process.env.TIMING ? JSON.parse(fs.readFileSync(process.env.TIMING)) : null;
  if (timing) { await p.evaluate(tj => setTiming(tj), timing); fs.writeFileSync(path.join(outDir, 'events.json'), JSON.stringify(await p.evaluate(() => getEvents()))); }
  const ts = tsArg ? tsArg.split(',').map(Number) : Array.from({ length: Math.round(dur * fps) }, (_, i) => i / fps);
  for (let i = 0; i < ts.length; i++) {
    await p.evaluate(t => render(t), ts[i]);
    await p.screenshot({ path: path.join(outDir, tsArg ? `t_${ts[i]}.jpg` : `f_${String(i).padStart(5, '0')}.jpg`), type: 'jpeg', quality: 92 });
  }
  await b.close();
})();
