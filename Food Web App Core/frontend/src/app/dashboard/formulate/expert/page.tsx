'use client';

import React, { useState, useEffect } from 'react';
import { useStore, Ingredient } from '@/store/useStore';
import { useRouter } from 'next/navigation';
import { 
  Activity, AlertCircle, Award, CheckCircle2, ChevronRight, HelpCircle, 
  Layers, Loader2, Plus, Search, Sparkles, Trash2 
} from 'lucide-react';
import FormulationResults from '@/components/formulation-results';

interface ChosenIngredient extends Ingredient {
  percentage: number;
}

export default function ExpertFormulator() {
  const { token, ingredients, fetchIngredients } = useStore();
  const router = useRouter();

  const [search, setSearch] = useState('');
  const [selectedRole, setSelectedRole] = useState('All');
  const [chosen, setChosen] = useState<ChosenIngredient[]>([]);
  const [macros, setMacros] = useState({ protein: 0, fat: 0, carbs: 0, calories: 0 });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState<any>(null);

  useEffect(() => {
    if (!token) {
      router.push('/login');
    } else {
      fetchIngredients();
    }
  }, [token, router, fetchIngredients]);

  // Recalculate macro contributions dynamically in client-side runtime
  useEffect(() => {
    const totals = chosen.reduce(
      (acc, x) => {
        const factor = x.percentage / 100;
        return {
          protein: acc.protein + x.protein * factor,
          fat: acc.fat + x.fat * factor,
          carbs: acc.carbs + x.carbs * factor,
          calories: acc.calories + x.calories * factor,
        };
      },
      { protein: 0, fat: 0, carbs: 0, calories: 0 }
    );
    setMacros(totals);
  }, [chosen]);

  const addIngredient = (ing: Ingredient) => {
    if (chosen.find((x) => x.name === ing.name)) return;
    setChosen([...chosen, { ...ing, percentage: 10.0 }]);
  };

  const removeIngredient = (name: string) => {
    setChosen(chosen.filter((x) => x.name !== name));
  };

  const updatePercentage = (name: string, value: number) => {
    setChosen(
      chosen.map((x) => (x.name === name ? { ...x, percentage: value } : x))
    );
  };

  const distributeEqually = () => {
    if (chosen.length === 0) return;
    const equalShare = parseFloat((100 / chosen.length).toFixed(2));
    setChosen(chosen.map((x) => ({ ...x, percentage: equalShare })));
  };

  const totalPercentage = chosen.reduce((sum, x) => sum + x.percentage, 0);

  const handleRunCompliance = async () => {
    if (Math.abs(totalPercentage - 100.0) > 0.05) {
      setError('Formula unbalanced! Ratios must sum to exactly 100.00% to run validations.');
      return;
    }
    setLoading(true);
    setError('');
    
    // Group into bulk and functional compositions
    const bulk = chosen.filter(x => x.category === 'Protein Source' || x.category === 'Bulking Agent' || x.category === 'Lipid Source').map(x => ({
      name: x.name,
      category: x.category,
      percentage: x.percentage
    }));
    const functional = chosen.filter(x => x.category !== 'Protein Source' && x.category !== 'Bulking Agent' && x.category !== 'Lipid Source').map(x => ({
      name: x.name,
      functional_role: x.functional_role,
      percentage: x.percentage
    }));

    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const composition = { bulk_ingredients: bulk, functional_ingredients: functional };
      const res = await fetch(`${api_url}/api/formulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: `Expert balance: ${chosen.map(x => `${x.name} (${x.percentage}%)`).join(', ')}`,
          composition: composition,
          constraints: {
            vegan: chosen.some(x => x.allergen === 'Milk' || x.allergen === 'Egg') ? false : true,
            gluten_free: chosen.some(x => x.allergen === 'Gluten') ? false : true
          }
        }),
      });
      if (!res.ok) {
        throw new Error('Compliance validation engine returned an error status.');
      }
      const data = await res.json();
      setResults(data);
    } catch (err: any) {
      setError(err.message || 'Validation request failed');
    } finally {
      setLoading(false);
    }
  };

  const roles = ['All', 'Protein Source', 'Bulking Agent', 'Emulsifier', 'Stabilizer', 'Sweetener', 'Flavor System', 'Acidity Control', 'Preservation'];

  const filteredCatalog = ingredients.filter((ing) => {
    const matchSearch = ing.name.toLowerCase().includes(search.toLowerCase()) || ing.functional_role.toLowerCase().includes(search.toLowerCase());
    const matchRole = selectedRole === 'All' || ing.functional_role === selectedRole;
    return matchSearch && matchRole;
  });

  if (results) {
    return (
      <div className="py-8 px-4 max-w-5xl mx-auto">
        <FormulationResults data={results} onReset={() => setResults(null)} />
      </div>
    );
  }

  return (
    <div className="grid grid-cols-12 gap-6 py-8 relative z-10 px-4">
      {/* Sidebar: Catalog Explorer */}
      <div className="col-span-12 lg:col-span-4 space-y-4">
        <div className="glass-panel p-5 rounded-2xl border border-slate-900 flex flex-col h-[650px]">
          <div>
            <span className="text-[10px] font-mono text-indigo-400 font-bold uppercase tracking-widest">Expert Canvas</span>
            <h3 className="text-lg font-bold text-white mt-1">Ingredient Catalog</h3>
            <p className="text-slate-500 text-xs mt-0.5">Click components to append them to your balancing list.</p>
          </div>

          <div className="relative mt-4">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-500" />
            <input
              type="text"
              placeholder="Search components..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-4 py-2 bg-slate-950/80 border border-slate-800 rounded-xl text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 transition text-xs"
            />
          </div>

          <div className="flex gap-1.5 overflow-x-auto py-3 scrollbar-none">
            {roles.map((role) => (
              <button
                key={role}
                onClick={() => setSelectedRole(role)}
                className={`px-3 py-1.5 rounded-full text-[10px] font-bold whitespace-nowrap border transition ${
                  selectedRole === role
                    ? 'bg-indigo-600 border-indigo-500 text-white'
                    : 'bg-slate-950 border-slate-800 text-slate-400 hover:text-white'
                }`}
              >
                {role}
              </button>
            ))}
          </div>

          <div className="flex-1 overflow-y-auto space-y-2 mt-2 pr-1">
            {filteredCatalog.map((ing) => (
              <div
                key={ing.name}
                className="flex items-center justify-between p-3 rounded-xl bg-slate-950 border border-slate-850 hover:border-slate-700 transition"
              >
                <div>
                  <div className="font-semibold text-xs text-white">{ing.name}</div>
                  <div className="text-[10px] text-indigo-400 font-mono mt-0.5">{ing.functional_role}</div>
                </div>
                <button
                  onClick={() => addIngredient(ing)}
                  className="p-1 rounded-lg bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 hover:bg-indigo-600 hover:text-white transition"
                  title="Add to canvas"
                >
                  <Plus className="h-4 w-4" />
                </button>
              </div>
            ))}
            {filteredCatalog.length === 0 && (
              <div className="text-center py-12 text-slate-500 text-xs">No ingredients match query filters.</div>
            )}
          </div>
        </div>
      </div>

      {/* Main Workspace: Balancing Canvas */}
      <div className="col-span-12 lg:col-span-8 space-y-6">
        {error && (
          <div className="rounded-xl bg-red-950/20 border border-red-800/50 p-4 text-xs text-red-400">
            {error}
          </div>
        )}

        <div className="glass-panel p-6 rounded-2xl border border-slate-900">
          <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4 border-b border-slate-900 pb-4 mb-6">
            <div>
              <h2 className="text-xl font-extrabold text-white flex items-center gap-2">
                <Layers className="h-5 w-5 text-indigo-400" />
                Formulation Composer
              </h2>
              <p className="text-slate-500 text-xs mt-0.5">Tweak proportions using ranges sliders. Ensure total sums to 100%.</p>
            </div>
            
            <div className="flex items-center gap-4">
              <button 
                onClick={distributeEqually}
                className="px-3 py-1.5 border border-slate-800 hover:border-slate-700 rounded-lg text-slate-400 hover:text-white transition text-xs font-semibold"
              >
                Distribute Equally
              </button>
              <div className="font-mono text-xs">
                Total Share: 
                <span className={`ml-2 font-bold px-2 py-0.5 rounded ${
                  Math.abs(totalPercentage - 100) < 0.05 
                    ? 'bg-emerald-950/30 text-emerald-400 border border-emerald-900/50' 
                    : 'bg-yellow-950/30 text-yellow-400 border border-yellow-900/50'
                }`}>
                  {totalPercentage.toFixed(2)}%
                </span>
              </div>
            </div>
          </div>

          <div className="space-y-4 max-h-[350px] overflow-y-auto pr-1">
            {chosen.length === 0 ? (
              <div className="text-center py-16 text-slate-500 text-xs">
                Your balancing canvas is empty. Select ingredients from the sidebar catalog catalog.
              </div>
            ) : (
              chosen.map((ing) => (
                <div key={ing.name} className="p-4 rounded-xl bg-slate-950 border border-slate-850 space-y-3">
                  <div className="flex justify-between items-center text-xs">
                    <div>
                      <span className="font-semibold text-white">{ing.name}</span>
                      <span className="ml-2 text-[9px] px-2 py-0.5 rounded bg-slate-900 text-indigo-400 font-mono">
                        {ing.functional_role}
                      </span>
                      {ing.allergen !== 'None' && (
                        <span className="ml-1.5 text-[9px] px-2 py-0.5 rounded bg-red-950/20 text-red-400 font-mono">
                          {ing.allergen}
                        </span>
                      )}
                    </div>
                    <div className="flex items-center gap-3">
                      <span className="font-mono font-bold text-white">{ing.percentage.toFixed(1)}%</span>
                      <button 
                        onClick={() => removeIngredient(ing.name)}
                        className="text-slate-600 hover:text-red-400 transition"
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </div>
                  </div>

                  <div className="flex gap-4 items-center">
                    <input
                      type="range"
                      min={0}
                      max={100}
                      step={0.1}
                      value={ing.percentage}
                      onChange={(e) => updatePercentage(ing.name, parseFloat(e.target.value))}
                      className="flex-1 accent-indigo-500 h-1 bg-slate-900 rounded-lg appearance-none cursor-pointer"
                    />
                  </div>
                </div>
              ))
            )}
          </div>

          {/* Macro Prediction Panel */}
          <div className="grid grid-cols-4 gap-4 mt-6 pt-6 border-t border-slate-900">
            <div className="p-3 bg-slate-950 border border-slate-850 rounded-xl text-center">
              <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider block">Protein</span>
              <div className="text-lg font-mono font-extrabold text-indigo-400 mt-1">{macros.protein.toFixed(1)}g</div>
            </div>
            <div className="p-3 bg-slate-950 border border-slate-850 rounded-xl text-center">
              <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider block">Fat</span>
              <div className="text-lg font-mono font-extrabold text-pink-400 mt-1">{macros.fat.toFixed(1)}g</div>
            </div>
            <div className="p-3 bg-slate-950 border border-slate-850 rounded-xl text-center">
              <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider block">Carbs</span>
              <div className="text-lg font-mono font-extrabold text-yellow-500 mt-1">{macros.carbs.toFixed(1)}g</div>
            </div>
            <div className="p-3 bg-slate-950 border border-slate-850 rounded-xl text-center">
              <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider block">Energy</span>
              <div className="text-lg font-mono font-extrabold text-emerald-400 mt-1">{macros.calories.toFixed(0)} kcal</div>
            </div>
          </div>

          {/* Warning Box */}
          {Math.abs(totalPercentage - 100) > 0.05 && chosen.length > 0 && (
            <div className="flex gap-2.5 p-4 rounded-xl bg-yellow-950/15 border border-yellow-900/40 text-yellow-400 text-xs mt-6 leading-relaxed">
              <AlertCircle className="h-4.5 w-4.5 shrink-0 mt-0.5" />
              <span>
                Attention: The compound ratios sum to {totalPercentage.toFixed(2)}%. Compounding simulation checks and LLM verification requires exactly 100.00% to run compliance checks.
              </span>
            </div>
          )}

          {/* Trigger validation */}
          {Math.abs(totalPercentage - 100) <= 0.05 && chosen.length > 0 && (
            <div className="flex gap-4 mt-6">
              <button
                onClick={handleRunCompliance}
                disabled={loading}
                className="w-full flex items-center justify-center gap-1.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 py-3 text-xs font-semibold text-white hover:opacity-95 transition disabled:opacity-50"
              >
                {loading ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    Running Audit Audits...
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="h-4 w-4" />
                    Validate Regional Compliance & Save
                  </>
                )}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
