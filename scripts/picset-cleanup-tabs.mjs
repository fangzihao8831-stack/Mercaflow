#!/usr/bin/env node
// Close all picsetai tabs except studio-genesis
import puppeteer from 'puppeteer-core';

const browser = await puppeteer.connect({
  browserURL: 'http://localhost:9222',
  defaultViewport: null,
});

const pages = await browser.pages();
console.log('Open pages:');
for (const p of pages) console.log('  ', p.url());

const studio = pages.find(p => p.url().includes('studio-genesis'));
if (!studio) {
  console.error('No studio-genesis tab found');
  await browser.disconnect();
  process.exit(1);
}

for (const p of pages) {
  if (p === studio) continue;
  if (p.url().includes('picsetai.cn') || p.url() === 'about:blank' || p.url() === 'chrome://newtab/') {
    console.log('Closing:', p.url());
    await p.close();
  }
}

// Bring studio to front
await studio.bringToFront();
console.log('Active page now:', studio.url());

await browser.disconnect();
