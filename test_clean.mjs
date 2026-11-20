import { chromium } from './Food Web App Core/frontend/node_modules/playwright-core/index.mjs';

(async () => {
  console.log('Testing clean flow without modal hang...');
  const browser = await chromium.launch({ executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe', headless: true });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('http://localhost:3000/dashboard/formulate/guided');
  
  const brief = 'Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at most 28% sugar, creamy melt, rich vanilla and cocoa flavor, 12-month shelf life, and free from dairy ingredients.';
  await page.locator('textarea').fill(brief);
  console.log('1. Brief filled');

  await page.locator('button:has-text("Analyze Brief")').first().click();
  await page.waitForSelector('text=AI-Recommended Constraints', { timeout: 25000 });
  console.log('2. Stage 2 reached');

  await page.locator('button:has-text("Configure Hard")').first().click();
  await page.waitForSelector('text=Select Soft vs. Hard Constraints', { timeout: 15000 });
  console.log('3. Stage 3 reached');

  await page.locator('button:has-text("Run AI Formulation")').first().click();
  await page.waitForSelector('text=Select Best Candidate Set', { timeout: 35000 });
  console.log('4. Stage 4 reached');

  // Test opening modal
  console.log('Opening inspection modal...');
  await page.locator('button:has-text("Inspect Candidate Set")').first().click();
  await page.waitForTimeout(2000);

  // Close modal via the X button at the top right!
  console.log('Closing modal via X button...');
  await page.locator('button[aria-label="Close modal"]').click();
  await page.waitForTimeout(1000);
  console.log('Modal closed!');

  // Now click Candidate 1 card selection button
  console.log('Clicking Select Candidate Set on card...');
  await page.locator('button:has-text("Select Candidate Set & View Final Report")').first().click();
  
  await page.waitForSelector('text=FINAL FORMULATION REPORT', { timeout: 15000 });
  console.log('5. Stage 5 reached!');

  // Click tabs
  const tabs = ['Ingredients', 'Process', 'Cost Analysis', 'Nutrition', 'Allergens', 'AI Rationale', 'Overview'];
  for (const t of tabs) {
    console.log(`Clicking tab ${t}...`);
    await page.locator(`button:has-text("${t}")`).first().click();
    await page.waitForTimeout(1000);
  }

  await browser.close();
  console.log('*** COMPLETE 5-STAGE FLOW VERIFIED 100%! ***');
})();

