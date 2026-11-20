/**
 * Authoritative Benchmark Briefs - Shared Single Source of Truth
 * Used by both Dashboard and Guided Formulation Workflow pages.
 */

export interface BenchmarkBrief {
  id: string;
  title: string;
  category: string;
  text: string;
  tag?: string;
}

export const RESEARCH_BENCHMARK_BRIEFS: BenchmarkBrief[] = [
  {
    id: 'exp-001-vegan-chocolate',
    title: 'EXP-001: High-Protein Vegan Chocolate Bar',
    category: 'Confectionery & Functional Bars',
    text: 'Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at most 28% sugar, creamy melt, rich vanilla and cocoa flavor, 12-month shelf life, and free from dairy ingredients.',
    tag: 'Functional Confectionery'
  },
  {
    id: 'prebiotic-citrus-beverage',
    title: 'Low-Sugar Prebiotic Citrus Beverage',
    category: 'Functional Beverages',
    text: 'Formulate a refreshing sparkling citrus beverage with at least 5g prebiotic dietary fiber, under 4g total sugar per serving, and a refreshing citrus flavor profile.',
    tag: 'Functional Beverage'
  },
  {
    id: 'digestive-oat-bar',
    title: 'High-Fibre Gluten-Free Digestive Oat Bar',
    category: 'Bakery & Cereals',
    text: 'Develop a soft-baked gluten-free oat bar with at least 8g dietary fiber, at least 10g plant-based protein, and appropriate nutritional and product-quality requirements.',
    tag: 'Baked Nutrition'
  }
];

export const STORAGE_KEY_PRODUCT_BRIEF = 'formulation_product_brief';
