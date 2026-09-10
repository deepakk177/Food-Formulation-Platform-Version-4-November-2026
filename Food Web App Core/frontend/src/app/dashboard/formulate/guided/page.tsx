'use client';

import React, { useState, useEffect } from 'react';
import { useStore } from '@/store/useStore';
import { useRouter } from 'next/navigation';
import { 
  Loader2, Plus, X, Sparkles, Check, ArrowRight, ArrowLeft, 
  Search, ShieldAlert, Layers, Grid, Sliders, Filter, CheckCircle, Trash2,
  Tag, FileText, SlidersHorizontal, Package, Award, ArrowUpRight
} from 'lucide-react';
import FormulationResults from '@/components/formulation-results';
import AIProcessingState from '@/components/ai-processing-state';

interface ExtractedRequirementRow {
  id: string;
  category: 'Nutrition' | 'Functionality' | 'Processing' | 'Cost' | 'Sensory';
  name: string;
  target: string;
  type: 'HARD CONSTRAINT' | 'SOFT OBJECTIVE';
}

interface IngredientBundle {
  id: string;
  name: string;
  role: string;
  price: string;
  badge: string;
  ingredients: string[];
  selected: boolean;
}

const CATEGORIES = [
  'Confectionery & Chocolate',
  'Bakery & Cereals',
  'Beverages',
  'Dairy & Alternatives',
  'Snacks & Extruded',
  'Meat Analogues',
  'Sauces & Condiments'
];

const ALL_DIETARY_OPTIONS = [
  "Vegan", "Vegetarian", "Gluten-Free", "Dairy-Free", "Lactose-Free", 
  "Egg-Free", "Nut-Free", "Peanut-Free", "Soy-Free", "Sesame-Free", 
  "Allergen-Free", "Halal", "Kosher", "Non-GMO", "Organic", "Clean Label", 
  "Keto", "Low Sugar", "No Added Sugar", "Low Sodium", "High Protein", 
  "High Fibre", "Low Fat", "Low Saturated Fat"
];

const TEXTURE_OPTIONS = [
  "Smooth & Creamy",
  "Crunchy & Crispy",
  "Chewy & Fudgy",
  "Liquid / Viscous"
];

