/**
 * Canonical Ingredient & Formulation Formatting Helpers
 * Single source of truth for amount formatting, unit conversions, and cost representation.
 */

/**
 * Formats ingredient quantities cleanly in a single line without wrapping.
 * - Under 1 kg: formatted in grams (e.g. 0.500 kg -> '500 g', 0.080 kg -> '80 g')
 * - 1 kg and above: formatted in kg with max 2 decimal places and trailing zeros removed (e.g. 2.77 kg -> '2.77 kg', 1.00 kg -> '1 kg')
 * - Does not modify the underlying raw floating-point value.
 */
export function formatIngredientAmount(qtyKg: number): string {
  if (typeof qtyKg !== 'number' || isNaN(qtyKg) || qtyKg < 0) return '0 g';
  if (qtyKg === 0) return '0 g';

  if (qtyKg < 1) {
    const grams = qtyKg * 1000;
    const roundedGrams = parseFloat(grams.toFixed(2));
    return `${roundedGrams} g`;
  } else {
    const roundedKg = parseFloat(qtyKg.toFixed(2));
    return `${roundedKg} kg`;
  }
}

/**
 * Formats ingredient cost per kg with zero-cost prevention.
 * Unverified or missing costs are represented explicitly as 'Cost Data Unavailable' (never silently $0).
 */
export function formatIngredientCostPerKg(
  costPerKg: number | null | undefined,
  isVerifiedZero: boolean = false
): { display: string; isAvailable: boolean } {
  if (costPerKg === null || costPerKg === undefined || isNaN(Number(costPerKg))) {
    return { display: 'Cost Data Unavailable', isAvailable: false };
  }
  const num = Number(costPerKg);
  if (num < 0) {
    return { display: 'Cost Data Unavailable', isAvailable: false };
  }
  if (num === 0 && !isVerifiedZero) {
    return { display: 'Cost Data Unavailable', isAvailable: false };
  }
  return { display: `$${num.toFixed(2)}`, isAvailable: true };
}

/**
 * Formats batch cost with zero-cost prevention.
 */
export function formatBatchCost(
  costUSD: number | null | undefined,
  isVerifiedZero: boolean = false
): { display: string; isAvailable: boolean } {
  if (costUSD === null || costUSD === undefined || isNaN(Number(costUSD))) {
    return { display: 'Cost Data Unavailable', isAvailable: false };
  }
  const num = Number(costUSD);
  if (num < 0) {
    return { display: 'Cost Data Unavailable', isAvailable: false };
  }
  if (num === 0 && !isVerifiedZero) {
    return { display: 'Cost Data Unavailable', isAvailable: false };
  }
  return { display: `$${num.toFixed(2)}`, isAvailable: true };
}
