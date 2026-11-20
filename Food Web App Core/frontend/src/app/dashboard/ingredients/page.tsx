'use client';

import React, { useState, useMemo, useEffect } from 'react';
import { 
  Search, Filter, Database, Check, Plus, X, ArrowRight, Grid, List, Heart, Sliders, Info, ShieldCheck, CheckCircle
} from 'lucide-react';
import KnowledgeGraph from '@/components/knowledge-graph/knowledge-graph';

interface Ingredient {
  id: string;
  name: string;
  desc: string;
  proteinNum: number;
  proteinStr: string;
  fatNum: number;
  fatStr: string;
  carbsNum: number;
  sugarNum: number;
  fibreNum: number;
  sodiumNum: number;
  caloriesNum: number;
  costNum: number | null;
  costStr: string;
  category: string;
  functionalRole: string;
  source: string;
  roles: string[];
  allergens: string;
  vegan: boolean;
  glutenFree: boolean;
  dairyFree: boolean;
  nonGmo: boolean;
  organic: boolean;
  insNumber: string | null;
  casNumber: string | null;
  waterBinding: number;
  emulsification: number;
  gelation: number;
  thickening: number;
  textureImpact: string;
  flavorProfile: string;
  evidenceClaim: string;
  evidenceSource: string;
}