export default function GuidedFormulator() {
  const { token } = useStore();
  const router = useRouter();
  
  const [step, setStep] = useState(1);
  const [category, setCategory] = useState('Confectionery & Chocolate');
  const [query, setQuery] = useState('');
  
  // Step 2 State
  const [dietaryChips, setDietaryChips] = useState<string[]>(['Vegan', 'Gluten-Free', 'Low Sugar']);
  const [selectedTexture, setSelectedTexture] = useState('Smooth & Creamy');
  const [proteinTarget, setProteinTarget] = useState(20);
  const [showDietaryDropdown, setShowDietaryDropdown] = useState(false);
  const [searchDietary, setSearchDietary] = useState('');

  // Step 3 State
  const [extractedRequirements, setExtractedRequirements] = useState<ExtractedRequirementRow[]>([
    { id: 'req_1', category: 'Nutrition', name: 'Protein Concentration', target: '≥ 20%', type: 'SOFT OBJECTIVE' },
    { id: 'req_2', category: 'Nutrition', name: 'Sugar Limit', target: '≤ 5g / 100g', type: 'HARD CONSTRAINT' },
    { id: 'req_3', category: 'Functionality', name: 'Emulsion Stability Index', target: '≥ 85%', type: 'HARD CONSTRAINT' },
    { id: 'req_4', category: 'Processing', name: 'Water Activity (aw)', target: '≤ 0.60', type: 'HARD CONSTRAINT' },
    { id: 'req_5', category: 'Cost', name: 'Raw Material Cost', target: '≤ $4.50 / kg', type: 'HARD CONSTRAINT' },
    { id: 'req_6', category: 'Sensory', name: 'Flavor Profile', target: 'Clean Cocoa', type: 'SOFT OBJECTIVE' },
  ]);

  // Step 4 State
  const [viewMode, setViewMode] = useState<'bundles' | 'single'>('bundles');
  const [ingredientBundles, setIngredientBundles] = useState<IngredientBundle[]>([
    {
      id: 'b1',
      name: 'Pea & Rice Protein Synergy Set',
      role: 'Protein',
      price: '$12.40/kg',
      badge: 'MAIN PROTEIN',
      ingredients: ['Pea Protein Isolate (85%)', 'Organic Brown Rice Protein'],
      selected: true
    },
    {
      id: 'b2',
      name: 'Soluble Fiber & Prebiotic Matrix',
      role: 'Fiber',
      price: '$8.50/kg',
      badge: 'BULKING AGENT',
      ingredients: ['Soluble Corn Fiber', 'Chicory Root Inulin Fibre'],
      selected: true
    },
    {
      id: 'b3',
      name: 'Almond Butter & Lecithin Emulsion Set',
      role: 'Fats & Oils',
      price: '$14.20/kg',
      badge: 'FAT/TEXTURE',
      ingredients: ['Almond Butter (Smooth)', 'Sunflower Lecithin', 'Prime Press Cocoa Butter'],
      selected: true
    },
    {
      id: 'b4',
      name: 'Monk Fruit & Allulose Sweetener System',
      role: 'Sweetener',
      price: '$45.00/kg',
      badge: 'SWEETENER',
      ingredients: ['Monk Fruit Extract', 'Rare Sugar Allulose', 'Stevia Reb M'],
      selected: false
    },
    {
      id: 'b5',
      name: 'Hydrocolloid & Tapioca Stabilizer System',
      role: 'Emulsifier',
      price: '$10.50/kg',
      badge: 'EMULSIFIER',
      ingredients: ['Native Tapioca Starch', 'Xanthan Gum 200 Mesh'],
      selected: false
    }
  ]);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [results, setResults] = useState<any>(null);

  const addDietaryChip = (reqName: string) => {
    if (!reqName.trim()) return;
    const formatted = reqName.trim();
    if (!dietaryChips.includes(formatted)) {
      setDietaryChips([...dietaryChips, formatted]);
    }
    setShowDietaryDropdown(false);
    setSearchDietary('');
  };

  const removeDietaryChip = (reqName: string) => {
    setDietaryChips(dietaryChips.filter(c => c !== reqName));
  };

  const toggleRequirementGuard = (id: string) => {
    setExtractedRequirements(prev =>
      prev.map(row => (row.id === id ? { ...row, type: row.type === 'HARD CONSTRAINT' ? 'SOFT OBJECTIVE' : 'HARD CONSTRAINT' } : row))
    );
  };

  const removeRequirementRow = (id: string) => {
    setExtractedRequirements(prev => prev.filter(r => r.id !== id));
  };

  const toggleBundleSelection = (id: string) => {
    setIngredientBundles(prev =>
      prev.map(b => (b.id === id ? { ...b, selected: !b.selected } : b))
    );
  };

  const handleGenerate = async () => {
    setLoading(true);
    setError('');
    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      const briefPayload = {
        category,
        description: query || `Formulate a ${category} with target texture ${selectedTexture}.`,
        texture_requirements: [selectedTexture],
        dietary_requirements: dietaryChips,
        nutrition_targets: { protein_min: proteinTarget },
        excluded_ingredients: extractedRequirements.filter(r => r.type === 'HARD CONSTRAINT').map(r => r.name)
      };

      const res = await fetch(`${api_url}/api/formulation/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ product_brief: briefPayload, query })
      });

      if (!res.ok) {
        const errData = await res.json();
        throw new Error(errData.detail || 'Formulation pipeline generation failed.');
      }
      const data = await res.json();
      setResults(data);
      setStep(5);
    } catch (err: any) {
      setError(err.message || 'Generation failed');
    } finally {
      setLoading(false);
    }
  };

  const stepperIcons = [Tag, FileText, SlidersHorizontal, Package, Sparkles, Award];
  const stepperTitles = ['Product Category', 'Product Brief', 'Functional Goals', 'Ingredient Exploration', 'AI Recommendations', 'Review & Export'];

  return (
    <div className="w-full max-w-[1600px] mx-auto py-6 px-4 sm:px-6 lg:px-8 space-y-8">
      
      {/* Canonical Step Stepper Header (matching Screenshot 1 & 4) */}
      <div className="flex justify-between items-center max-w-4xl mx-auto px-4 overflow-x-auto">
        {stepperTitles.map((title, idx) => {
          const Icon = stepperIcons[idx];
          const isCompleted = step > idx + 1;
          const isActive = step === idx + 1;

          return (
            <React.Fragment key={title}>
              <div className="flex flex-col items-center gap-1.5 shrink-0 cursor-pointer" onClick={() => setStep(idx + 1)}>
                <div className={`h-10 w-10 rounded-full flex items-center justify-center border transition-all ${
                  isActive 
                    ? 'bg-[#164E3D] border-[#164E3D] text-white shadow-md' 
                    : isCompleted 
                    ? 'bg-[#ECF4F0] border-[#D1E2D9] text-[#164E3D]' 
                    : 'bg-white border-[#E5E9E6] text-[#5F6D67]'
                }`}>
                  <Icon className="h-5 w-5" />
                </div>
                <span className={`text-[11px] font-bold ${isActive ? 'text-[#164E3D]' : 'text-[#5F6D67]'}`}>
                  {title}
                </span>
              </div>

              {idx < stepperTitles.length - 1 && (
                <div className={`stepper-connector hidden sm:block ${step > idx + 1 ? 'stepper-connector-active' : ''}`} />
              )}
            </React.Fragment>
          );
        })}
      </div>

      {error && (
        <div className="rounded-xl bg-red-50 border border-red-200 p-4 text-xs text-red-700 font-sans">
          {error}
        </div>
      )}

      {/* STEP 1: Product Category (Exact match for Screenshot 1) */}
      {step === 1 && (
        <div className="space-y-6">
          <div className="text-center space-y-1">
            <span className="text-[10px] font-mono text-[#5F6D67] font-bold uppercase tracking-widest block">STEP 1 OF 6</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#191C1E] font-heading">Product Category</h2>
            <p className="text-[#5F6D67] text-xs">Select the product category for your formulation:</p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            
            {/* Left Category Selection List */}
            <div className="lg:col-span-7 space-y-3">
              {CATEGORIES.map((cat) => (
                <button
                  key={cat}
                  onClick={() => { setCategory(cat); }}
                  className={`w-full p-4 rounded-xl border text-left font-bold text-xs transition flex items-center justify-between ${
                    category === cat
                      ? 'border-[#164E3D] bg-white text-[#164E3D] shadow-sm'
                      : 'border-[#E5E9E6] bg-white text-[#191C1E] hover:border-[#164E3D]'
                  }`}
                >
                  <span>{cat}</span>
                  {category === cat && <Check className="h-4 w-4 text-[#164E3D]" />}
                </button>
              ))}
            </div>

            {/* Right Tip & Brief Card */}
            <div className="lg:col-span-5 space-y-4">
              <div className="p-4 rounded-xl bg-[#ECF4F0] border border-[#D1E2D9] space-y-2">
                <div className="flex items-center gap-2 text-xs font-bold text-[#164E3D]">
                  <Sparkles className="h-4 w-4 text-[#164E3D]" />
                  <span>Tip</span>
                </div>
                <p className="text-xs text-[#5F6D67] leading-relaxed">
                  Selecting the right category ensures our AI uses the most relevant regulatory and scientific datasets.
                </p>
              </div>

              <div className="canonical-card p-4 space-y-2">
                <span className="text-[10px] font-mono font-bold text-[#5F6D67] uppercase tracking-wider block">
                  YOUR BRIEF SO FAR
                </span>
                <div className="text-xs text-[#191C1E]">
                  Category: <span className="font-bold text-[#164E3D]">{category}</span>
                </div>
              </div>
            </div>

          </div>

          <div className="flex justify-end pt-4">
            <button
              onClick={() => setStep(2)}
              className="px-6 py-3 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white font-bold text-xs transition shadow-md flex items-center gap-2"
            >
              Continue to Brief
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 2: Define your Product Brief (Exact match for Screenshot 4) */}
      {step === 2 && (
        <div className="space-y-6">
          <div className="text-center space-y-1">
            <span className="text-[10px] font-mono text-[#5F6D67] font-bold uppercase tracking-widest block">STEP 2 OF 6</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#191C1E] font-heading">Define your Product Brief</h2>
            <p className="text-[#5F6D67] text-xs max-w-lg mx-auto leading-relaxed">
              Tell us about the core characteristics of your product. Our AI uses this information to search across 12M+ research papers for the most compatible ingredient pairings.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            
            {/* Left Card: Target Texture, Dietary Requirements, Slider */}
            <div className="lg:col-span-8 canonical-card p-6 space-y-6">
              
              {/* Target Texture & Mouthfeel */}
              <div className="space-y-3">
                <label className="text-xs font-bold text-[#191C1E] block">Target Texture & Mouthfeel</label>
                <div className="grid grid-cols-2 gap-3">
                  {TEXTURE_OPTIONS.map(tex => (
                    <button
                      key={tex}
                      type="button"
                      onClick={() => setSelectedTexture(tex)}
                      className={`p-3.5 rounded-xl border text-xs font-bold text-left transition flex items-center justify-between ${
                        selectedTexture === tex 
                          ? 'border-[#164E3D] bg-white text-[#164E3D] shadow-sm' 
                          : 'border-[#E5E9E6] bg-white text-[#5F6D67] hover:border-[#164E3D]'
                      }`}
                    >
                      <span>{tex}</span>
                      {selectedTexture === tex && <Check className="h-4 w-4 text-[#164E3D]" />}
                    </button>
                  ))}
                </div>
              </div>

              {/* Key Dietary Requirements */}
              <div className="space-y-3">
                <label className="text-xs font-bold text-[#191C1E] block">Key Dietary Requirements</label>
                <div className="flex flex-wrap gap-2 items-center">
                  {dietaryChips.map(chip => (
                    <span
                      key={chip}
                      className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold bg-[#164E3D] text-white shadow-sm"
                    >
                      {chip}
                      <button
                        type="button"
                        onClick={() => removeDietaryChip(chip)}
                        className="hover:text-red-300 transition"
                      >
                        <X className="h-3.5 w-3.5" />
                      </button>
                    </span>
                  ))}

                  <div className="relative">
                    <button
                      type="button"
                      onClick={() => setShowDietaryDropdown(!showDietaryDropdown)}
                      className="text-xs font-semibold text-[#5F6D67] hover:text-[#164E3D] border border-dashed border-[#5F6D67] px-3 py-1 rounded-full transition"
                    >
                      + Add Requirement
                    </button>

                    {showDietaryDropdown && (
                      <div className="absolute left-0 mt-2 w-64 canonical-card bg-white border border-[#E5E9E6] rounded-xl p-3 shadow-2xl z-50">
                        <input
                          type="text"
                          value={searchDietary}
                          onChange={(e) => setSearchDietary(e.target.value)}
                          placeholder="Search requirement..."
                          className="w-full bg-[#F7F9F8] border border-[#E5E9E6] text-xs text-[#191C1E] p-2 rounded-lg mb-2 focus:outline-none focus:border-[#164E3D]"
                        />
                        <div className="max-h-40 overflow-y-auto space-y-1">
                          {ALL_DIETARY_OPTIONS.filter(o => !dietaryChips.includes(o) && o.toLowerCase().includes(searchDietary.toLowerCase())).map(opt => (
                            <button
                              key={opt}
                              type="button"
                              onClick={() => addDietaryChip(opt)}
                              className="w-full text-left text-xs text-[#5F6D67] hover:text-[#164E3D] hover:bg-[#ECF4F0] p-1.5 rounded transition"
                            >
                              + {opt}
                            </button>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Protein Target Slider */}
              <div className="space-y-2 pt-2 border-t border-[#E5E9E6]">
                <div className="flex justify-between items-center text-xs font-bold text-[#191C1E]">
                  <span>Protein Target (%)</span>
                  <span className="font-mono text-[#164E3D]">{proteinTarget}%</span>
                </div>
                <input
                  type="range"
                  min={0}
                  max={90}
                  value={proteinTarget}
                  onChange={(e) => setProteinTarget(parseInt(e.target.value))}
                  className="w-full accent-[#164E3D] h-2 bg-[#E5E9E6] rounded-lg appearance-none cursor-pointer"
                />
              </div>

            </div>

            {/* Right Card: AI Intelligence Tip (Matching Screenshot 4) */}
            <div className="lg:col-span-4 p-5 rounded-2xl bg-[#ECF4F0] border border-[#D1E2D9] space-y-4">
              <div className="flex items-center gap-2 text-xs font-bold text-[#164E3D]">
                <Sparkles className="h-4 w-4" />
                <span>AI Intelligence Tip</span>
              </div>

              <p className="text-xs text-[#191C1E] italic leading-relaxed">
                &ldquo;Based on your <span className="font-bold">{selectedTexture}</span> requirement for a <span className="font-bold">{dietaryChips.join(', ')}</span> product, I recommend exploring <span className="font-bold text-[#164E3D]">Micronized Pea Protein</span> or <span className="font-bold text-[#164E3D]">Potato Protein</span>. These provide superior emulsification compared to standard soy isolates.&rdquo;
              </p>

              <div className="p-3 bg-white rounded-xl border border-[#D1E2D9] space-y-1">
                <span className="text-[9px] font-mono font-bold text-[#5F6D67] uppercase tracking-wider block">
                  SCIENTIFIC REFERENCE
                </span>
                <p className="text-[11px] font-mono text-[#191C1E]">
                  &ldquo;Functional properties of plant-based proteins in confectionery applications&rdquo; — Journal of Food Science (2023)
                </p>
              </div>

              <div className="text-[11px] font-mono text-[#164E3D] font-bold pt-2 flex items-center gap-1">
                <Check className="h-3.5 w-3.5" />
                Formulation Confidence: 88%
              </div>
            </div>

          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setStep(1)}
              className="px-6 py-3 rounded-xl border border-[#E5E9E6] hover:border-[#164E3D] text-xs font-bold text-[#5F6D67] hover:text-[#191C1E] transition flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Category
            </button>
            <button
              onClick={() => setStep(3)}
              className="px-6 py-3 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white font-bold text-xs transition shadow-md flex items-center gap-2"
            >
              Continue to Goals
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 3: Extracted Requirements */}
      {step === 3 && (
        <div className="space-y-6">
          <div className="text-center space-y-1">
            <span className="text-[10px] font-mono text-[#5F6D67] font-bold uppercase tracking-widest block">STEP 3 OF 6</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#191C1E] font-heading">Extracted Requirements</h2>
            <p className="text-[#5F6D67] text-xs">Configure hard veto constraints versus soft objectives:</p>
          </div>

          <div className="canonical-card p-6 space-y-4">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs divide-y divide-[#E5E9E6]">
                <thead>
                  <tr className="text-[#5F6D67] font-bold uppercase text-[10px] tracking-wider">
                    <th className="py-3 px-4">CATEGORY</th>
                    <th className="py-3 px-4">REQUIREMENT NAME</th>
                    <th className="py-3 px-4">TARGET</th>
                    <th className="py-3 px-4">TYPE</th>
                    <th className="py-3 px-4 text-right">TOGGLE GUARD</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E5E9E6] font-mono">
                  {extractedRequirements.map((row) => (
                    <tr key={row.id} className="hover:bg-[#F7F9F8]">
                      <td className="py-3 px-4">
                        <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-[#F7F9F8] border border-[#E5E9E6] text-[#5F6D67]">
                          {row.category}
                        </span>
                      </td>
                      <td className="py-3 px-4 font-sans font-bold text-[#191C1E]">{row.name}</td>
                      <td className="py-3 px-4 text-[#164E3D] font-bold">{row.target}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                          row.type === 'HARD CONSTRAINT' ? 'bg-red-50 text-red-700 border border-red-200' : 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                        }`}>
                          {row.type}
                        </span>
                      </td>
                      <td className="py-3 px-4 text-right">
                        <button
                          type="button"
                          onClick={() => toggleRequirementGuard(row.id)}
                          className="px-3 py-1 rounded-lg text-xs font-bold border border-[#E5E9E6] hover:border-[#164E3D] text-[#5F6D67] hover:text-[#164E3D] transition bg-white"
                        >
                          {row.type === 'HARD CONSTRAINT' ? 'Set Soft' : 'Set Hard'}
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setStep(2)}
              className="px-6 py-3 rounded-xl border border-[#E5E9E6] text-xs font-bold text-[#5F6D67] flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Brief
            </button>
            <button
              onClick={() => setStep(4)}
              className="px-6 py-3 rounded-xl bg-[#164E3D] text-white font-bold text-xs flex items-center gap-2"
            >
              Continue to Ingredients
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* STEP 4: Ingredient Exploration */}
      {step === 4 && (
        <div className="space-y-6">
          <div className="text-center space-y-1">
            <span className="text-[10px] font-mono text-[#5F6D67] font-bold uppercase tracking-widest block">STEP 4 OF 6</span>
            <h2 className="text-2xl sm:text-3xl font-extrabold text-[#191C1E] font-heading">Ingredient Exploration</h2>
            <p className="text-[#5F6D67] text-xs">Select candidate ingredients or functional ingredient sets:</p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {ingredientBundles.map(bundle => (
              <div
                key={bundle.id}
                onClick={() => toggleBundleSelection(bundle.id)}
                className={`canonical-card p-5 cursor-pointer transition-all hover-lift flex flex-col justify-between ${
                  bundle.selected ? 'border-[#164E3D] bg-[#ECF4F0]/30 shadow-md' : 'hover:border-[#164E3D]'
                }`}
              >
                <div>
                  <div className="flex justify-between items-start mb-2">
                    <span className="text-[10px] font-mono font-bold text-[#164E3D] bg-[#ECF4F0] px-2 py-0.5 rounded border border-[#D1E2D9]">
                      {bundle.badge}
                    </span>
                    {bundle.selected && <CheckCircle className="h-5 w-5 text-[#164E3D]" />}
                  </div>
                  <h4 className="font-bold text-sm text-[#191C1E] mt-2">{bundle.name}</h4>
                  <div className="mt-3 space-y-1">
                    {bundle.ingredients.map((ing, idx) => (
                      <div key={idx} className="text-xs text-[#5F6D67] font-mono flex items-center gap-1.5">
                        <span className="h-1.5 w-1.5 rounded-full bg-[#164E3D]" />
                        {ing}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="border-t border-[#E5E9E6] pt-3 mt-4 text-xs font-mono font-bold text-[#164E3D]">
                  {bundle.price}
                </div>
              </div>
            ))}
          </div>

          <div className="flex justify-between pt-4">
            <button
              onClick={() => setStep(3)}
              className="px-6 py-3 rounded-xl border border-[#E5E9E6] text-xs font-bold text-[#5F6D67] flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back
            </button>
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="px-6 py-3 rounded-xl bg-[#164E3D] text-white font-bold text-xs flex items-center gap-2 shadow-md disabled:opacity-50"
            >
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Sparkles className="h-4 w-4" />}
              Generate AI Recommendation →
            </button>
          </div>
        </div>
      )}

      {/* STEP 5: Formulation Results Presentation View */}
      {step === 5 && results && (
        <FormulationResults data={results} onReset={() => setStep(1)} />
      )}

    </div>
  );
}
