'use client';

import React, { useState } from 'react';
import { 
  Search, Filter, Database, Check, Plus, X, ArrowRight, Grid, List, Heart, Sliders, Info
} from 'lucide-react';
import KnowledgeGraph from '@/components/knowledge-graph/knowledge-graph';

interface Ingredient {
  id: string;
  name: string;
  desc: string;
  protein: string;
  fat: string;
  price: string;
  category: string;
  source: string;
  roles: string[];
}

export default function IngredientLibrary() {
  const [searchTerm, setSearchTerm] = useState('Protein');
  const [selectedCategory, setSelectedCategory] = useState('Proteins');
  const [compareItems, setCompareItems] = useState<string[]>(['Pea Protein Isolate', 'Potato Protein']);
  const [selectedIngredient, setSelectedIngredient] = useState<Ingredient | null>(null);
  const [activeModalTab, setActiveModalTab] = useState<'OVERVIEW' | 'NUTRITION' | 'PROPERTIES' | 'COMPLIANCE' | 'KG RELATIONS'>('OVERVIEW');

  const [ingredientsList, setIngredientsList] = useState<Ingredient[]>([
    {
      id: 'ING_001',
      name: 'Pea Protein Isolate',
      desc: 'High-purity plant protein derived from yellow peas. Excellent emulsification and binding properties for bakery, confectionery, and dairy alternative applications.',
      protein: '85% min',
      fat: '4.2%',
      price: '$12.40',
      category: 'Proteins',
      source: 'FooDB',
      roles: ['Binding', 'Emulsification']
    },
    {
      id: 'ING_002',
      name: 'Brown Rice Protein',
      desc: 'Hypoallergenic protein source with a complete amino acid profile. Ideal for clean-label sport nutrition and bakery matrices.',
      protein: '80% min',
      fat: '3.5%',
      price: '$10.85',
      category: 'Proteins',
      source: 'FooDB',
      roles: ['Fortification', 'Nutritional Density']
    },
    {
      id: 'ING_003',
      name: 'Potato Protein',
      desc: 'High-performance functional protein with superior gelling and foaming properties suitable for plant-based meat analogues and egg replacements.',
      protein: '90% min',
      fat: '3.5%',
      price: '$18.20',
      category: 'Proteins',
      source: 'FooDB',
      roles: ['Gelling', 'Foaming']
    }
  ]);

  React.useEffect(() => {
    async function fetchIngredients() {
      try {
        const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        const res = await fetch(`${api_url}/api/ingredients`);
        if (res.ok) {
          const data = await res.json();
          if (Array.isArray(data) && data.length > 0) {
            const mapped: Ingredient[] = data.map((item: any, idx: number) => ({
              id: item.id || `ING_00${idx + 1}`,
              name: item.name || 'Food Ingredient',
              desc: item.description || item.flavor_notes || 'Grounded food ingredient entry from scientific knowledge base.',
              protein: item.protein_percent ? `${item.protein_percent}%` : '80% min',
              fat: item.fat_percent ? `${item.fat_percent}%` : '3.5%',
              price: item.cost_per_kg ? `$${item.cost_per_kg}` : '$12.00',
              category: item.category || 'Proteins',
              source: item.data_source || 'Grounded DB',
              roles: item.functional_roles || [item.category || 'Protein']
            }));
            setIngredientsList(mapped);
          }
        }
      } catch (err) {
        console.log("Using cached ingredients data.");
      }
    }
    fetchIngredients();
  }, []);

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
        <div className="lg:col-span-4 canonical-card p-5 space-y-6 bg-white">
          
          {/* CATEGORIES */}
          <div className="space-y-3">
            <span className="text-[10px] font-mono font-bold text-[#5F6D67] uppercase tracking-wider block">
              CATEGORIES
            </span>
            <div className="space-y-2 text-xs font-bold text-[#191C1E]">
              <label className="flex justify-between items-center cursor-pointer">
                <div className="flex items-center gap-2">
                  <input type="checkbox" defaultChecked className="accent-[#164E3D] rounded" />
                  <span>Proteins</span>
                </div>
                <span className="text-[11px] text-[#5F6D67] font-mono">242</span>
              </label>

              <label className="flex justify-between items-center cursor-pointer">
                <div className="flex items-center gap-2">
                  <input type="checkbox" className="accent-[#164E3D] rounded" />
                  <span>Sweeteners</span>
                </div>
                <span className="text-[11px] text-[#5F6D67] font-mono">158</span>
              </label>

              <label className="flex justify-between items-center cursor-pointer">
                <div className="flex items-center gap-2">
                  <input type="checkbox" className="accent-[#164E3D] rounded" />
                  <span>Fats & Oils</span>
                </div>
                <span className="text-[11px] text-[#5F6D67] font-mono">94</span>
              </label>

              <label className="flex justify-between items-center cursor-pointer">
                <div className="flex items-center gap-2">
                  <input type="checkbox" className="accent-[#164E3D] rounded" />
                  <span>Emulsifiers</span>
                </div>
                <span className="text-[11px] text-[#5F6D67] font-mono">67</span>
              </label>
            </div>
          </div>

          {/* FUNCTIONAL PROPERTIES */}
          <div className="space-y-3 border-t border-[#E5E9E6] pt-4">
            <span className="text-[10px] font-mono font-bold text-[#5F6D67] uppercase tracking-wider block">
              FUNCTIONAL PROPERTIES
            </span>
            <div className="flex flex-wrap gap-2 text-xs font-bold">
              <span className="px-2.5 py-1 rounded-full bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9]">Binding</span>
              <span className="px-2.5 py-1 rounded-full bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9]">Emulsification</span>
              <span className="px-2.5 py-1 rounded-full bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9]">Thickening</span>
              <span className="px-2.5 py-1 rounded-full text-[#5F6D67] border border-[#E5E9E6] bg-white">Colorant</span>
            </div>
          </div>

          {/* DIETARY COMPLIANCE */}
          <div className="space-y-3 border-t border-[#E5E9E6] pt-4">
            <span className="text-[10px] font-mono font-bold text-[#5F6D67] uppercase tracking-wider block">
              DIETARY COMPLIANCE
            </span>
            <div className="space-y-2 text-xs font-bold text-[#191C1E]">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" defaultChecked className="accent-[#164E3D] rounded" />
                <span>Vegan</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" defaultChecked className="accent-[#164E3D] rounded" />
                <span>Non-GMO</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" defaultChecked className="accent-[#164E3D] rounded" />
                <span>Organic</span>
              </label>
            </div>
          </div>

          {/* COST RANGE */}
          <div className="space-y-3 border-t border-[#E5E9E6] pt-4">
            <div className="flex justify-between items-center text-[10px] font-mono font-bold text-[#5F6D67]">
              <span>COST RANGE</span>
              <span className="text-[#164E3D]">$0 - $500/KG</span>
            </div>
            <input type="range" min={0} max={500} defaultValue={120} className="w-full accent-[#164E3D]" />
          </div>

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
                className="w-full bg-white border border-[#E5E9E6] rounded-xl pl-10 pr-4 py-2.5 text-xs font-bold text-[#191C1E] focus:outline-none focus:border-[#164E3D]"
              />
            </div>
          </div>

          {/* Results Metadata Bar */}
          <div className="flex items-center gap-2 text-xs font-mono text-[#5F6D67] font-bold">
            <span>Showing <strong className="text-[#191C1E]">24 results</strong> for &ldquo;{searchTerm}&rdquo;</span>
            <span className="px-2 py-0.5 rounded-full bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9] font-bold text-[10px] flex items-center gap-1">
              Category: Proteins
              <X className="h-3 w-3 cursor-pointer" />
            </span>
          </div>

          {/* Ingredient Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {ingredientsList.map((item) => {
              const isCompared = compareItems.includes(item.name);

              return (
                <div key={item.id} className="canonical-card p-5 space-y-4 hover-lift flex flex-col justify-between bg-white">
                  <div>
                    <div className="flex justify-between items-start mb-2">
                      <div className="h-8 w-8 rounded-lg bg-[#ECF4F0] text-[#164E3D] flex items-center justify-center">
                        <Database className="h-4 w-4" />
                      </div>
                      <button 
                        type="button"
                        onClick={() => toggleCompare(item.name)}
                        className={`text-slate-400 hover:text-[#164E3D] ${isCompared ? 'text-[#164E3D]' : ''}`}
                      >
                        <Heart className={`h-4 w-4 ${isCompared ? 'fill-[#164E3D]' : ''}`} />
                      </button>
                    </div>

                    <h4 className="font-extrabold text-sm text-[#191C1E] font-heading">{item.name}</h4>
                    <p className="text-xs text-[#5F6D67] mt-1.5 line-clamp-2 leading-relaxed font-bold">
                      {item.desc}
                    </p>

                    <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6] mt-3 grid grid-cols-2 gap-2 text-[11px] font-mono font-bold">
                      <div>
                        <span className="text-[9px] text-[#5F6D67] block uppercase">PROTEIN</span>
                        <span className="font-bold text-[#191C1E]">{item.protein}</span>
                      </div>
                      <div>
                        <span className="text-[9px] text-[#5F6D67] block uppercase">FAT</span>
                        <span className="font-bold text-[#191C1E]">{item.fat}</span>
                      </div>
                    </div>
                  </div>

                  <div className="flex justify-between items-center border-t border-[#E5E9E6] pt-3 mt-2">
                    <span className="font-mono font-extrabold text-xs text-[#191C1E]">{item.price}/kg</span>
                    <button
                      type="button"
                      onClick={() => { setSelectedIngredient(item); setActiveModalTab('OVERVIEW'); }}
                      className="px-3 py-1.5 rounded-lg bg-[#164E3D] hover:bg-[#123F32] text-white font-extrabold text-xs transition"
                    >
                      View Specs
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

        </div>

      </div>

      {/* IMAGE 2 EXACT MATCH: Ingredient Specs Modal Overlay */}
      {selectedIngredient && (
        <div className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white border border-[#E5E9E6] rounded-2xl max-w-lg w-full p-6 space-y-5 shadow-2xl relative">
            
            {/* Header with Category Badge and Title */}
            <div className="flex justify-between items-start border-b border-[#E5E9E6] pb-3">
              <div>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9] uppercase tracking-wider inline-block mb-1">
                  {selectedIngredient.category}
                </span>
                <h3 className="text-xl font-extrabold text-[#191C1E] font-heading">{selectedIngredient.name}</h3>
              </div>
              <button
                type="button"
                onClick={() => setSelectedIngredient(null)}
                className="p-1 rounded-lg hover:bg-[#FAFAF8] text-[#5F6D67] hover:text-[#191C1E] transition"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            {/* Navigation Tabs (OVERVIEW, NUTRITION, PROPERTIES, COMPLIANCE, KG RELATIONS) */}
            <div className="flex border-b border-[#E5E9E6] gap-4 text-xs font-mono font-bold overflow-x-auto">
              {(['OVERVIEW', 'NUTRITION', 'PROPERTIES', 'COMPLIANCE', 'KG RELATIONS'] as const).map((tab) => (
                <button
                  key={tab}
                  type="button"
                  onClick={() => setActiveModalTab(tab)}
                  className={`pb-2.5 transition whitespace-nowrap ${
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
                    Functional Roles
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
                    <span className="text-lg font-mono font-extrabold text-[#191C1E]">{selectedIngredient.price}</span>
                  </div>
                  <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
                    <span className="text-[9px] font-mono font-bold text-[#5F6D67] uppercase block">DATA SOURCE</span>
                    <span className="text-lg font-mono font-extrabold text-[#164E3D]">{selectedIngredient.source}</span>
                  </div>
                </div>
              </div>
            )}

            {/* Tab 2: NUTRITION */}
            {activeModalTab === 'NUTRITION' && (
              <div className="grid grid-cols-2 gap-3 text-xs font-mono">
                <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
                  <span className="text-[9px] text-[#5F6D67] block uppercase">Protein Content</span>
                  <span className="text-base font-extrabold text-[#164E3D]">{selectedIngredient.protein}</span>
                </div>
                <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
                  <span className="text-[9px] text-[#5F6D67] block uppercase">Fat Content</span>
                  <span className="text-base font-extrabold text-[#191C1E]">{selectedIngredient.fat}</span>
                </div>
                <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
                  <span className="text-[9px] text-[#5F6D67] block uppercase">Energy Density</span>
                  <span className="text-base font-extrabold text-[#191C1E]">380 kcal / 100g</span>
                </div>
                <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
                  <span className="text-[9px] text-[#5F6D67] block uppercase">Moisture</span>
                  <span className="text-base font-extrabold text-[#191C1E]">5.0% max</span>
                </div>
              </div>
            )}

            {/* Tab 3: PROPERTIES */}
            {activeModalTab === 'PROPERTIES' && (
              <div className="space-y-2 text-xs font-mono">
                <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                  <span className="text-[#5F6D67]">Texture Impact:</span>
                  <span className="font-bold text-[#164E3D]">Smooth & Creamy</span>
                </div>
                <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                  <span className="text-[#5F6D67]">Emulsion Index:</span>
                  <span className="font-bold text-[#164E3D]">88% Stability</span>
                </div>
                <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                  <span className="text-[#5F6D67]">Water Binding:</span>
                  <span className="font-bold text-[#191C1E]">3.8g / g</span>
                </div>
              </div>
            )}

            {/* Tab 4: COMPLIANCE */}
            {activeModalTab === 'COMPLIANCE' && (
              <div className="space-y-2 text-xs font-mono">
                <div className="flex justify-between p-2.5 bg-emerald-50 rounded-lg border border-emerald-200 text-emerald-800 font-bold">
                  <span>US FDA Status:</span>
                  <span>Approved (GRAS)</span>
                </div>
                <div className="flex justify-between p-2.5 bg-emerald-50 rounded-lg border border-emerald-200 text-emerald-800 font-bold">
                  <span>EU EFSA Status:</span>
                  <span>Approved</span>
                </div>
                <div className="flex justify-between p-2.5 bg-[#FAFAF8] rounded-lg border border-[#E5E9E6]">
                  <span className="text-[#5F6D67]">Allergens:</span>
                  <span className="font-bold text-emerald-700">None (Hypoallergenic)</span>
                </div>
              </div>
            )}

            {/* Tab 5: KG RELATIONS (Live Interactive Cytoscape Knowledge Graph) */}
            {activeModalTab === 'KG RELATIONS' && (
              <div className="space-y-4 font-mono">
                <div className="p-3 bg-[#ECF4F0] rounded-xl border border-[#D1E2D9] space-y-1 text-xs">
                  <span className="text-[10px] font-bold text-[#164E3D] uppercase block">LIVE NEO4J SUBGRAPH NEIGHBORHOOD</span>
                  <div className="text-xs font-bold text-[#191C1E]">
                    (:Ingredient &#123;id: &ldquo;{selectedIngredient.id}&rdquo;, name: &ldquo;{selectedIngredient.name}&rdquo;&#125;)
                  </div>
                  <span className="text-[9px] text-[#5F6D67]">Data Source: {selectedIngredient.source}</span>
                </div>

                {/* Embedded Cytoscape Knowledge Graph Component */}
                <div className="h-[400px] w-full rounded-2xl overflow-hidden border border-[#E5E9E6]">
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
                className="w-full py-2.5 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-xs font-extrabold text-white transition shadow-sm"
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
