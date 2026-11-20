import { chromium } from './Food Web App Core/frontend/node_modules/playwright-core/index.mjs';

(async () => {
  console.log('Verifying persistent sticky progress bar across all scroll positions and workflow steps...');
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    headless: true
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  
  await page.goto('http://localhost:3000/dashboard/formulate/guided', { waitUntil: 'networkidle' });

  async function verifyStickyStepper(stepName) {
    console.log(`\n--- Testing Step: ${stepName} ---`);
    // Find the sticky stepper element
    const stepperCard = page.locator('div.sticky');
    await stepperCard.waitFor({ state: 'visible' });

    // Helper to check bounding box
    async function checkVisibility(scrollLabel) {
      const box = await stepperCard.boundingBox();
      const isVisible = await stepperCard.isVisible();
      const windowScrollY = await page.evaluate(() => window.scrollY);
      console.log(`[${scrollLabel}] window.scrollY: ${windowScrollY}px | Stepper Y: ${box?.y.toFixed(1)}px | Height: ${box?.height.toFixed(1)}px | Visible: ${isVisible}`);
      
      // The global header height is 64px. The sticky stepper top must be at or very close to 64px when scrolled.
      if (windowScrollY > 100) {
        if (Math.abs(box.y - 64) > 10) {
          console.error(`FAILURE: Stepper Y (${box.y}) is not docked at top-16 (64px) below header!`);
          return false;
        }
      }
      if (!isVisible || box.y < 0) {
        console.error(`FAILURE: Stepper is out of view!`);
        return false;
      }
      return true;
    }

    // 1. Check at scroll position 0
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(300);
    let ok = await checkVisibility('Scroll 0');

    // 2. Scroll down 400px
    await page.evaluate(() => window.scrollTo(0, 400));
    await page.waitForTimeout(300);
    ok = ok && (await checkVisibility('Scroll 400px'));

    // 3. Scroll to the very bottom
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(300);
    ok = ok && (await checkVisibility('Scroll Bottom'));

    return ok;
  }

  // STEP 1
  let step1Ok = await verifyStickyStepper('Step 1: Product Brief');

  // Navigate to Step 2
  const brief = 'Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at most 28% sugar, creamy melt, rich vanilla and cocoa flavor, 12-month shelf life, and free from dairy ingredients.';
  await page.locator('textarea').fill(brief);
  // Button was renamed to "Start Formulating →"
  const startBtn = page.locator('button:has-text("Start Formulating")').first();
  await startBtn.click();
  await page.waitForSelector('text=AI-Recommended Constraints', { timeout: 30000 });
  
  // STEP 2
  let step2Ok = await verifyStickyStepper('Step 2: Constraint Discovery');

  // Navigate to Step 3
  await page.locator('button:has-text("Configure Hard")').first().click();
  await page.waitForSelector('text=Select Soft vs. Hard Constraints', { timeout: 15000 });

  // STEP 3
  let step3Ok = await verifyStickyStepper('Step 3: Hard / Soft Goals');

  // Navigate to Step 4
  await page.locator('button:has-text("Run AI Formulation")').first().click();
  await page.waitForSelector('text=Select Best Candidate Set', { timeout: 35000 });

  // STEP 4
  let step4Ok = await verifyStickyStepper('Step 4: Candidate Sets');

  // Open modal and select Set to go to Step 5
  await page.locator('button:has-text("Inspect Candidate Set")').first().click();
  await page.waitForTimeout(1500);
  await page.locator('button:has-text("Select This Candidate Set")').first().click();
  await page.waitForSelector('text=FINAL FORMULATION REPORT', { timeout: 25000 });

  // STEP 5
  let step5Ok = await verifyStickyStepper('Step 5: Final Report');

  await browser.close();

  console.log('\n=========================================');
  console.log(`Step 1 Result: ${step1Ok ? 'PASSED' : 'FAILED'}`);
  console.log(`Step 2 Result: ${step2Ok ? 'PASSED' : 'FAILED'}`);
  console.log(`Step 3 Result: ${step3Ok ? 'PASSED' : 'FAILED'}`);
  console.log(`Step 4 Result: ${step4Ok ? 'PASSED' : 'FAILED'}`);
  console.log(`Step 5 Result: ${step5Ok ? 'PASSED' : 'FAILED'}`);
  console.log('=========================================');

  if (step1Ok && step2Ok && step3Ok && step4Ok && step5Ok) {
    console.log('SUCCESS: All 5 formulation steps verified with persistent sticky progress bar!');
    process.exit(0);
  } else {
    process.exit(1);
  }
})();

