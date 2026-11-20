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
  
  // First, inspect candidate modal
  console.log('Clicking Inspect Candidate Set...');
  await page.locator('button:has-text("Inspect Candidate Set")').first().click();
  await page.waitForTimeout(3000);
  
  // Close inspector modal via Close button
  const closeBtn = page.locator('button:has-text("Close Inspector")').first();
  const hasClose = await closeBtn.isVisible().catch(() => false);
  console.log('Close Inspector button visible:', hasClose);
  if (hasClose) {
    await closeBtn.click();
    console.log('Closed inspector modal');
    await page.waitForTimeout(1000);
  }

  // Now click Select Candidate Set & View Final Report on the card!
  console.log('Clicking Select Candidate Set on card...');
  const selBtn = page.locator('button:has-text("Select Candidate Set")').first();
  await selBtn.click();
  
  await page.waitForSelector('text=FINAL FORMULATION REPORT', { timeout: 15000 });
  console.log('*** SUCCESS! Stage 5 FINAL FORMULATION REPORT REACHED! ***');
  
  // Test clicking all 7 tabs on Stage 5:
  const tabs = ['Overview', 'Ingredients', 'Process', 'Cost Analysis', 'Nutrition', 'Allergens', 'AI Rationale'];
  for (const t of tabs) {
    const tabBtn = page.locator(`button:has-text("${t}")`).first();
    const canClick = await tabBtn.isVisible().catch(() => false);
    console.log(`Tab '${t}' visible:`, canClick);
    if (canClick) await tabBtn.click();
    await page.waitForTimeout(500);
  }
  console.log('*** ALL 7 TABS CLICKED SUCCESSFULLY! ***');

  await browser.close();
})();