export default function IngredientLibrary() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategories, setSelectedCategories] = useState<string[]>(['Proteins']);
  const [selectedProps, setSelectedProps] = useState<string[]>([]);
  const [dietaryFilters, setDietaryFilters] = useState<{ vegan: boolean; nonGmo: boolean; organic: boolean }>({
    vegan: false,
    nonGmo: false,
    organic: false
  });
  const [maxCost, setMaxCost] = useState<number>(500);
  const [compareItems, setCompareItems] = useState<string[]>([]);
  const [selectedIngredient, setSelectedIngredient] = useState<Ingredient | null>(null);
  const [activeModalTab, setActiveModalTab] = useState<'OVERVIEW' | 'NUTRITION' | 'PROPERTIES' | 'COMPLIANCE' | 'KG RELATIONS'>('OVERVIEW');
  const [ingredientsList, setIngredientsList] = useState<Ingredient[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchIngredients() {
      try {
        setLoading(true);
        const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const res = await fetch(`${api_url}/api/ingredients`);
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data) && data.length > 0) {
            const mapped: Ingredient[] = data.map((item: any, idx: number) => {
              const pNum = item.protein !== undefined && item.protein !== null 
                ? Number(item.protein) 
                : (item.protein_percent !== undefined && item.protein_percent !== null ? Number(item.protein_percent) : 0);
              
              const fNum = item.fat !== undefined && item.fat !== null 
                ? Number(item.fat) 
                : (item.fat_percent !== undefined && item.fat_percent !== null ? Number(item.fat_percent) : 0);
              
              const cNum = item.carbs !== undefined && item.carbs !== null ? Number(item.carbs) : 0;
              const calNum = item.energy !== undefined && item.energy !== null 
                ? Number(item.energy) 
                : (item.calories !== undefined ? Number(item.calories) : 0);
              
              const costVal = item.cost_per_kg !== undefined && item.cost_per_kg !== null && !isNaN(Number(item.cost_per_kg))
                ? Number(item.cost_per_kg)
                : null;

              const isVegan = Boolean(item.vegan === 1 || item.vegan === true);
              const isGF = Boolean(item.gluten_free === 1 || item.gluten_free === true);
              const isDF = Boolean(item.dairy_free === 1 || item.dairy_free === true);
              const isOrg = Boolean(item.name?.toLowerCase().includes('organic') || item.category?.toLowerCase().includes('organic'));
              const isNonGmo = Boolean(!item.name?.toLowerCase().includes('gmo') && !item.desc?.toLowerCase().includes('bioengineered'));

              const catName = item.category || 'General';
              const fRole = item.functional_role || catName;
              const rolesList = item.functional_roles || [fRole];

              return {
                id: item.id || `ing_${idx + 1}`,
                name: item.name || 'Food Ingredient',
                desc: item.evidence_claim || item.flavor_notes || 'Grounded food ingredient entry from scientific knowledge base.',
                proteinNum: pNum,
                proteinStr: pNum > 0 ? `${pNum.toFixed(1)}%` : '0.0%',
                fatNum: fNum,
                fatStr: fNum > 0 ? `${fNum.toFixed(1)}%` : '0.0%',
                carbsNum: cNum,
                sugarNum: Number(item.sugar || 0),
                fibreNum: Number(item.fibre || 0),
                sodiumNum: Number(item.sodium || 0),
                caloriesNum: calNum,
                costNum: costVal,
                costStr: costVal !== null ? `$${costVal.toFixed(2)}/kg` : 'N/A',
                category: catName,
                functionalRole: fRole,
                source: item.evidence_source || item.data_source || 'USDA FDC / Food Science KG',
                roles: Array.isArray(rolesList) ? rolesList : [String(rolesList)],
                allergens: item.allergens || 'None',
                vegan: isVegan,
                glutenFree: isGF,
                dairyFree: isDF,
                nonGmo: isNonGmo,
                organic: isOrg,
                insNumber: item.ins_number || null,
                casNumber: item.cas_number || null,
                waterBinding: Number(item.water_binding || 0.5),
                emulsification: Number(item.emulsification || 0.5),
                gelation: Number(item.gelation || 0.4),
                thickening: Number(item.thickening || 0.5),
                textureImpact: item.texture_impact || 'Standard Matrix Impact',
                flavorProfile: item.flavor_profile || 'Clean Neutral Profile',
                evidenceClaim: item.evidence_claim || 'Scientifically validated food formulation ingredient.',
                evidenceSource: item.evidence_source || 'Scientific Literature / Codex Standards'
              };
            });
            setIngredientsList(mapped);
          }
        }
      } catch (err) {
        console.error("Failed to load ingredients:", err);
      } finally {
        setLoading(false);
      }
    }
    fetchIngredients();
  }, []);

  // Category counts computed dynamically from true dataset
  const categoryCounts = useMemo(() => {
    return {
      Proteins: ingredientsList.filter(i => 
        i.category.toLowerCase().includes('protein') || 
        i.functionalRole.toLowerCase().includes('protein') || 
        i.roles.some(r => r.toLowerCase().includes('protein')) ||
        i.name.toLowerCase().includes('protein') ||
        i.proteinNum >= 10.0
      ).length,
      Sweeteners: ingredientsList.filter(i => 
        i.category.toLowerCase().includes('sweetener') || 
        i.functionalRole.toLowerCase().includes('sweetener') ||
        i.name.toLowerCase().includes('sugar') || 
        i.name.toLowerCase().includes('allulose') || 
        i.name.toLowerCase().includes('syrup') ||
        i.name.toLowerCase().includes('stevia') ||
        i.name.toLowerCase().includes('monk') ||
        i.name.toLowerCase().includes('erythritol')
      ).length,
      FatsAndOils: ingredientsList.filter(i => 
        i.category.toLowerCase().includes('fat') || 
        i.category.toLowerCase().includes('oil') || 
        i.functionalRole.toLowerCase().includes('fat') ||
        i.functionalRole.toLowerCase().includes('lipid') ||
        i.name.toLowerCase().includes('butter') || 
        i.name.toLowerCase().includes('oil') ||
        i.fatNum >= 10.0
      ).length,
      Emulsifiers: ingredientsList.filter(i => 
        i.category.toLowerCase().includes('emulsifier') || 
        i.functionalRole.toLowerCase().includes('emulsifier') ||
        i.roles.some(r => r.toLowerCase().includes('emulsifier')) ||
        i.name.toLowerCase().includes('lecithin') ||
        i.name.toLowerCase().includes('phosphatide') ||
        i.name.toLowerCase().includes('gum') ||
        i.name.toLowerCase().includes('pectin') ||
        i.emulsification >= 0.7
      ).length,
    };
  }, [ingredientsList]);

  // Toggle category checkbox
  const toggleCategory = (cat: string) => {
    setSelectedCategories(prev => {
      if (prev.includes(cat)) {
        return prev.filter(c => c !== cat);
      } else {
        return [...prev, cat];
      }
    });
  };

  // Toggle functional property pill
  const toggleProp = (prop: string) => {
    setSelectedProps(prev => {
      if (prev.includes(prop)) {
        return prev.filter(p => p !== prop);
      } else {
        return [...prev, prop];
      }
    });
  };

  // Multi-facet filtering logic
  const filteredIngredients = useMemo(() => {
    return ingredientsList.filter((item) => {
      // 1. Search term match
      if (searchTerm.trim()) {
        const q = searchTerm.toLowerCase();
        const matchesName = item.name.toLowerCase().includes(q);
        const matchesDesc = item.desc.toLowerCase().includes(q);
        const matchesCat = item.category.toLowerCase().includes(q);
        const matchesRole = item.functionalRole.toLowerCase().includes(q) || item.roles.some(r => r.toLowerCase().includes(q));
        const matchesCas = item.casNumber ? item.casNumber.toLowerCase().includes(q) : false;
        const matchesIns = item.insNumber ? item.insNumber.toLowerCase().includes(q) : false;
        if (!matchesName && !matchesDesc && !matchesCat && !matchesRole && !matchesCas && !matchesIns) {
          return false;
        }
      }

      // 2. Categories filter (if any categories selected)
      if (selectedCategories.length > 0) {
        const matchesAnyCat = selectedCategories.some(cat => {
          if (cat === 'Proteins') {
            return item.category.toLowerCase().includes('protein') || 
                   item.functionalRole.toLowerCase().includes('protein') || 
                   item.name.toLowerCase().includes('protein') ||
                   item.proteinNum >= 10.0;
          }
          if (cat === 'Sweeteners') {
            return item.category.toLowerCase().includes('sweetener') || 
                   item.functionalRole.toLowerCase().includes('sweetener') ||
                   item.name.toLowerCase().includes('sugar') || 
                   item.name.toLowerCase().includes('allulose') || 
                   item.name.toLowerCase().includes('syrup') ||
                   item.name.toLowerCase().includes('stevia') ||
                   item.name.toLowerCase().includes('monk') ||
                   item.name.toLowerCase().includes('erythritol');
          }
          if (cat === 'Fats & Oils') {
            return item.category.toLowerCase().includes('fat') || 
                   item.category.toLowerCase().includes('oil') || 
                   item.functionalRole.toLowerCase().includes('fat') ||
                   item.functionalRole.toLowerCase().includes('lipid') ||
                   item.name.toLowerCase().includes('butter') || 
                   item.name.toLowerCase().includes('oil') ||
                   item.fatNum >= 10.0;
          }
          if (cat === 'Emulsifiers') {
            return item.category.toLowerCase().includes('emulsifier') || 
                   item.functionalRole.toLowerCase().includes('emulsifier') ||
                   item.roles.some(r => r.toLowerCase().includes('emulsifier')) ||
                   item.name.toLowerCase().includes('lecithin') ||
                   item.name.toLowerCase().includes('phosphatide') ||
                   item.name.toLowerCase().includes('gum') ||
                   item.name.toLowerCase().includes('pectin') ||
                   item.emulsification >= 0.7;
          }
          return false;
        });
        if (!matchesAnyCat) return false;
      }

      // 3. Functional Properties filter
      if (selectedProps.length > 0) {
        const matchesProps = selectedProps.every(prop => {
          if (prop === 'Binding') {
            return item.waterBinding >= 0.5 || item.roles.some(r => r.toLowerCase().includes('bind') || r.toLowerCase().includes('stabil'));
          }
          if (prop === 'Emulsification') {
            return item.emulsification >= 0.5 || item.category.toLowerCase().includes('emuls') || item.functionalRole.toLowerCase().includes('emuls');
          }
          if (prop === 'Thickening') {
            return item.thickening >= 0.5 || item.roles.some(r => r.toLowerCase().includes('thicken')) || item.name.toLowerCase().includes('gum') || item.name.toLowerCase().includes('starch');
          }
          if (prop === 'Colorant') {
            return item.category.toLowerCase().includes('color') || item.roles.some(r => r.toLowerCase().includes('color')) || item.name.toLowerCase().includes('carotene') || item.name.toLowerCase().includes('color');
          }
          return true;
        });
        if (!matchesProps) return false;
      }

      // 4. Dietary Compliance filter
      if (dietaryFilters.vegan && !item.vegan) return false;
      if (dietaryFilters.nonGmo && !item.nonGmo) return false;
      if (dietaryFilters.organic && !item.organic) return false;

      // 5. Cost Range filter
      if (maxCost < 500 && item.costNum !== null && item.costNum > maxCost) {
        return false;
      }

      return true;
    });
  }, [ingredientsList, searchTerm, selectedCategories, selectedProps, dietaryFilters, maxCost]);

  const toggleCompare = (name: string) => {
    if (compareItems.includes(name)) {
      setCompareItems(compareItems.filter(i => i !== name));
    } else if (compareItems.length < 4) {
      setCompareItems([...compareItems, name]);
    }
  };

  return (
    <div className="max-w-6xl mx-auto py-4 space-y-6 font-sans">
      
      {/* Title Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-[#191C1E] font-heading">Ingredient Library</h1>
        <p className="text-[#5F6D67] text-xs font-mono font-bold mt-0.5">
          Explore 2.4M+ structured chemical compositions, functional properties, and regulatory datasets.
        </p>
      </div>

      {/* Main Layout Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Left Sidebar Filters */}
        <div className="lg:col-span-4 canonical-card p-5 space-y-6 bg-white border border-[#E5E9E6] rounded-2xl shadow-sm">
          
          {/* CATEGORIES */}
          <div className="space-y-3">
            <span className="text-[10px] font-mono font-bold text-[#5F6D67] uppercase tracking-wider block">
              CATEGORIES
            </span>
            <div className="space-y-2 text-xs font-bold text-[#191C1E]">
              <label className="flex justify-between items-center cursor-pointer select-none">
                <div className="flex items-center gap-2">
                  <input 
                    type="checkbox" 
                    checked={selectedCategories.includes('Proteins')} 
                    onChange={() => toggleCategory('Proteins')}
                    className="accent-[#164E3D] rounded h-3.5 w-3.5 cursor-pointer" 
                  />
                  <span>Proteins</span>
                </div>
                <span className="text-[11px] text-[#5F6D67] font-mono">{categoryCounts.Proteins}</span>
              </label>

              <label className="flex justify-between items-center cursor-pointer select-none">
                <div className="flex items-center gap-2">
                  <input 
                    type="checkbox" 
                    checked={selectedCategories.includes('Sweeteners')} 
                    onChange={() => toggleCategory('Sweeteners')}
                    className="accent-[#164E3D] rounded h-3.5 w-3.5 cursor-pointer" 
                  />
                  <span>Sweeteners</span>
                </div>
                <span className="text-[11px] text-[#5F6D67] font-mono">{categoryCounts.Sweeteners}</span>
              </label>

              <label className="flex justify-between items-center cursor-pointer select-none">
                <div className="flex items-center gap-2">
                  <input 
                    type="checkbox" 
                    checked={selectedCategories.includes('Fats & Oils')} 
                    onChange={() => toggleCategory('Fats & Oils')}
                    className="accent-[#164E3D] rounded h-3.5 w-3.5 cursor-pointer" 
                  />
                  <span>Fats & Oils</span>
                </div>
                <span className="text-[11px] text-[#5F6D67] font-mono">{categoryCounts.FatsAndOils}</span>
              </label>

              <label className="flex justify-between items-center cursor-pointer select-none">
                <div className="flex items-center gap-2">
                  <input 
                    type="checkbox" 
                    checked={selectedCategories.includes('Emulsifiers')} 
                    onChange={() => toggleCategory('Emulsifiers')}
                    className="accent-[#164E3D] rounded h-3.5 w-3.5 cursor-pointer" 
                  />
                  <span>Emulsifiers</span>
                </div>
                <span className="text-[11px] text-[#5F6D67] font-mono">{categoryCounts.Emulsifiers}</span>
              </label>
            </div>
          </div>

          {/* FUNCTIONAL PROPERTIES */}
          <div className="space-y-3 border-t border-[#E5E9E6] pt-4">
            <span className="text-[10px] font-mono font-bold text-[#5F6D67] uppercase tracking-wider block">
              FUNCTIONAL PROPERTIES
            </span>
            <div className="flex flex-wrap gap-2 text-xs font-bold">
              {['Binding', 'Emulsification', 'Thickening', 'Colorant'].map((prop) => {
                const isActive = selectedProps.includes(prop);
                return (
                  <button
                    key={prop}
                    type="button"
                    onClick={() => toggleProp(prop)}
                    className={`px-2.5 py-1 rounded-full text-xs font-bold transition cursor-pointer select-none ${
                      isActive 
                        ? 'bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9] shadow-xs' 
                        : 'text-[#5F6D67] border border-[#E5E9E6] bg-white hover:border-[#164E3D]'
                    }`}
                  >
                    {prop}
                  </button>
                );
              })}
            </div>
          </div>

          {/* DIETARY COMPLIANCE */}
          <div className="space-y-3 border-t border-[#E5E9E6] pt-4">
            <span className="text-[10px] font-mono font-bold text-[#5F6D67] uppercase tracking-wider block">
              DIETARY COMPLIANCE
            </span>
            <div className="space-y-2 text-xs font-bold text-[#191C1E]">
              <label className="flex items-center gap-2 cursor-pointer select-none">
                <input 
                  type="checkbox" 
                  checked={dietaryFilters.vegan} 
                  onChange={(e) => setDietaryFilters(prev => ({ ...prev, vegan: e.target.checked }))}
                  className="accent-[#164E3D] rounded h-3.5 w-3.5 cursor-pointer" 
                />
                <span>Vegan</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer select-none">
                <input 
                  type="checkbox" 
                  checked={dietaryFilters.nonGmo} 
                  onChange={(e) => setDietaryFilters(prev => ({ ...prev, nonGmo: e.target.checked }))}
                  className="accent-[#164E3D] rounded h-3.5 w-3.5 cursor-pointer" 
                />
                <span>Non-GMO</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer select-none">
                <input 
                  type="checkbox" 
                  checked={dietaryFilters.organic} 
                  onChange={(e) => setDietaryFilters(prev => ({ ...prev, organic: e.target.checked }))}
                  className="accent-[#164E3D] rounded h-3.5 w-3.5 cursor-pointer" 
                />
                <span>Organic</span>
              </label>
            </div>
          </div>

          {/* COST RANGE */}
          <div className="space-y-3 border-t border-[#E5E9E6] pt-4">
            <div className="flex justify-between items-center text-[10px] font-mono font-bold text-[#5F6D67]">
              <span>COST RANGE</span>
              <span className="text-[#164E3D]">$0 - ${maxCost}/KG</span>
            </div>
            <input 
              type="range" 
              min={0} 
              max={500} 
              value={maxCost} 
              onChange={(e) => setMaxCost(Number(e.target.value))}
              className="w-full accent-[#164E3D] cursor-pointer" 
            />
          </div>

          {/* Reset Filters Button */}
          {(selectedCategories.length !== 1 || selectedCategories[0] !== 'Proteins' || selectedProps.length > 0 || dietaryFilters.vegan || dietaryFilters.nonGmo || dietaryFilters.organic || maxCost < 500) && (
            <div className="pt-2 border-t border-[#E5E9E6]">
              <button
                type="button"
                onClick={() => {
                  setSelectedCategories([]);
                  setSelectedProps([]);
                  setDietaryFilters({ vegan: false, nonGmo: false, organic: false });
                  setMaxCost(500);
                  setSearchTerm('');
                }}
                className="w-full py-1.5 text-center text-xs font-mono font-bold text-[#164E3D] hover:underline"
              >
                Clear all filters
              </button>
            </div>
          )}

        </div>

        {/* Right Content Area */}
        <div className="lg:col-span-8 space-y-4">
          
          {/* Search Bar */}
          <div className="flex flex-col sm:flex-row justify-between items-center gap-3">
            <div className="relative flex-1 w-full">
              <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-[#5F6D67]" />
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search by name, CAS number, or functional property..."
                className="w-full bg-white border border-[#E5E9E6] rounded-xl pl-10 pr-4 py-2.5 text-xs font-bold text-[#191C1E] focus:outline-none focus:border-[#164E3D] shadow-xs"
              />
              {searchTerm && (
                <button 
                  type="button" 
                  onClick={() => setSearchTerm('')} 
                  className="absolute right-3.5 top-1/2 -translate-y-1/2 text-[#5F6D67] hover:text-[#191C1E]"
                >
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>
          </div>

          {/* Results Metadata Bar */}
          <div className="flex flex-wrap items-center gap-2 text-xs font-mono text-[#5F6D67] font-bold">
            <span>Showing <strong className="text-[#191C1E]">{filteredIngredients.length} results</strong>{searchTerm ? ` for "${searchTerm}"` : ''}</span>
            {selectedCategories.map(cat => (
              <span key={cat} className="px-2 py-0.5 rounded-full bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9] font-bold text-[10px] flex items-center gap-1">
                {cat}
                <X className="h-3 w-3 cursor-pointer" onClick={() => toggleCategory(cat)} />
              </span>
            ))}
            {selectedProps.map(prop => (
              <span key={prop} className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold text-[10px] flex items-center gap-1">
                {prop}
                <X className="h-3 w-3 cursor-pointer" onClick={() => toggleProp(prop)} />
              </span>
            ))}
            {dietaryFilters.vegan && (
              <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-900 font-bold text-[10px] flex items-center gap-1">
                Vegan
                <X className="h-3 w-3 cursor-pointer" onClick={() => setDietaryFilters(prev => ({ ...prev, vegan: false }))} />
              </span>
            )}
          </div>

          {/* Ingredient Cards Grid */}
          {loading ? (
            <div className="py-16 text-center text-[#5F6D67] font-sans text-sm font-bold bg-white rounded-2xl border border-[#E5E9E6]">
              Loading ingredient catalog...
            </div>
          ) : filteredIngredients.length === 0 ? (
            <div className="py-16 text-center text-[#5F6D67] font-sans text-sm font-bold bg-white rounded-2xl border border-[#E5E9E6] space-y-2">
              <p>No ingredients found matching your search and filter criteria.</p>
              <button
                type="button"
                onClick={() => {
                  setSelectedCategories([]);
                  setSelectedProps([]);
                  setDietaryFilters({ vegan: false, nonGmo: false, organic: false });
                  setMaxCost(500);
                  setSearchTerm('');
                }}
                className="text-xs font-mono font-bold text-[#164E3D] hover:underline"
              >
                Reset filters to view all ingredients
              </button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {filteredIngredients.map((item) => {
                const isCompared = compareItems.includes(item.name);

                return (
                  <div key={item.id} className="canonical-card p-5 space-y-4 hover-lift flex flex-col justify-between bg-white border border-[#E5E9E6] rounded-2xl shadow-sm">
                    <div>
                      <div className="flex justify-between items-start mb-2">
                        <div className="h-8 w-8 rounded-lg bg-[#ECF4F0] text-[#164E3D] flex items-center justify-center">
                          <Database className="h-4 w-4" />
                        </div>
                        <button 
                          type="button"
                          onClick={() => toggleCompare(item.name)}
                          className={`text-slate-400 hover:text-[#164E3D] transition ${isCompared ? 'text-[#164E3D]' : ''}`}
                        >
                          <Heart className={`h-4 w-4 ${isCompared ? 'fill-[#164E3D]' : ''}`} />
                        </button>
                      </div>

                      <h4 className="font-extrabold text-sm text-[#191C1E] font-heading line-clamp-1">{item.name}</h4>
                      <p className="text-xs text-[#5F6D67] mt-1.5 line-clamp-2 leading-relaxed font-bold">
                        {item.desc}
                      </p>

                      <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6] mt-3 grid grid-cols-2 gap-2 text-[11px] font-mono font-bold">
                        <div>
                          <span className="text-[9px] text-[#5F6D67] block uppercase">PROTEIN</span>
                          <span className="font-bold text-[#191C1E]">{item.proteinStr}</span>
                        </div>
                        <div>
                          <span className="text-[9px] text-[#5F6D67] block uppercase">FAT</span>
                          <span className="font-bold text-[#191C1E]">{item.fatStr}</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex justify-between items-center border-t border-[#E5E9E6] pt-3 mt-2">
                      <span className="font-mono font-extrabold text-xs text-[#191C1E]">{item.costStr}</span>
                      <button
                        type="button"
                        onClick={() => { setSelectedIngredient(item); setActiveModalTab('OVERVIEW'); }}
                        className="px-3 py-1.5 rounded-lg bg-[#164E3D] hover:bg-[#123F32] text-white font-extrabold text-xs transition shadow-xs cursor-pointer"
                      >
                        View Specs
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}

        </div>

      </div>

      {/* Ingredient Specs Modal Overlay */}
      {selectedIngredient && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white border border-[#E5E9E6] rounded-2xl max-w-lg w-full p-6 space-y-5 shadow-2xl relative max-h-[90vh] overflow-y-auto">
            
            {/* Header with Category Badge and Title */}
            <div className="flex justify-between items-start border-b border-[#E5E9E6] pb-3">
              <div>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9] uppercase tracking-wider inline-block mb-1 font-mono">
                  {selectedIngredient.category}
                </span>
                <h3 className="text-xl font-extrabold text-[#191C1E] font-heading">{selectedIngredient.name}</h3>
              </div>
              <button
                type="button"
                onClick={() => setSelectedIngredient(null)}
                className="p-1 rounded-lg hover:bg-[#FAFAF8] text-[#5F6D67] hover:text-[#191C1E] transition cursor-pointer"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Navigation Tabs (OVERVIEW, NUTRITION, PROPERTIES, COMPLIANCE, KG RELATIONS) */}
            <div className="flex border-b border-[#E5E9E6] gap-4 text-xs font-mono font-bold overflow-x-auto pb-1">
              {(['OVERVIEW', 'NUTRITION', 'PROPERTIES', 'COMPLIANCE', 'KG RELATIONS'] as const).map((tab) => (
                <button
                  key={tab}
                  type="button"
                  onClick={() => setActiveModalTab(tab)}
                  className={`pb-2.5 transition whitespace-nowrap cursor-pointer ${
                    activeModalTab === tab 
                      ? 'text-[#164E3D] border-b-2 border-[#164E3D]' 
                      : 'text-[#5F6D67] hover:text-[#191C1E]'
                  }`}
                >
                  {tab}
                </button>
              ))}
            </div>

            {/* Tab 1: OVERVIEW */}
            {activeModalTab === 'OVERVIEW' && (
              <div className="space-y-4">
                <p className="text-xs text-[#5F6D67] leading-relaxed font-bold">
                  {selectedIngredient.desc}
                </p>

                <div className="space-y-1.5">
                  <span className="text-[10px] font-mono font-bold text-[#5F6D67] uppercase tracking-wider block">
                    Functional Roles & Taxonomy
                  </span>
                  <div className="flex flex-wrap gap-2 text-xs font-mono font-bold">
                    {selectedIngredient.roles.map(r => (
                      <span key={r} className="px-2.5 py-1 rounded-full bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9]">
                        {r}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3 pt-2">
                  <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
                    <span className="text-[9px] font-mono font-bold text-[#5F6D67] uppercase block">COST / KG</span>
                    <span className="text-lg font-mono font-extrabold text-[#191C1E]">{selectedIngredient.costStr}</span>
                  </div>
                  <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
                    <span className="text-[9px] font-mono font-bold text-[#5F6D67] uppercase block">DATA SOURCE</span>
                    <span className="text-sm font-mono font-extrabold text-[#164E3D] line-clamp-2">{selectedIngredient.source}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Tab 2: NUTRITION */}
            {activeModalTab === 'NUTRITION' && (
              <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
                  <span className="text-[9px] text-[#5F6D67] block uppercase">Protein Content</span>
                  <span className="text-base font-extrabold text-[#164E3D]">{selectedIngredient.proteinStr}</span>
                </div>
                <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
                  <span className="text-[9px] text-[#5F6D67] block uppercase">Fat Content</span>
                  <span className="text-base font-extrabold text-[#191C1E]">{selectedIngredient.fatStr}</span>
                </div>
                <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
                  <span className="text-[9px] text-[#5F6D67] block uppercase">Carbohydrates</span>
                  <span className="text-base font-extrabold text-[#191C1E]">{selectedIngredient.carbsNum.toFixed(1)}%</span>
                </div>
                <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
                  <span className="text-[9px] text-[#5F6D67] block uppercase">Energy Density</span>
                  <span className="text-base font-extrabold text-[#191C1E]">{selectedIngredient.caloriesNum.toFixed(0)} kcal / 100g</span>
                </div>
              </div>
            )}

            {/* Tab 3: PROPERTIES */}
            {activeModalTab === 'PROPERTIES' && (
              <div className="space-y-2 text-xs font-mono">
                <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                  <span className="text-[#5F6D67]">Texture Impact:</span>
                  <span className="font-bold text-[#164E3D]">{selectedIngredient.textureImpact}</span>
                </div>
                <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                  <span className="text-[#5F6D67]">Flavor Profile:</span>
                  <span className="font-bold text-[#164E3D]">{selectedIngredient.flavorProfile}</span>
                </div>
                <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                  <span className="text-[#5F6D67]">Emulsification Index:</span>
                  <span className="font-bold text-[#164E3D]">{(selectedIngredient.emulsification * 100).toFixed(0)}% Stability</span>
                </div>
                <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                  <span className="text-[#5F6D67]">Water Binding Capacity:</span>
                  <span className="font-bold text-[#191C1E]">{(selectedIngredient.waterBinding * 5).toFixed(1)}g / g</span>
                </div>
              </div>
            )}

            {/* Tab 4: COMPLIANCE */}
            {activeModalTab === 'COMPLIANCE' && (
              <div className="space-y-2 text-xs font-mono">
                <div className="flex justify-between p-2.5 bg-emerald-50 rounded-lg border border-emerald-200 text-emerald-800 font-bold">
                  <span>Vegan Status:</span>
                  <span>{selectedIngredient.vegan ? '100% Plant-Based' : 'Non-Vegan / Animal Derived'}</span>
                </div>
                <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                  <span className="text-[#5F6D67]">Gluten-Free:</span>
                  <span className="font-bold text-[#191C1E]">{selectedIngredient.glutenFree ? 'Gluten-Free' : 'Contains Gluten'}</span>
                </div>
                <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                  <span className="text-[#5F6D67]">Allergens:</span>
                  <span className={`font-bold ${selectedIngredient.allergens === 'None' ? 'text-emerald-700' : 'text-amber-700'}`}>
                    {selectedIngredient.allergens}
                  </span>
                </div>
                {selectedIngredient.insNumber && (
                  <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                    <span className="text-[#5F6D67]">INS Additive Code:</span>
                    <span className="font-bold text-[#164E3D]">{selectedIngredient.insNumber}</span>
                  </div>
                )}
                {selectedIngredient.casNumber && (
                  <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                    <span className="text-[#5F6D67]">CAS Registry Number:</span>
                    <span className="font-bold text-[#191C1E]">{selectedIngredient.casNumber}</span>
                  </div>
                )}
              </div>
            )}

            {/* Tab 5: KG RELATIONS (Live Interactive Knowledge Graph) */}
            {activeModalTab === 'KG RELATIONS' && (
              <div className="space-y-4 font-mono">
                <div className="p-3 bg-[#ECF4F0] rounded-xl border border-[#D1E2D9] space-y-1 text-xs">
                  <span className="text-[10px] font-bold text-[#164E3D] uppercase block">LIVE GROUNDED KNOWLEDGE GRAPH SUBGRAPH</span>
                  <div className="text-xs font-bold text-[#191C1E]">
                    (:Ingredient &#123;id: &ldquo;{selectedIngredient.id}&rdquo;, name: &ldquo;{selectedIngredient.name}&rdquo;&#125;)
                  </div>
                  <span className="text-[9px] text-[#5F6D67]">Data Source: {selectedIngredient.source}</span>
                </div>

                {/* Embedded Cytoscape Knowledge Graph Component */}
                <div className="h-[380px] w-full rounded-2xl overflow-hidden border border-[#E5E9E6]">
                  <KnowledgeGraph initialIngredientId={selectedIngredient.name} title="Ingredient Subgraph" subtitle={`Exploring connected nodes for ${selectedIngredient.name}`} />
                </div>

                <div className="flex justify-end pt-1 font-sans">
                  <a
                    href={`/dashboard/knowledge-graph`}
                    className="px-4 py-2 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white font-extrabold text-xs transition shadow-sm flex items-center gap-1.5"
                  >
                    Open Full Knowledge Graph Explorer <ArrowRight className="h-3.5 w-3.5" />
                  </a>
                </div>
              </div>
            )}

            <div className="pt-2">
              <button
                type="button"
                onClick={() => setSelectedIngredient(null)}
                className="w-full py-2.5 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-xs font-extrabold text-white transition shadow-sm cursor-pointer"
              >
                Close Specs
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
}
