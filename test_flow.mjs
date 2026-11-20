import { chromium } from './Food Web App Core/frontend/node_modules/playwright-core/index.mjs';

(async () => {
  console.log('Testing 5-stage flow...');
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    headless: true
  });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('http://localhost:3000/dashboard/formulate/guided');
  
  // 1. Fill brief
  const brief = 'Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at most 28% sugar, creamy melt, rich vanilla and cocoa flavor, 12-month shelf life, and free from dairy ingredients.';
  await page.locator('textarea').fill(brief);
  console.log('1. Brief filled');
  
  // 2. Click analyze
  await page.locator('button:has-text("Analyze Brief")').first().click();
  console.log('2. Clicked Analyze Brief');
  await page.waitForSelector('text=AI-Recommended Constraints', { timeout: 25000 });
  console.log('3. Stage 2 reached: AI-Recommended Constraints visible');
  
  // 3. Click Configure Hard & Soft Constraints
  await page.locator('button:has-text("Configure Hard")').first().click();
  console.log('4. Clicked Configure Hard');
  await page.waitForSelector('text=Select Soft vs. Hard Constraints', { timeout: 15000 });
  console.log('5. Stage 3 reached: Select Soft vs. Hard Constraints visible');
  
  // 4. Click Run AI Formulation Search
  await page.locator('button:has-text("Run AI Formulation")').first().click();
  console.log('6. Clicked Run AI Formulation Search');
  await page.waitForSelector('text=Select Best Candidate Set', { timeout: 35000 });
  console.log('7. Stage 4 reached: Select Best Candidate Set visible');
  
  // 5. Click Inspect Candidate Set
  await page.locator('button:has-text("Inspect Candidate Set")').first().click();
  console.log('8. Opened Inspection Modal');
  await page.waitForTimeout(2000);
  
  // 6. Select candidate set inside modal
  const selectModalBtn = page.locator('button:has-text("Select This Candidate Set")').first();
  await selectModalBtn.click();
  console.log('9. Clicked Select This Candidate Set');
  await page.waitForSelector('text=FINAL FORMULATION REPORT', { timeout: 20000 });
  console.log('10. Stage 5 reached: FINAL FORMULATION REPORT visible!');

  await browser.close();
  console.log('*** ALL 5 STAGES VERIFIED AND FULLY FUNCTIONAL! ***');
})();
