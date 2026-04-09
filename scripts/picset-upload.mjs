#!/usr/bin/env node
// Upload a file to a file input on the active page via Chrome DevTools Protocol.
// Usage: node picset-upload.js <local_file_path>
import puppeteer from 'puppeteer-core';
import path from 'path';

const filePath = path.resolve(process.argv[2]);
if (!process.argv[2]) {
  console.error('Usage: node picset-upload.js <file_path>');
  process.exit(1);
}

const browser = await puppeteer.connect({
  browserURL: 'http://localhost:9222',
  defaultViewport: null,
});
const pages = await browser.pages();
// Pick the first non-blank page (the active studio-genesis tab)
const page = pages.find(p => p.url().includes('studio-genesis')) || pages.find(p => p.url().includes('picsetai.cn')) || pages[0];
console.log('Using page:', page.url());

// Find the file input
const handle = await page.$('input[type="file"]');
if (!handle) {
  console.error('No file input found');
  await browser.disconnect();
  process.exit(1);
}

await handle.uploadFile(filePath);
console.log('Uploaded:', filePath);

await browser.disconnect();
