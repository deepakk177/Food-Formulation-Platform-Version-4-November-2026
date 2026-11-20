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
  
  console.log('Clicking Select inside modal...');
  await page.locator('div.fixed.inset-0 button:has-text("Select This Candidate Set")').click();
  
  await page.waitForSelector('text=FINAL FORMULATION REPORT', { timeout: 15000 });
  console.log('*** STAGE 5 REACHED SUCCESSFULLY VIA MODAL BUTTON! ***');
  
  await browser.close();
})();

