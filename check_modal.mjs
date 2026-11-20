import { chromium } from './Food Web App Core/frontend/node_modules/playwright-core/index.mjs';

(async () => {
  const browser = await chromium.launch({ executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  
  await page.goto('http://localhost:3000/dashboard/formulate/guided');
  const brief = 'Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at most 28% sugar, creamy melt, rich vanilla and cocoa flavor, 12-month shelf life, and free from dairy ingredients.';
  await page.locator('textarea').fill(brief);
  await page.locator('button:has-text("Analyze Brief")').first().click();
  await page.waitForSelector('text=AI-Recommended Constraints', { timeout: 25000 });
  await page.locator('button:has-text("Configure Hard")').first().click();
  await page.waitForSelector('text=Select Soft vs. Hard Constraints', { timeout: 15000 });
  await page.locator('button:has-text("Run AI Formulation")').first().click();
  await page.waitForSelector('text=Select Best Candidate Set', { timeout: 35000 });
  
  console.log('Clicking Inspect Candidate Set...');
  await page.locator('button:has-text("Inspect Candidate Set")').first().click();
  await page.waitForTimeout(2000);
  
  const b10 = await page.locator('button:has-text("10 KG")').isVisible();
  const b100 = await page.locator('button:has-text("100 KG")').isVisible();
  const b100g = await page.locator('button:has-text("100g (Basis)")').isVisible().catch(() => false);
  const b1000g = await page.locator('button:has-text("1,000g (1 kg)")').isVisible().catch(() => false);
  
  console.log('10 KG button visible:', b10);
  console.log('100 KG button visible:', b100);
  console.log('Old 100g button visible:', b100g);
  console.log('Old 1000g button visible:', b1000g);
  
  await page.screenshot({ path: 'modal_10kg_check.png' });
  console.log('Saved modal_10kg_check.png');
  
  // Click 100 KG
  console.log('Clicking 100 KG button...');
  await page.locator('button:has-text("100 KG")').click();
  await page.waitForTimeout(1000);
  await page.screenshot({ path: 'modal_100kg_check.png' });
  console.log('Saved modal_100kg_check.png');
  
  await browser.close();
})();
