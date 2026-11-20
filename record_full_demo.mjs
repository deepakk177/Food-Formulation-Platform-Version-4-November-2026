import { chromium } from './Food Web App Core/frontend/node_modules/playwright-core/index.mjs';
import fs from 'fs';
import path from 'path';

// Helper for human-like smooth mouse movement
async function smoothMove(page, targetX, targetY, steps = 25) {
  await page.mouse.move(targetX, targetY, { steps });
}

// Helper to smoothly scroll page
async function smoothScroll(page, deltaY, steps = 15, delayPerStep = 60) {
  for (let i = 0; i < steps; i++) {
    await page.evaluate((y) => window.scrollBy(0, y), deltaY / steps);
    await page.waitForTimeout(delayPerStep);
  }
}

// Helper to click an element smoothly with visual cursor feedback
async function smoothClick(page, selectorOrElement) {
  let el = typeof selectorOrElement === 'string' ? await page.waitForSelector(selectorOrElement, { state: 'visible', timeout: 10000 }) : selectorOrElement;
  const box = await el.boundingBox();
  if (box) {
    const targetX = box.x + box.width / 2;
    const targetY = box.y + box.height / 2;
    await page.mouse.move(targetX, targetY, { steps: 20 });
    await page.waitForTimeout(150);
    await page.mouse.down();
    await page.waitForTimeout(100);
    await page.mouse.up();
    await page.waitForTimeout(200);
  } else {
    await el.click();
  }
}

