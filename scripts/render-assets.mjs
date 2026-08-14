import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';

const BRAND_DIR = path.resolve('brand-materials');

const assets = [
  { src: 'logos/primary-logo.svg', out: 'logos/primary-logo.png', format: 'png' },
  { src: 'logos/stacked-logo.svg', out: 'logos/stacked-logo.png', format: 'png' },
  { src: 'logos/icon-only.svg', out: 'logos/icon-only.png', format: 'png' },
  { src: 'logos/monochrome-dark.svg', out: 'logos/monochrome-dark.png', format: 'png' },
  { src: 'logos/monochrome-white.svg', out: 'logos/monochrome-white.png', format: 'png' },
  { src: 'social/linkedin-cover.svg', out: 'social/linkedin-cover.jpg', format: 'jpeg' },
  { src: 'social/cover-banner.svg', out: 'social/cover-banner.jpg', format: 'jpeg' },
  { src: 'social/post-template-training.svg', out: 'social/post-template-training.jpg', format: 'jpeg' },
  { src: 'social/profile-photo.svg', out: 'social/profile-photo.png', format: 'png' },
];

function parseViewBox(svgContent) {
  const match = svgContent.match(/viewBox="([^"]*)"/);
  if (!match) return { width: 800, height: 600 };
  const parts = match[1].trim().split(/\s+/);
  return {
    width: parseFloat(parts[2]) || 800,
    height: parseFloat(parts[3]) || 600,
  };
}

function buildHtml(svgContent, isJpeg) {
  const bodyStyle = isJpeg ? 'margin:0;padding:0;background:white;' : 'margin:0;padding:0;';
  return `<!DOCTYPE html>
<html>
<head>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
  <style>body { ${bodyStyle} }</style>
</head>
<body>
${svgContent}
</body>
</html>`;
}

async function main() {
  const browser = await chromium.launch();
  const context = await browser.newContext({ deviceScaleFactor: 2 });
  let success = 0;
  let failed = 0;

  for (const asset of assets) {
    const srcPath = path.join(BRAND_DIR, asset.src);
    const outPath = path.join(BRAND_DIR, asset.out);

    try {
      const svgContent = fs.readFileSync(srcPath, 'utf-8');
      const { width, height } = parseViewBox(svgContent);
      const isJpeg = asset.format === 'jpeg';

      const page = await context.newPage();
      await page.setViewportSize({ width, height });
      await page.setContent(buildHtml(svgContent, isJpeg), { waitUntil: 'networkidle' });
      await page.waitForFunction(() => document.fonts.ready);

      await page.screenshot({
        path: outPath,
        type: asset.format,
        quality: isJpeg ? 95 : undefined,
        clip: { x: 0, y: 0, width, height },
      });

      await page.close();
      console.log(`✓ ${asset.out}`);
      success++;
    } catch (err) {
      console.error(`✗ ${asset.src}: ${err.message}`);
      failed++;
    }
  }

  await browser.close();
  console.log(`\nDone: ${success} succeeded, ${failed} failed`);
}

main();
