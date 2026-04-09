#!/usr/bin/env node
// Live network capture via CDP for the studio-genesis tab.
// Logs to a file and exits when you press Ctrl+C OR after a duration.
//
// Usage: node picset-network-capture.mjs <output_file> [duration_seconds]
import puppeteer from 'puppeteer-core';
import fs from 'fs';

const outFile = process.argv[2] || 'picset-network.json';
const duration = parseInt(process.argv[3] || '600', 10) * 1000;

const browser = await puppeteer.connect({
  browserURL: 'http://localhost:9222',
  defaultViewport: null,
});
const pages = await browser.pages();
const page = pages.find(p => p.url().includes('studio-genesis')) || pages[0];
console.log('Capturing network for:', page.url());

const cdp = await page.target().createCDPSession();
await cdp.send('Network.enable');

const requests = new Map();
const captured = [];

cdp.on('Network.requestWillBeSent', (e) => {
  const u = e.request.url;
  if (!u.includes('picsetai.cn') && !u.includes('supabase') && !u.includes('aliyuncs')) return;
  if (u.endsWith('.js') || u.endsWith('.css') || u.endsWith('.woff') || u.endsWith('.woff2') || u.endsWith('.png') || u.endsWith('.jpg') || u.endsWith('.svg') || u.includes('/assets/')) return;
  requests.set(e.requestId, {
    requestId: e.requestId,
    time: e.wallTime,
    url: u,
    method: e.request.method,
    headers: e.request.headers,
    postData: e.request.postData ? e.request.postData.slice(0, 16000) : null,
  });
});

cdp.on('Network.responseReceived', (e) => {
  const r = requests.get(e.requestId);
  if (r) {
    r.status = e.response.status;
    r.respHeaders = e.response.headers;
    r.mimeType = e.response.mimeType;
  }
});

cdp.on('Network.loadingFinished', async (e) => {
  const r = requests.get(e.requestId);
  if (!r) return;
  try {
    const body = await cdp.send('Network.getResponseBody', {requestId: e.requestId});
    r.respBody = body.base64Encoded ? `[base64 ${body.body.length}b]` : body.body.slice(0, 16000);
  } catch (err) { r.respError = String(err); }
  captured.push(r);
  console.log(`[${captured.length}] ${r.method} ${r.url} → ${r.status}`);
  fs.writeFileSync(outFile, JSON.stringify(captured, null, 2));
});

cdp.on('Network.loadingFailed', (e) => {
  const r = requests.get(e.requestId);
  if (!r) return;
  r.failed = e.errorText;
  captured.push(r);
});

console.log(`Capturing for up to ${duration/1000}s. Writing to ${outFile}. Press Ctrl+C to stop early.`);

const stop = async () => {
  console.log(`\nFinal: ${captured.length} requests captured. Saved to ${outFile}`);
  await browser.disconnect();
  process.exit(0);
};

setTimeout(stop, duration);
process.on('SIGINT', stop);