async function runDemoRecording() {
  const videoDir = path.resolve('demo_output/raw_video');
  if (fs.existsSync(videoDir)) {
    fs.rmSync(videoDir, { recursive: true, force: true });
  }
  fs.mkdirSync(videoDir, { recursive: true });

  console.log('[Recorder] Launching MS Edge browser for 1080p recording...');
  const browser = await chromium.launch({
    executablePath: 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe',
    headless: true,
    args: ['--window-size=1920,1080', '--disable-gpu']
  });

  const context = await browser.newContext({
    viewport: { width: 1920, height: 1080 },
    recordVideo: {
      dir: videoDir,
      size: { width: 1920, height: 1080 }
    }
  });

  // Inject visible custom mouse cursor dot
  await context.addInitScript(() => {
    window.addEventListener('DOMContentLoaded', () => {
      const cursor = document.createElement('div');
      cursor.id = 'demo-mouse-pointer';
      cursor.style.position = 'fixed';
      cursor.style.width = '20px';
      cursor.style.height = '20px';
      cursor.style.borderRadius = '50%';
      cursor.style.background = 'rgba(239, 68, 68, 0.85)';
      cursor.style.border = '2.5px solid white';
      cursor.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.5)';
      cursor.style.pointerEvents = 'none';
      cursor.style.zIndex = '2147483647';
      cursor.style.transform = 'translate(-50%, -50%)';
      cursor.style.transition = 'background 0.12s ease, transform 0.12s ease';
      document.body.appendChild(cursor);

      window.addEventListener('mousemove', (e) => {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
      });
      window.addEventListener('mousedown', () => {
        cursor.style.background = 'rgba(16, 185, 129, 0.9)';
        cursor.style.transform = 'translate(-50%, -50%) scale(0.8)';
      });
      window.addEventListener('mouseup', () => {
        cursor.style.background = 'rgba(239, 68, 68, 0.85)';
        cursor.style.transform = 'translate(-50%, -50%) scale(1.0)';
      });
    });
  });

  const page = await context.newPage();

  // =========================================================================
  // SCENE 1: Platform Introduction & Landing Page (55.0s)
  // =========================================================================
  console.log('=== SCENE 1: Platform Introduction & Landing Page (55.0s) ===');
  await page.goto('http://localhost:3000/');
  await page.waitForTimeout(3000);
  await smoothMove(page, 500, 350, 20);
  await page.waitForTimeout(4000);

  // Smooth scroll down to view architecture and capabilities
  await smoothScroll(page, 700, 25, 60);
  await page.waitForTimeout(8000);
  await smoothScroll(page, 800, 25, 60);
  await page.waitForTimeout(10000);
  await smoothScroll(page, 700, 25, 60);
  await page.waitForTimeout(8000);

  // Smooth scroll back to top
  await smoothScroll(page, -2200, 30, 40);
  await page.waitForTimeout(4000);

  // Click Go to Dashboard button
  const dashBtn = await page.waitForSelector('text=Go to Dashboard', { timeout: 10000 }).catch(() => null);
  if (dashBtn) {
    await smoothClick(page, dashBtn);
  } else {
    await page.goto('http://localhost:3000/dashboard');
  }
  await page.waitForTimeout(5000);

  // =========================================================================
  // SCENE 2: Central Command Dashboard & Workspace Overview (54.0s)
  // =========================================================================
  console.log('=== SCENE 2: Central Command Dashboard & Workspace Overview (54.0s) ===');
  await page.waitForSelector('text=Dashboard', { timeout: 10000 });
  await page.waitForTimeout(4000);

  // Hover over sidebar items
  await smoothMove(page, 120, 200, 20); // Dashboard
  await page.waitForTimeout(3000);
  await smoothMove(page, 120, 250, 20); // Formulate
  await page.waitForTimeout(3000);
  await smoothMove(page, 120, 300, 20); // Ingredients
  await page.waitForTimeout(3000);
  await smoothMove(page, 120, 350, 20); // Knowledge Graph
  await page.waitForTimeout(3000);
  await smoothMove(page, 120, 400, 20); // Compliance
  await page.waitForTimeout(3000);

  // Move over KPI cards
  await smoothMove(page, 500, 200, 25);
  await page.waitForTimeout(4000);
  await smoothMove(page, 800, 200, 25);
  await page.waitForTimeout(4000);

  // Scroll down to view projects table
  await smoothScroll(page, 450, 20, 60);
  await page.waitForTimeout(12000);

  // Scroll back up and navigate to Guided Formulator
  await smoothScroll(page, -450, 20, 50);
  await page.waitForTimeout(3000);
  await page.goto('http://localhost:3000/dashboard/formulate/guided');
  await page.waitForTimeout(4000);

  // =========================================================================
  // SCENE 3: Stage 1: Natural Language Product Brief Submission (60.8s)
  // =========================================================================
  console.log('=== SCENE 3: Stage 1: Natural Language Product Brief Submission (60.8s) ===');
  await page.waitForSelector('text=Product Brief', { timeout: 10000 });
  await page.waitForTimeout(4000);

  // Focus on the pinned stage bar
  await smoothMove(page, 400, 100, 20);
  await page.waitForTimeout(3000);

  // Fill the exact user brief
  const briefInput = await page.waitForSelector('textarea', { timeout: 10000 });
  await smoothClick(page, briefInput);
  await page.evaluate(() => {
    const el = document.querySelector('textarea');
    if (el) el.value = '';
  });
  await page.waitForTimeout(1000);

  const userBrief = "Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at most 28% sugar, creamy melt, rich vanilla and cocoa flavor, 12-month shelf life, and free from dairy ingredients.";
  await briefInput.type(userBrief, { delay: 45 });
  await page.waitForTimeout(5000);

  // Smooth scroll down to the Analyze Brief button
  await smoothScroll(page, 250, 15, 60);
  await page.waitForTimeout(4000);

  // Click Analyze Brief button
  const analyzeBtn = page.locator('button:has-text("Analyze Brief")').first();
  await analyzeBtn.click();
  console.log('[Recorder] Clicked Analyze Brief button. Waiting for Stage 2...');
  
  // Wait for transition to Stage 2
  await page.waitForSelector('text=AI-Recommended Constraints', { timeout: 25000 });
  await page.waitForTimeout(12000);

  // =========================================================================
  // SCENE 4: Stage 2: Automated Constraint Discovery & Entity Extraction (55.4s)
  // =========================================================================
  console.log('=== SCENE 4: Stage 2: Automated Constraint Discovery & Entity Extraction (55.4s) ===');
  await smoothMove(page, 600, 280, 25);
  await page.waitForTimeout(5000);

  // Scroll through constraints
  await smoothScroll(page, 350, 20, 60);
  await page.waitForTimeout(10000);
  await smoothScroll(page, 300, 20, 60);
  await page.waitForTimeout(12000);

  // Click Configure Hard & Soft Constraints button
  console.log('[Recorder] Advancing to Stage 3...');
  const toStage3Btn = page.locator('button:has-text("Configure Hard")').first();
  await toStage3Btn.click();
  await page.waitForSelector('text=Select Soft vs. Hard Constraints', { timeout: 15000 });
  await page.waitForTimeout(5000);

  // =========================================================================
  // SCENE 5: Stage 3: Hard Constraints & Soft Objectives Prioritization (52.7s)
  // =========================================================================
  console.log('=== SCENE 5: Stage 3: Hard Constraints & Soft Objectives Prioritization (52.7s) ===');
  // Inspect Hard constraints table
  await smoothMove(page, 500, 320, 20);
  await page.waitForTimeout(6000);

  // Scroll down to soft objectives
  await smoothScroll(page, 400, 20, 60);
  await page.waitForTimeout(10000);

  // Move cursor over toggles / sliders
  await smoothMove(page, 750, 600, 20);
  await page.waitForTimeout(6000);

  // Click Run AI Formulation Search
  console.log('[Recorder] Running AI Formulation Search...');
  const runSearchBtn = page.locator('button:has-text("Run AI Formulation")').first();
  await runSearchBtn.click();

  // Wait for transition to Stage 4
  await page.waitForSelector('text=Select Best Candidate Set', { timeout: 35000 });
  await page.waitForTimeout(8000);

  // =========================================================================
  // SCENE 6: Stage 4: Pareto Candidate Generation & Deep-Dive Inspection (68.0s)
  // =========================================================================
  console.log('=== SCENE 6: Stage 4: Pareto Candidate Generation & Deep-Dive Inspection (68.0s) ===');
  // Hover over the first candidate card
  await smoothMove(page, 450, 350, 20);
  await page.waitForTimeout(6000);
  // Hover over second candidate card
  await smoothMove(page, 850, 350, 20);
  await page.waitForTimeout(6000);

  // Click Inspect Candidate Set button on Candidate 1
  console.log('[Recorder] Opening Candidate Inspection Modal...');
  const inspectBtn = page.locator('button:has-text("Inspect Candidate Set")').first();
  await inspectBtn.click();
  await page.waitForSelector('div.fixed.inset-0', { timeout: 10000 });
  await page.waitForTimeout(6000);

  // Inside Modal: scroll down through ingredients matrix
  await smoothScroll(page, 250, 15, 60);
  await page.waitForTimeout(8000);

  // Switch to radar/strategy tab inside modal
  const strategyTab = page.locator('div.fixed.inset-0 button:has-text("Why"), div.fixed.inset-0 button:has-text("Strategy")').first();
  const hasStrat = await strategyTab.isVisible().catch(() => false);
  if (hasStrat) {
    await strategyTab.click();
    await page.waitForTimeout(6000);
  }

  // Click "Select This Candidate Set & View Final Report" button inside modal!
  console.log('[Recorder] Selecting Candidate Set from modal...');
  const modalSelectBtn = page.locator('div.fixed.inset-0 button:has-text("Select This Candidate Set")').first();
  await modalSelectBtn.click();

  // Wait for transition to Stage 5
  await page.waitForSelector('text=FINAL FORMULATION REPORT', { timeout: 20000 });
  await page.waitForTimeout(6000);

  // =========================================================================
  // SCENE 7: Stage 5: Final Formulation Dossier (All 7 Analytical Tabs) (101.6s)
  // =========================================================================
  console.log('=== SCENE 7: Stage 5: Final Formulation Dossier (All 7 Analytical Tabs) (101.6s) ===');
  // Tab 1: Overview
  console.log(' - Demonstrating Tab 1: Overview');
  await smoothMove(page, 500, 350, 20);
  await page.waitForTimeout(3000);
  await smoothScroll(page, 300, 15, 60);
  await page.waitForTimeout(5000);
  await smoothScroll(page, -300, 15, 50);
  await page.waitForTimeout(2000);

  // Tab 2: Ingredients
  console.log(' - Demonstrating Tab 2: Ingredients');
  const ingTab = page.locator('button:has-text("Ingredients")').first();
  await ingTab.click();
  await page.waitForTimeout(3000);
  await smoothScroll(page, 350, 15, 60);
  await page.waitForTimeout(7000);
  await smoothScroll(page, -350, 15, 50);
  await page.waitForTimeout(2000);

  // Tab 3: Process
  console.log(' - Demonstrating Tab 3: Process');
  const procTab = page.locator('button:has-text("Process")').first();
  await procTab.click();
  await page.waitForTimeout(3000);
  await smoothScroll(page, 300, 15, 60);
  await page.waitForTimeout(6000);
  await smoothScroll(page, -300, 15, 50);
  await page.waitForTimeout(2000);

  // Tab 4: Cost Analysis
  console.log(' - Demonstrating Tab 4: Cost Analysis');
  const costTab = page.locator('button:has-text("Cost Analysis")').first();
  await costTab.click();
  await page.waitForTimeout(3000);
  await smoothScroll(page, 300, 15, 60);
  await page.waitForTimeout(6000);
  await smoothScroll(page, -300, 15, 50);
  await page.waitForTimeout(2000);

  // Tab 5: Nutrition
  console.log(' - Demonstrating Tab 5: Nutrition');
  const nutrTab = page.locator('button:has-text("Nutrition")').first();
  await nutrTab.click();
  await page.waitForTimeout(3000);
  await smoothScroll(page, 300, 15, 60);
  await page.waitForTimeout(6000);
  await smoothScroll(page, -300, 15, 50);
  await page.waitForTimeout(2000);

  // Tab 6: Allergens & Compliance
  console.log(' - Demonstrating Tab 6: Allergens & Compliance');
  const allTab = page.locator('button:has-text("Allergens")').first();
  await allTab.click();
  await page.waitForTimeout(3000);
  await smoothScroll(page, 300, 15, 60);
  await page.waitForTimeout(6000);
  await smoothScroll(page, -300, 15, 50);
  await page.waitForTimeout(2000);

  // Tab 7: AI Rationale
  console.log(' - Demonstrating Tab 7: AI Rationale');
  const ratTab = page.locator('button:has-text("AI Rationale")').first();
  await ratTab.click();
  await page.waitForTimeout(3000);
  await smoothScroll(page, 300, 15, 60);
  await page.waitForTimeout(6000);
  await smoothScroll(page, -300, 15, 50);
  await page.waitForTimeout(2000);

  // Demonstrate pinned stage bar
  console.log(' - Demonstrating persistent pinned stage bar navigation');
  const stage2Circle = page.locator('button:has-text("Constraint Discovery"), button:has-text("2")').first();
  await stage2Circle.click();
  await page.waitForTimeout(3000);
  const stage5Circle = page.locator('button:has-text("Final Report"), button:has-text("5")').first();
  await stage5Circle.click();
  await page.waitForTimeout(4000);

  // =========================================================================
  // SCENE 8: Knowledge Graph Explorer & Semantic Traversal (53.9s)
  // =========================================================================
  console.log('=== SCENE 8: Knowledge Graph Explorer & Semantic Traversal (53.9s) ===');
  await page.goto('http://localhost:3000/dashboard/knowledge-graph');
  await page.waitForSelector('text=Knowledge Graph', { timeout: 15000 });
  await page.waitForTimeout(4000);

  // Point out node count and filters
  await smoothMove(page, 300, 180, 20);
  await page.waitForTimeout(5000);

  // Click filter buttons
  const ingFilterBtn = page.locator('button:has-text("Ingredients"), button:has-text("Nodes")').first();
  const hasFilter = await ingFilterBtn.isVisible().catch(() => false);
  if (hasFilter) {
    await ingFilterBtn.click();
    await page.waitForTimeout(4000);
  }

  // Search input in Knowledge Graph
  const kgSearch = page.locator('input[type="text"], input[placeholder*="Search"]').first();
  const hasKgSearch = await kgSearch.isVisible().catch(() => false);
  if (hasKgSearch) {
    await kgSearch.click();
    await kgSearch.type('Cocoa Butter', { delay: 60 });
    await page.waitForTimeout(6000);
  }

  // Pan / inspect graph canvas
  await smoothMove(page, 960, 540, 25);
  await page.mouse.down();
  await smoothMove(page, 1020, 580, 20);
  await page.mouse.up();
  await page.waitForTimeout(18000);

  // =========================================================================
  // SCENE 9: Comprehensive Ingredient Library & Specification Drawer (53.8s)
  // =========================================================================
  console.log('=== SCENE 9: Comprehensive Ingredient Library & Specification Drawer (53.8s) ===');
  await page.goto('http://localhost:3000/dashboard/ingredients');
  await page.waitForSelector('text=Ingredient', { timeout: 15000 });
  await page.waitForTimeout(4000);

  // Category filtering
  const proteinBtn = page.locator('button:has-text("Proteins"), button:has-text("Protein")').first();
  if (await proteinBtn.isVisible().catch(() => false)) {
    await proteinBtn.click();
    await page.waitForTimeout(4000);
  }

  const fatsBtn = page.locator('button:has-text("Fats & Oils"), button:has-text("Fats")').first();
  if (await fatsBtn.isVisible().catch(() => false)) {
    await fatsBtn.click();
    await page.waitForTimeout(4000);
  }

  // Type search in ingredient catalog
  const ingSearchInput = page.locator('input[placeholder*="Search"], input[type="text"]').first();
  if (await ingSearchInput.isVisible().catch(() => false)) {
    await ingSearchInput.click();
    await ingSearchInput.fill('');
    await ingSearchInput.type('Cocoa Butter', { delay: 60 });
    await page.waitForTimeout(5000);
  }

  // Click ingredient row to open slide-over drawer
  const firstRow = page.locator('tr.cursor-pointer, div.cursor-pointer, text=Cocoa Butter').first();
  if (await firstRow.isVisible().catch(() => false)) {
    await firstRow.click();
    console.log('[Recorder] Opened Ingredient Specification Drawer');
    await page.waitForTimeout(6000);
    await smoothScroll(page, 200, 15, 60);
    await page.waitForTimeout(10000);
    await smoothScroll(page, -200, 15, 50);
    await page.waitForTimeout(4000);
  }

  // =========================================================================
  // SCENE 10: User Profile, Laboratory Settings & Formulation History (40.6s)
  // =========================================================================
  console.log('=== SCENE 10: User Profile, Laboratory Settings & Formulation History (40.6s) ===');
  await page.goto('http://localhost:3000/dashboard/profile');
  await page.waitForTimeout(4000);

  // Inspect profile information
  await smoothMove(page, 450, 250, 20);
  await page.waitForTimeout(6000);
  await smoothScroll(page, 300, 15, 60);
  await page.waitForTimeout(14000);
  await smoothScroll(page, -300, 15, 50);
  await page.waitForTimeout(6000);

  // =========================================================================
  // SCENE 11: Closing Summary & Dashboard Return (35.2s)
  // =========================================================================
  console.log('=== SCENE 11: Closing Summary & Dashboard Return (35.2s) ===');
  await page.goto('http://localhost:3000/dashboard');
  await page.waitForSelector('text=Dashboard', { timeout: 10000 });
  await page.waitForTimeout(4000);

  // Smooth celebratory pan across dashboard
  await smoothMove(page, 500, 220, 25);
  await page.waitForTimeout(5000);
  await smoothScroll(page, 200, 15, 60);
  await page.waitForTimeout(12000);
  await smoothScroll(page, -200, 15, 50);
  await page.waitForTimeout(6000);

  console.log('[Recorder] Finishing recording session and closing browser context...');
  await page.close();
  await context.close();
  await browser.close();
  console.log('[Recorder] Browser closed successfully! Video file finalized in demo_output/raw_video');
}

runDemoRecording().catch(err => {
  console.error('[Recorder Error]:', err);
  process.exit(1);
});
