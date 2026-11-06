// Installed Pyodide wheel checks, not an application loader or benchmark.
// npm install --no-save --package-lock=false playwright@1.63.0
// npx playwright install chromium firefox
// node tools/test_pyodide_wheels.mjs wheelhouse [chromium|firefox]
import { chromium, firefox } from 'playwright';
import { createServer } from 'node:http';
import { readFile, readdir } from 'node:fs/promises';
import { resolve, sep } from 'node:path';

const root = resolve(process.argv[2] || 'wheelhouse');
const kind = process.argv[3] || 'chromium';
const runtimes = { '313': '0.29.5', '314': '314.0.4' };
const wheels = (await readdir(root)).filter(x => x.startsWith('pymunk-') && x.endsWith('.whl')).sort();
if (!wheels.length) throw new Error('No Pymunk wheels found in ' + root);
const scenario = await readFile(new URL('./pyodide_scenario.py', import.meta.url), 'utf8');
const server = createServer(async (req, res) => {
  if (req.url === '/') { res.end('<!doctype html><title>Pymunk Pyodide checks</title>'); return; }
  const path = resolve(root, '.' + new URL(req.url, 'http://localhost').pathname);
  if (!path.startsWith(root + sep)) { res.writeHead(403).end(); return; }
  try {
    res.setHeader('Content-Type', 'application/octet-stream');
    res.end(await readFile(path));
  } catch { res.writeHead(404).end(); }
});
await new Promise(r => server.listen(0, '127.0.0.1', r));
let browser;
try {
  browser = await ({ chromium, firefox }[kind]).launch({ headless: true });
  const results = [];
  for (const wheel of wheels) {
    const abi = wheel.match(/-cp(\d+)-/)?.[1];
    const version = runtimes[abi];
    if (!version) throw new Error('No test runtime configured for wheel ABI: ' + wheel);
    const page = await browser.newPage();
    await page.goto(`http://127.0.0.1:${server.address().port}/`);
    await page.addScriptTag({ url: `https://cdn.jsdelivr.net/pyodide/v${version}/full/pyodide.js` });
    const result = await page.evaluate(async ({ wheel, version, scenario }) => {
      const out = [], err = [];
      const pyodide = await loadPyodide({
        indexURL: `https://cdn.jsdelivr.net/pyodide/v${version}/full/`,
        stdout: x => out.push(x), stderr: x => err.push(x),
      });
      await pyodide.loadPackage('micropip');
      const wheelUrl = new URL('/' + wheel, location.href).href;
      await pyodide.runPythonAsync('import micropip\nawait micropip.install(' + JSON.stringify(wheelUrl) + ')');
      try {
        const value = await pyodide.runPythonAsync(scenario);
        return { runtime: pyodide.version, ...JSON.parse(value), out, err };
      } catch (error) {
        throw new Error(JSON.stringify({ wheel, error: String(error), out, err }));
      }
    }, { wheel, version, scenario });
    results.push({ wheel, browser: kind, version: browser.version(), ...result });
    await page.close(); // Fresh runtime per wheel: no mixed CFFI/backend state.
  }
  console.log(JSON.stringify(results, null, 2));
} finally {
  await browser?.close();
  await new Promise(r => server.close(r));
}
