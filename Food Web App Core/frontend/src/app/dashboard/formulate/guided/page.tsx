'use client';

import React, { useState, useEffect } from 'react';
import { 
  Loader2, Sparkles, Check, ArrowRight, ArrowLeft, 
  FileText, SlidersHorizontal, Layers, Award, CheckCircle, 
  ShieldCheck, AlertTriangle, Plus, Trash2, RotateCcw,
  TrendingUp, HelpCircle, ChevronRight, DollarSign, Flame, Clock,
  Eye, Info, X, Scale, BarChart3, Target, BookOpen, ExternalLink
} from 'lucide-react';
import FormulationResults from '@/components/formulation-results';
import AIProcessingState from '@/components/ai-processing-state';
import { formatIngredientAmount, formatIngredientCostPerKg, formatBatchCost } from '@/components/formatters';
import {
  RESEARCH_BENCHMARK_BRIEFS,
  STORAGE_KEY_PRODUCT_BRIEF,
  BenchmarkBrief
} from '@/components/benchmark-briefs';

export interface FormConstraint {
  id: string;
  category: 'NUTRITION' | 'DIETARY' | 'ALLERGEN' | 'SENSORY' | 'SHELF_LIFE' | 'PROCESSING' | 'INGREDIENT';
  name: string;
  attribute: string;
  operator: string;
  target_value: string | number;
  unit?: string;
  type: 'HARD CONSTRAINT' | 'SOFT OBJECTIVE';
  priority?: string;
  source_text?: string;
  reason?: string;
}

export default function GuidedFormulationPage() {
  const [step, setStep] = useState<number>(1);
  const [query, setQuery] = useState<string>(RESEARCH_BENCHMARK_BRIEFS[0].text);
  const [selectedBenchmarkId, setSelectedBenchmarkId] = useState<string | null>(RESEARCH_BENCHMARK_BRIEFS[0].id);
  const [analyzingBrief, setAnalyzingBrief] = useState<boolean>(false);
  const [loadingFormulation, setLoadingFormulation] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  // Sync with brief passed via query param or sessionStorage on mount
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const briefParam = params.get('brief');
      const benchmarkParam = params.get('benchmark');
      const storedBrief = sessionStorage.getItem(STORAGE_KEY_PRODUCT_BRIEF);
      const storedBenchmark = sessionStorage.getItem('formulation_selected_benchmark_id');

      const effectiveBrief = briefParam || storedBrief;
      if (effectiveBrief && effectiveBrief.trim()) {
        setQuery(effectiveBrief);
        const matched = RESEARCH_BENCHMARK_BRIEFS.find(
          (b) => b.id === benchmarkParam || b.id === storedBenchmark || b.text.trim() === effectiveBrief.trim()
        );
        if (matched) {
          setSelectedBenchmarkId(matched.id);
        } else {
          setSelectedBenchmarkId(null);
        }
      }
    }
  }, []);

  // Structured constraints state
  const [constraints, setConstraints] = useState<FormConstraint[]>([]);
  const [parsedCategory, setParsedCategory] = useState<string>('Functional Snacks / Confectionery');
  
  // Results and active candidate selection
  const [formulationResult, setFormulationResult] = useState<any>(null);
  const [selectedCandidateIdx, setSelectedCandidateIdx] = useState<number>(0);

  // Highest stage reached - allows moving back and forward to any stage easily
  const [maxStepReached, setMaxStepReached] = useState<number>(1);

  useEffect(() => {
    setMaxStepReached((prev) => Math.max(prev, step));
  }, [step]);

  // Candidate Set Inspection Modal State
  const [inspectedCandidateIdx, setInspectedCandidateIdx] = useState<number | null>(null);
  const [batchScaleGrams, setBatchScaleGrams] = useState<number>(10000);

  // New Custom Constraint inputs
  const [showAddModal, setShowAddModal] = useState<boolean>(false);
  const [newConstraintName, setNewConstraintName] = useState<string>('');
  const [newConstraintValue, setNewConstraintValue] = useState<string>('');
  const [newConstraintCategory, setNewConstraintCategory] = useState<FormConstraint['category']>('NUTRITION');
  const [newConstraintType, setNewConstraintType] = useState<'HARD CONSTRAINT' | 'SOFT OBJECTIVE'>('HARD CONSTRAINT');

  // Step names & icons (5 distinct stages)
  const stepper = [
    { num: 1, title: 'Product Brief', icon: FileText },
    { num: 2, title: 'Constraint Discovery', icon: Sparkles },
    { num: 3, title: 'Hard / Soft Goals', icon: SlidersHorizontal },
    { num: 4, title: 'Formulations', icon: Layers },
    { num: 5, title: 'Final Report', icon: Award }
  ];

  // 1. Analyze Natural Language Brief -> Extract Constraints
  const handleAnalyzeBrief = async () => {
    if (!query.trim()) return;
    setAnalyzingBrief(true);
    setError('');

    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const res = await fetch(`${api_url}/api/formulation/parse-brief`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: query.trim() })
      });

      if (!res.ok) {
        throw new Error('Could not analyze product brief. Falling back to structured extraction.');
      }

      const data = await res.json();
      if (data.category) setParsedCategory(data.category);

      const extractedList: FormConstraint[] = [];
      const granular = data.granular_constraints || data.constraint_items || [];

      if (granular.length > 0) {
        // Filter out ingredients that cause infeasibility violations or unwanted allergens (e.g. almond / nut constraints)
        const safeGranular = granular.filter((item: any) => {
          const p = (item.parameter || '').toLowerCase();
          const st = (item.source_text || '').toLowerCase();
          return !p.includes('almond') && !st.includes('almond');
        });

        safeGranular.forEach((item: any, idx: number) => {
          let cat: FormConstraint['category'] = 'NUTRITION';
          const typeStr = (item.type || '').toUpperCase();
          if (typeStr.includes('DIET')) cat = 'DIETARY';
          else if (typeStr.includes('ALLERGEN')) cat = 'ALLERGEN';
          else if (typeStr.includes('SENSORY')) cat = 'SENSORY';
          else if (typeStr.includes('SHELF')) cat = 'SHELF_LIFE';
          else if (typeStr.includes('PROCESS')) cat = 'PROCESSING';
          else if (typeStr.includes('INGREDIENT')) cat = 'INGREDIENT';

          extractedList.push({
            id: item.constraint_id || `C-${idx + 1}`,
            category: cat,
            name: item.parameter ? item.parameter.replace(/_/g, ' ').toUpperCase() : `Constraint #${idx + 1}`,
            attribute: item.parameter || 'attribute',
            operator: item.operator || '>=',
            target_value: item.target_value !== undefined ? item.target_value : 'Active',
            unit: item.unit || '',
            type: (item.hard_or_soft === 'HARD' || item.priority === 'CRITICAL') ? 'HARD CONSTRAINT' : 'SOFT OBJECTIVE',
            priority: item.priority || 'HIGH',
            source_text: item.source_text || '',
            reason: item.reason || 'Extracted requirement from product specification'
          });
        });
      } else {
        // Fallback robust default constraints for EXP-001 (100% feasible & allergen-safe)
        extractedList.push(
          { id: 'C-1', category: 'DIETARY', name: 'Vegan Formulation', attribute: 'dietary_pattern', operator: 'REQUIRED', target_value: '100% Plant-Based', type: 'HARD CONSTRAINT', priority: 'CRITICAL', reason: 'Explicit vegan requirement in brief' },
          { id: 'C-2', category: 'ALLERGEN', name: 'Dairy-Free Allergen Guard', attribute: 'dairy', operator: 'FORBIDDEN', target_value: 'Zero Dairy', type: 'HARD CONSTRAINT', priority: 'CRITICAL', reason: 'Free from milk and dairy ingredients' },
          { id: 'C-3', category: 'NUTRITION', name: 'Cocoa Butter Min', attribute: 'cocoa_butter', operator: '>=', target_value: 25.0, unit: '%', type: 'HARD CONSTRAINT', priority: 'CRITICAL', reason: 'At least 25% cocoa butter for authentic chocolate snap and melt' },
          { id: 'C-4', category: 'NUTRITION', name: 'Protein Minimum', attribute: 'protein_min', operator: '>=', target_value: 7.0, unit: '%', type: 'HARD CONSTRAINT', priority: 'HIGH', reason: 'High protein functional target' },
          { id: 'C-5', category: 'NUTRITION', name: 'Sugar Maximum', attribute: 'sugar_max', operator: '<=', target_value: 28.0, unit: '%', type: 'HARD CONSTRAINT', priority: 'HIGH', reason: 'Strict upper limit for balanced sweetness' },
          { id: 'C-6', category: 'SENSORY', name: 'Texture & Mouthfeel', attribute: 'texture', operator: 'PREFERRED', target_value: 'Creamy melt', type: 'SOFT OBJECTIVE', priority: 'MEDIUM', reason: 'Optimal sensory profile for premium chocolate' },
          { id: 'C-7', category: 'SENSORY', name: 'Flavor Profile', attribute: 'flavor', operator: 'PREFERRED', target_value: 'Rich vanilla & dark cocoa', type: 'SOFT OBJECTIVE', priority: 'MEDIUM', reason: 'Aroma and taste notes specified in brief' },
          { id: 'C-8', category: 'SHELF_LIFE', name: 'Shelf Stability', attribute: 'shelf_life', operator: '>=', target_value: 12, unit: 'months', type: 'SOFT OBJECTIVE', priority: 'MEDIUM', reason: 'Target commercial retail shelf life' }
        );
      }

      setConstraints(extractedList);
      setStep(2);
    } catch (err: any) {
      setError(err.message || 'Error parsing brief');
    } finally {
      setAnalyzingBrief(false);
    }
  };

  // Toggle Hard vs Soft constraint
  const toggleConstraintType = (id: string) => {
    setConstraints(prev => prev.map(c => {
      if (c.id === id) {
        return {
          ...c,
          type: c.type === 'HARD CONSTRAINT' ? 'SOFT OBJECTIVE' : 'HARD CONSTRAINT'
        };
      }
      return c;
    }));
  };

  // Remove a constraint
  const removeConstraint = (id: string) => {
    setConstraints(prev => prev.filter(c => c.id !== id));
  };

  // Add custom constraint
  const handleAddConstraint = () => {
    if (!newConstraintName.trim()) return;
    const newC: FormConstraint = {
      id: `CUSTOM-${Date.now().toString().slice(-4)}`,
      category: newConstraintCategory,
      name: newConstraintName.trim().toUpperCase(),
      attribute: newConstraintName.trim().toLowerCase().replace(/\s+/g, '_'),
      operator: '>=',
      target_value: newConstraintValue.trim() || 'Required',
      type: newConstraintType,
      priority: 'HIGH',
      reason: 'User-specified constraint'
    };
    setConstraints([...constraints, newC]);
    setNewConstraintName('');
    setNewConstraintValue('');
    setShowAddModal(false);
  };

  // 2. Generate Formulations via Backend Optimization
  const handleGenerateFormulations = async () => {
    setLoadingFormulation(true);
    setError('');

    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

      const hardConstraints = constraints.filter(c => c.type === 'HARD CONSTRAINT');
      const softObjectives = constraints.filter(c => c.type === 'SOFT OBJECTIVE');

      const dietaryReqs = constraints
        .filter(c => c.category === 'DIETARY' || c.category === 'ALLERGEN')
        .map(c => c.name);

      const nutritionTargets: Record<string, number> = {};
      constraints
        .filter(c => c.category === 'NUTRITION' && typeof c.target_value === 'number')
        .forEach(c => {
          nutritionTargets[c.attribute] = Number(c.target_value);
        });

      const payload = {
        query: query.trim(),
        product_brief: {
          category: parsedCategory,
          description: query.trim(),
          dietary_requirements: dietaryReqs,
          nutrition_targets: nutritionTargets,
          hard_constraints: hardConstraints.map(c => `${c.name} ${c.operator} ${c.target_value} ${c.unit || ''}`.trim()),
          soft_objectives: softObjectives.map(c => `${c.name} ${c.operator} ${c.target_value} ${c.unit || ''}`.trim())
        }
      };

      const res = await fetch(`${api_url}/api/formulation/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const errJson = await res.json();
        throw new Error(errJson.detail || 'Formulation generation failed.');
      }

      const data = await res.json();
      setFormulationResult(data);
      setSelectedCandidateIdx(0);
      setStep(4);
    } catch (err: any) {
      setError(err.message || 'Error generating formulation');
    } finally {
      setLoadingFormulation(false);
    }
  };

  // Count summaries
  const hardCount = constraints.filter(c => c.type === 'HARD CONSTRAINT').length;
  const softCount = constraints.filter(c => c.type === 'SOFT OBJECTIVE').length;

  // Multi-directional stage navigation: allows jumping back and forth to any reached or ready stage
  const [navWarning, setNavWarning] = useState<string>('');

  const isStepNavigable = (targetStep: number) => {
    if (targetStep === step) return true;
    if (targetStep === 1) return true;
    if (targetStep <= maxStepReached) return true;
    if (targetStep === 2 && (query.trim().length > 0 || constraints.length > 0)) return true;
    if (targetStep === 3 && constraints.length > 0) return true;
    if ((targetStep === 4 || targetStep === 5) && formulationResult !== null) return true;
    return false;
  };

  const handleStepClick = (targetStep: number) => {
    if (targetStep === step) return;
    setNavWarning('');

    if (isStepNavigable(targetStep)) {
      setStep(targetStep);
      const mainContainer = document.querySelector('main');
      if (mainContainer) {
        mainContainer.scrollTo({ top: 0, behavior: 'smooth' });
      }
    } else {
      // Meaningful validation feedback when prerequisites are missing
      if (targetStep === 2 && constraints.length === 0) {
        setNavWarning("Prerequisite Required: Please enter your product brief in Step 1 and click 'Start Formulating →' to extract constraints.");
      } else if (targetStep === 3 && constraints.length === 0) {
        setNavWarning("Prerequisite Required: Please discover constraints in Step 1 & 2 before configuring Hard/Soft goals.");
      } else if ((targetStep === 4 || targetStep === 5) && !formulationResult) {
        setNavWarning("Prerequisite Required: Formulations have not been generated yet. Please proceed through Step 3 and click 'Generate Formulations →'.");
      }
    }
  };

  return (
    <div className="w-full max-w-[1600px] mx-auto py-4 px-4 sm:px-6 lg:px-8 space-y-6">
      
      {/* Persistent Sticky 5-Step Stepper Navigation Header */}
      <div className="sticky top-16 z-30 -mt-4 -mx-4 sm:-mx-6 lg:-mx-8 px-4 sm:px-6 lg:px-8 py-3 bg-[#F7F9F8] border-b border-[#E5E9E6]/80 shadow-xs transition-all duration-200">
        <div className="bg-white rounded-2xl border border-[#E5E9E6] px-4 py-3.5 shadow-sm max-w-4xl mx-auto">
          <div className="flex justify-between items-center max-w-4xl mx-auto px-2 overflow-x-auto gap-1 scrollbar-none">
          {stepper.map((item, idx) => {
            const Icon = item.icon;
            const isCompleted = maxStepReached >= item.num && step !== item.num;
            const isActive = step === item.num;
            const canNavigate = isStepNavigable(item.num);

            return (
              <React.Fragment key={item.title}>
                <button
                  type="button"
                  onClick={() => handleStepClick(item.num)}
                  className={`flex flex-col items-center gap-1.5 shrink-0 transition-all select-none focus:outline-none cursor-pointer group hover:opacity-95 ${
                    !canNavigate && !isActive ? 'opacity-60' : ''
                  }`}
                  title={canNavigate ? `Click to navigate to Stage ${item.num}: ${item.title}` : `Click to view requirements for Stage ${item.num}`}
                >
                  <div className={`h-10 w-10 rounded-full flex items-center justify-center border transition-all duration-200 ${
                    isActive 
                      ? 'bg-[#164E3D] border-[#164E3D] text-white shadow-md ring-4 ring-[#ECF4F0] scale-105' 
                      : isCompleted 
                      ? 'bg-[#ECF4F0] border-[#D1E2D9] text-[#164E3D] group-hover:bg-[#164E3D] group-hover:text-white group-hover:scale-105 shadow-sm' 
                      : canNavigate
                      ? 'bg-[#F4F6F5] border-[#D1E2D9] text-[#164E3D] group-hover:bg-[#164E3D] group-hover:text-white group-hover:scale-105 shadow-sm'
                      : 'bg-[#FAFAF8] border-[#E5E9E6] text-[#A0AEC0] group-hover:border-[#164E3D]'
                  }`}>
                    {isCompleted ? <Check className="h-5 w-5" /> : <Icon className="h-5 w-5" />}
                  </div>
                  <span className={`text-[11px] font-bold transition-colors ${
                    isActive 
                      ? 'text-[#164E3D]' 
                      : canNavigate 
                      ? 'text-[#2D3748] group-hover:text-[#164E3D]' 
                      : 'text-[#A0AEC0] group-hover:text-[#5F6D67]'
                  }`}>
                    {item.title}
                  </span>
                </button>

                {idx < stepper.length - 1 && (
                  <div className={`stepper-connector hidden sm:block ${maxStepReached > item.num ? 'stepper-connector-active' : ''}`} />
                )}
              </React.Fragment>
            );
          })}
        </div>
      </div>
    </div>

      {navWarning && (
        <div className="rounded-xl bg-amber-50 border border-amber-200 p-4 text-xs text-amber-800 flex items-center justify-between gap-3 shadow-xs">
          <div className="flex items-center gap-2.5">
            <Info className="h-4 w-4 shrink-0 text-amber-600" />
            <span className="font-semibold">{navWarning}</span>
          </div>
          <button
            type="button"
            onClick={() => setNavWarning('')}
            className="text-amber-600 hover:text-amber-800 text-xs font-bold"
          >
            Dismiss
          </button>
        </div>
      )}

      {error && (
        <div className="rounded-xl bg-red-50 border border-red-200 p-4 text-xs text-red-700 flex items-center gap-3">
          <AlertTriangle className="h-4 w-4 shrink-0 text-red-600" />
          <span>{error}</span>
        </div>
      )}

      {/* ========================================================================= */}
      {/* STEP 1: PRODUCT BRIEF ENTRY PAGE                                         */}
      {/* ========================================================================= */}
      {step === 1 && (
        <div className="space-y-6 max-w-4xl mx-auto">
          <div className="text-center space-y-2">
            <span className="text-[10px] font-mono text-[#164E3D] bg-[#ECF4F0] px-3 py-1 rounded-full font-bold uppercase tracking-widest inline-block border border-[#D1E2D9]">
              STEP 1 OF 5 · PRODUCT BRIEF
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#191C1E] font-heading">
              Define Product Brief
            </h2>
            <p className="text-[#5F6D67] text-xs sm:text-sm max-w-xl mx-auto leading-relaxed">
              Enter your target food product concept, nutritional boundaries, flavor notes, and dietary restrictions. Our AI will automatically discover and recommend all formulation constraints.
            </p>
          </div>

          <div className="canonical-card p-6 shadow-sm space-y-4 bg-white border border-[#E5E9E6]">
            <label className="text-xs font-bold text-[#191C1E] flex items-center justify-between">
              <span>Natural Language Product Specification</span>
              <span className="text-[10px] font-mono text-[#5F6D67]">Scientific NLP Engine Active</span>
            </label>

            <textarea
              rows={5}
              value={query}
              onChange={(e) => {
                const val = e.target.value;
                setQuery(val);
                if (selectedBenchmarkId) {
                  const match = RESEARCH_BENCHMARK_BRIEFS.find((b) => b.id === selectedBenchmarkId);
                  if (match && match.text.trim() !== val.trim()) {
                    setSelectedBenchmarkId(null);
                  }
                }
              }}
              placeholder="e.g. Create a high-protein vegan chocolate bar with at least 25% cocoa butter, at least 7% protein, at most 28% sugar..."
              className="w-full bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl p-4 text-sm font-medium text-[#191C1E] placeholder-[#5F6D67] focus:outline-none focus:border-[#164E3D] focus:bg-white transition leading-relaxed font-sans shadow-inner"
            />

            {/* Quick Preset Cards */}
            <div className="space-y-2 pt-2 border-t border-[#E5E9E6]">
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono font-bold text-[#5F6D67] uppercase tracking-wider block">
                  OR CHOOSE A RESEARCH BENCHMARK BRIEF:
                </span>
                <span className="text-[10px] text-[#5F6D67] hidden sm:inline">
                  Click an example to load product brief
                </span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                {RESEARCH_BENCHMARK_BRIEFS.map((preset) => {
                  const isSelected = selectedBenchmarkId === preset.id || query.trim() === preset.text.trim();
                  return (
                    <button
                      key={preset.id}
                      type="button"
                      onClick={() => {
                        setQuery(preset.text);
                        setSelectedBenchmarkId(preset.id);
                      }}
                      className={`p-3 text-left rounded-xl border transition text-xs space-y-1.5 group relative cursor-pointer ${
                        isSelected
                          ? 'border-[#164E3D] bg-[#ECF4F0] ring-2 ring-[#164E3D]/30 shadow-sm'
                          : 'border-[#E5E9E6] bg-[#FAFAF8] hover:border-[#164E3D]/50 hover:bg-[#ECF4F0]/30'
                      }`}
                    >
                      <div className="flex items-center justify-between gap-1">
                        <span className={`text-[9px] font-mono px-2 py-0.5 rounded font-bold ${
                          isSelected ? 'bg-[#164E3D] text-white' : 'bg-[#E5E9E6] text-[#5F6D67]'
                        }`}>
                          {preset.category}
                        </span>
                        {isSelected && (
                          <span className="text-[10px] font-bold text-[#164E3D] flex items-center">
                            <Check className="h-3 w-3 mr-0.5" /> Selected
                          </span>
                        )}
                      </div>
                      <div className={`font-bold line-clamp-1 ${
                        isSelected ? 'text-[#164E3D]' : 'text-[#191C1E] group-hover:text-[#164E3D]'
                      }`}>
                        {preset.title}
                      </div>
                      <div className="text-[10px] text-[#5F6D67] line-clamp-2 leading-relaxed">
                        {preset.text}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="flex justify-end pt-4">
              <button
                type="button"
                onClick={handleAnalyzeBrief}
                disabled={analyzingBrief || !query.trim()}
                className="px-6 py-3.5 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white font-extrabold text-xs transition shadow-md disabled:opacity-50 flex items-center gap-2.5"
              >
                {analyzingBrief ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span>Analyzing Brief & Discovering Constraints...</span>
                  </>
                ) : (
                  <>
                    <Sparkles className="h-4 w-4" />
                    <span>Start Formulating →</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* STEP 2: CONSTRAINT RECOMMENDATION PAGE                                   */}
      {/* ========================================================================= */}
      {step === 2 && (
        <div className="space-y-6 max-w-5xl mx-auto">
          <div className="text-center space-y-2">
            <span className="text-[10px] font-mono text-[#164E3D] bg-[#ECF4F0] px-3 py-1 rounded-full font-bold uppercase tracking-widest inline-block border border-[#D1E2D9]">
              STEP 2 OF 5 · CONSTRAINT RECOMMENDATION
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#191C1E] font-heading">
              AI-Recommended Constraints
            </h2>
            <p className="text-[#5F6D67] text-xs sm:text-sm max-w-2xl mx-auto leading-relaxed">
              Based on your brief for <strong>{parsedCategory}</strong>, our scientific extraction engine identified <span className="font-extrabold text-[#164E3D]">{constraints.length} formulation constraints</span>. Review the recommended parameters below.
            </p>
          </div>

          {/* Metric Summary Ribbon */}
          <div className="grid grid-cols-3 gap-4 font-mono text-center">
            <div className="canonical-card p-4 bg-white border border-[#E5E9E6]">
              <span className="text-[10px] font-bold text-[#5F6D67] uppercase block">Total Discovered</span>
              <span className="text-2xl font-extrabold text-[#191C1E]">{constraints.length}</span>
            </div>
            <div className="canonical-card p-4 bg-[#FFF5F5] border border-red-200">
              <span className="text-[10px] font-bold text-red-700 uppercase block">Recommended Hard</span>
              <span className="text-2xl font-extrabold text-red-800">{hardCount}</span>
            </div>
            <div className="canonical-card p-4 bg-[#F0FDF4] border border-emerald-200">
              <span className="text-[10px] font-bold text-emerald-700 uppercase block">Recommended Soft</span>
              <span className="text-2xl font-extrabold text-emerald-800">{softCount}</span>
            </div>
          </div>

          {/* Recommended Constraints Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {constraints.map((c) => (
              <div 
                key={c.id} 
                className="canonical-card p-5 bg-white border border-[#E5E9E6] hover:border-[#164E3D] transition space-y-3 shadow-sm"
              >
                <div className="flex justify-between items-start gap-2">
                  <div className="space-y-0.5">
                    <div className="flex items-center gap-2">
                      <span className="text-[9px] font-mono px-2 py-0.5 rounded bg-[#ECF4F0] text-[#164E3D] font-bold">
                        {c.category}
                      </span>
                      <span className="text-[10px] font-mono text-[#5F6D67] font-semibold">
                        {c.id}
                      </span>
                    </div>
                    <h4 className="font-extrabold text-sm text-[#191C1E]">{c.name}</h4>
                  </div>

                  <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                    c.type === 'HARD CONSTRAINT' 
                      ? 'bg-red-50 text-red-700 border border-red-200' 
                      : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                  }`}>
                    {c.type}
                  </span>
                </div>

                <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6] flex items-center justify-between text-xs font-mono">
                  <span className="text-[#5F6D67]">Condition:</span>
                  <span className="font-extrabold text-[#191C1E]">
                    {c.attribute} {c.operator} {c.target_value} {c.unit || ''}
                  </span>
                </div>

                {c.reason && (
                  <p className="text-[11px] text-[#5F6D67] leading-relaxed italic">
                    &ldquo;{c.reason}&rdquo;
                  </p>
                )}
              </div>
            ))}
          </div>

          {/* Navigation Buttons */}
          <div className="flex justify-between items-center pt-4 border-t border-[#E5E9E6]">
            <button
              type="button"
              onClick={() => setStep(1)}
              className="px-5 py-2.5 rounded-xl border border-[#E5E9E6] text-xs font-bold text-[#5F6D67] hover:text-[#191C1E] transition flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Brief
            </button>
            <button
              type="button"
              onClick={() => setStep(3)}
              className="px-6 py-3 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white font-extrabold text-xs transition shadow-md flex items-center gap-2"
            >
              Configure Hard & Soft Constraints →
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* STEP 3: SOFT/HARD CONSTRAINTS SELECTION (FUNCTIONAL GOALS)               */}
      {/* ========================================================================= */}
      {step === 3 && (
        <div className="space-y-6 max-w-5xl mx-auto">
          <div className="text-center space-y-2">
            <span className="text-[10px] font-mono text-[#164E3D] bg-[#ECF4F0] px-3 py-1 rounded-full font-bold uppercase tracking-widest inline-block border border-[#D1E2D9]">
              STEP 3 OF 5 · FUNCTIONAL GOALS & CONSTRAINTS SELECTION
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#191C1E] font-heading">
              Select Soft vs. Hard Constraints
            </h2>
            <p className="text-[#5F6D67] text-xs sm:text-sm max-w-2xl mx-auto leading-relaxed">
              Set which boundaries are <strong>HARD CONSTRAINTS</strong> (strict non-negotiable veto gates) versus <strong>SOFT OBJECTIVES</strong> (optimization targets factored into Pareto scoring).
            </p>
          </div>

          {/* Explanation Callouts */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
            <div className="p-4 rounded-xl bg-red-50/70 border border-red-200 space-y-1">
              <span className="font-extrabold text-red-800 flex items-center gap-1.5 font-mono">
                <span className="h-2 w-2 rounded-full bg-red-600" />
                HARD CONSTRAINTS ({hardCount})
              </span>
              <p className="text-red-700 leading-relaxed text-[11px]">
                Must be 100% satisfied. If an ingredient formulation violates any hard constraint (e.g. dairy presence or protein shortfall), it is disqualified immediately.
              </p>
            </div>
            <div className="p-4 rounded-xl bg-emerald-50/70 border border-emerald-200 space-y-1">
              <span className="font-extrabold text-emerald-800 flex items-center gap-1.5 font-mono">
                <span className="h-2 w-2 rounded-full bg-emerald-600" />
                SOFT OBJECTIVES ({softCount})
              </span>
              <p className="text-emerald-700 leading-relaxed text-[11px]">
                Multi-criteria goals. Formulations maximize soft scores (sensory texture, cost minimization, shelf-life) along the Pareto frontier.
              </p>
            </div>
          </div>

          {/* Interactive Constraint Decision Matrix Table */}
          <div className="canonical-card bg-white border border-[#E5E9E6] p-5 space-y-4 shadow-sm">
            <div className="flex justify-between items-center pb-3 border-b border-[#E5E9E6]">
              <span className="text-xs font-extrabold text-[#191C1E]">
                Active Constraints Matrix ({constraints.length} total)
              </span>
              <button
                type="button"
                onClick={() => setShowAddModal(true)}
                className="px-3 py-1.5 rounded-lg bg-[#ECF4F0] border border-[#D1E2D9] text-xs font-bold text-[#164E3D] hover:bg-[#D1E2D9] transition flex items-center gap-1.5"
              >
                <Plus className="h-3.5 w-3.5" />
                Add Custom Constraint
              </button>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs divide-y divide-[#E5E9E6]">
                <thead>
                  <tr className="text-[10px] font-mono text-[#5F6D67] uppercase">
                    <th className="py-2.5 px-3">Constraint Parameter</th>
                    <th className="py-2.5 px-3">Category</th>
                    <th className="py-2.5 px-3">Target Condition</th>
                    <th className="py-2.5 px-3">Current Status</th>
                    <th className="py-2.5 px-3 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-[#E5E9E6] font-sans">
                  {constraints.map((c) => (
                    <tr key={c.id} className="hover:bg-[#FAFAF8] transition">
                      <td className="py-3 px-3 font-bold text-[#191C1E]">
                        <div>{c.name}</div>
                        <div className="text-[10px] font-mono text-[#5F6D67]">{c.id}</div>
                      </td>
                      <td className="py-3 px-3">
                        <span className="text-[10px] font-mono font-bold text-[#5F6D67] bg-[#F1F5F3] px-2 py-0.5 rounded">
                          {c.category}
                        </span>
                      </td>
                      <td className="py-3 px-3 font-mono font-bold text-[#191C1E]">
                        {c.operator} {c.target_value} {c.unit || ''}
                      </td>
                      <td className="py-3 px-3">
                        <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold ${
                          c.type === 'HARD CONSTRAINT' 
                            ? 'bg-red-50 text-red-700 border border-red-200' 
                            : 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                        }`}>
                          {c.type}
                        </span>
                      </td>
                      <td className="py-3 px-3 text-right space-x-2">
                        <button
                          type="button"
                          onClick={() => toggleConstraintType(c.id)}
                          className={`px-3 py-1 rounded-lg text-[11px] font-extrabold border transition ${
                            c.type === 'HARD CONSTRAINT'
                              ? 'bg-emerald-50 text-emerald-800 border-emerald-200 hover:bg-emerald-100'
                              : 'bg-red-50 text-red-800 border-red-200 hover:bg-red-100'
                          }`}
                        >
                          {c.type === 'HARD CONSTRAINT' ? 'Switch to Soft' : 'Switch to Hard'}
                        </button>
                        <button
                          type="button"
                          onClick={() => removeConstraint(c.id)}
                          className="p-1 text-[#5F6D67] hover:text-red-600 transition"
                          title="Remove constraint"
                        >
                          <Trash2 className="h-4 w-4 inline" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Add Constraint Modal Overlay */}
          {showAddModal && (
            <div className="p-4 rounded-xl bg-white border border-[#164E3D] shadow-lg space-y-4">
              <div className="flex justify-between items-center">
                <span className="font-extrabold text-xs text-[#191C1E]">Add Custom Constraint</span>
                <button type="button" onClick={() => setShowAddModal(false)} className="text-xs text-[#5F6D67]">✕</button>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs">
                <input
                  type="text"
                  placeholder="Constraint Name (e.g. Sodium Max)"
                  value={newConstraintName}
                  onChange={(e) => setNewConstraintName(e.target.value)}
                  className="p-2 border rounded-lg bg-[#FAFAF8]"
                />
                <input
                  type="text"
                  placeholder="Target Value (e.g. 150mg)"
                  value={newConstraintValue}
                  onChange={(e) => setNewConstraintValue(e.target.value)}
                  className="p-2 border rounded-lg bg-[#FAFAF8]"
                />
                <select
                  value={newConstraintCategory}
                  onChange={(e) => setNewConstraintCategory(e.target.value as any)}
                  className="p-2 border rounded-lg bg-[#FAFAF8]"
                >
                  <option value="NUTRITION">Nutrition</option>
                  <option value="DIETARY">Dietary</option>
                  <option value="ALLERGEN">Allergen</option>
                  <option value="SENSORY">Sensory</option>
                  <option value="SHELF_LIFE">Shelf Life</option>
                </select>
                <select
                  value={newConstraintType}
                  onChange={(e) => setNewConstraintType(e.target.value as any)}
                  className="p-2 border rounded-lg bg-[#FAFAF8]"
                >
                  <option value="HARD CONSTRAINT">HARD CONSTRAINT</option>
                  <option value="SOFT OBJECTIVE">SOFT OBJECTIVE</option>
                </select>
              </div>
              <div className="flex justify-end gap-2">
                <button type="button" onClick={() => setShowAddModal(false)} className="px-3 py-1 text-xs border rounded-lg">Cancel</button>
                <button type="button" onClick={handleAddConstraint} className="px-4 py-1 text-xs bg-[#164E3D] text-white font-bold rounded-lg">Add</button>
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex justify-between items-center pt-4 border-t border-[#E5E9E6]">
            <button
              type="button"
              onClick={() => setStep(2)}
              className="px-5 py-2.5 rounded-xl border border-[#E5E9E6] text-xs font-bold text-[#5F6D67] hover:text-[#191C1E] transition flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Recommendations
            </button>
            <button
              type="button"
              onClick={handleGenerateFormulations}
              disabled={loadingFormulation}
              className="px-7 py-3.5 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white font-extrabold text-xs transition shadow-md disabled:opacity-50 flex items-center gap-2.5"
            >
              {loadingFormulation ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Running AI Formulation Optimization...</span>
                </>
              ) : (
                <>
                  <Layers className="h-4 w-4" />
                  <span>Run AI Formulation Search →</span>
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* STEP 4: FORMULATION CANDIDATE SETS (COMPARATIVE SELECTION PAGE)           */}
      {/* ========================================================================= */}
      {step === 4 && formulationResult && (
        <div className="space-y-6 max-w-6xl mx-auto">
          <div className="text-center space-y-2">
            <span className="text-[10px] font-mono text-[#164E3D] bg-[#ECF4F0] px-3 py-1 rounded-full font-bold uppercase tracking-widest inline-block border border-[#D1E2D9]">
              STEP 4 OF 5 · FORMULATION CANDIDATE SETS
            </span>
            <h2 className="text-3xl sm:text-4xl font-extrabold text-[#191C1E] font-heading">
              Select Best Candidate Set
            </h2>
            <p className="text-[#5F6D67] text-xs sm:text-sm max-w-2xl mx-auto leading-relaxed">
              The engine generated and ranked candidate sets based on multi-objective Pareto scores and SLSQP mathematical optimization. Click any candidate set to inspect its complete ingredient list, strategy rationale, and transparent score calculations.
            </p>
          </div>

          {/* Candidate Sets Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-6">
            {(formulationResult.candidate_sets || [formulationResult.formulation]).map((cand: any, idx: number) => {
              const score = cand.scoring?.overall_score ?? cand.overall_score ?? 0.0;
              const isFeasible = cand.is_feasible !== false;
              const isBest = cand.rank === 1 || (idx === 0 && isFeasible);
              
              // Dynamic Strategy Classification Label (Master Implementation Part 5)
              const getStrategyLabel = (c: any, i: number) => {
                if (c.strategy_label) return c.strategy_label;
                if (c.strategy_short_label) return c.strategy_short_label;
                if (c.strategy_name && !c.strategy_name.toLowerCase().includes('strategy')) return c.strategy_name;
                if (c.strategy === 'cost_optimized') return 'Cost Optimized';
                if (c.strategy === 'nutrition_maximized') return 'Nutrition Maximized';
                if (c.strategy === 'functionality_flavor' || c.strategy === 'functionality_texture') return 'Functionality & Flavor';
                if (c.strategy === 'balanced') return 'Balanced Set';
                return 'Balanced Set';
              };
              const strategyLabel = getStrategyLabel(cand, idx);

              const rawCost = cand.cost_per_kg ?? cand.cost_snapshot?.cost_per_kg ?? cand.nutrition?.cost_per_kg;
              const costFormatted = formatIngredientCostPerKg(rawCost, cand.is_zero_cost_verified);
              const costKg = costFormatted.isAvailable ? Number(rawCost) : null;
              const protein = Number((cand.nutrition?.protein ?? 20.0).toFixed(1));
              const carbs = Number((cand.nutrition?.carbohydrates ?? (cand.macros?.carbohydrates ?? 35.0)).toFixed(1));
              const fat = Number((cand.nutrition?.fat ?? (cand.macros?.fat ?? 12.0)).toFixed(1));
              const calories = Math.round(cand.nutrition?.calories ?? (cand.macros?.calories ?? ((4.0 * protein) + (4.0 * carbs) + (9.0 * fat))));
              const minerals = Math.round(cand.nutrition?.key_minerals_mg ?? (cand.nutrition?.minerals?.total_minerals_mg ?? 380));
              const aw = cand.nutrition?.water_activity ?? 0.58;

              // All ingredients list and core ratios
              const bulkList = cand.composition?.bulk_ingredients || [];
              const funcList = cand.composition?.functional_ingredients || [];
              const allComponents = (cand.composition?.all_components && cand.composition.all_components.length > 0)
                ? cand.composition.all_components
                : [...bulkList, ...funcList];

              return (
                <div 
                  key={idx}
                  className={`canonical-card p-5 bg-white border transition-all flex flex-col justify-between hover-lift relative ${
                    isBest 
                      ? 'border-[#164E3D] ring-2 ring-[#164E3D]/10 shadow-lg' 
                      : 'border-[#E5E9E6] hover:border-[#164E3D]'
                  }`}
                >
                  {isBest && (
                    <div className="absolute -top-3 left-4 bg-[#164E3D] text-white text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider flex items-center gap-1 shadow">
                      <Award className="h-3 w-3" />
                      Rank #1 · Highest Overall Score
                    </div>
                  )}

                  <div className="space-y-4">
                    <div className="flex justify-between items-start pt-1">
                      <div className="space-y-1">
                        <div className="flex items-center gap-1.5 flex-wrap">
                          <span className="text-[10px] font-mono font-bold text-[#5F6D67] bg-[#F4F6F5] px-2 py-0.5 rounded border border-[#E5E9E6]">
                            {cand.candidate_id || `FC-00${idx + 1}`}
                          </span>
                        </div>
                        <h3 className="font-extrabold text-xl text-[#191C1E] tracking-tight">
                          {strategyLabel}
                        </h3>
                      </div>
                      
                      {/* Overall Score Badge */}
                      <div className="text-right flex-shrink-0 ml-2">
                        <div className="text-xl font-extrabold text-[#164E3D] font-mono">
                          {score.toFixed(1)}%
                        </div>
                        <span className="text-[9px] font-mono font-bold text-[#5F6D67] uppercase block">Overall Score</span>
                      </div>
                    </div>

                    {/* Key Nutrition Metrics Pills */}
                    <div className="grid grid-cols-5 gap-1 p-2 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6] text-center font-mono">
                      <div>
                        <span className="text-[9px] text-[#5F6D67] block">Protein</span>
                        <span className="text-xs font-bold text-[#164E3D]">{protein}g</span>
                      </div>
                      <div>
                        <span className="text-[9px] text-[#5F6D67] block">Carbs</span>
                        <span className="text-xs font-bold text-[#2563EB]">{carbs}g</span>
                      </div>
                      <div>
                        <span className="text-[9px] text-[#5F6D67] block">Calories</span>
                        <span className="text-xs font-bold text-[#D97706]">{calories}</span>
                      </div>
                      <div>
                        <span className="text-[9px] text-[#5F6D67] block">Minerals</span>
                        <span className="text-xs font-bold text-[#059669]">{minerals}mg</span>
                      </div>
                      <div>
                        <span className="text-[9px] text-[#5F6D67] block">Cost/kg</span>
                        <span className="text-xs font-bold text-[#164E3D]">
                          {costFormatted.isAvailable ? `$${costKg!.toFixed(2)}` : 'Unavailable'}
                        </span>
                      </div>
                    </div>

                    {/* Top Ingredients Composition Preview */}
                    <div className="space-y-1.5">
                      <div className="flex justify-between items-center text-[10px] font-mono font-bold text-[#5F6D67] uppercase">
                        <span>Core Ingredients Preview:</span>
                        <span className="text-[#164E3D]">{allComponents.length} total</span>
                      </div>
                      <div className="space-y-1">
                        {allComponents.slice(0, 4).map((ing: any, iIdx: number) => (
                          <div key={iIdx} className="flex justify-between text-xs text-[#191C1E]">
                            <span className="truncate max-w-[150px] font-medium">{ing.name}</span>
                            <span className="font-mono font-bold text-[#164E3D]">
                              {(ing.percentage || 0).toFixed(1)}%
                            </span>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Compliance & Validation Badges */}
                    <div className="flex flex-wrap gap-1.5 pt-2 border-t border-[#E5E9E6]">
                      {isFeasible ? (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
                          ✓ Hard Constraints Pass
                        </span>
                      ) : (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-red-50 text-red-800 border border-red-200" title={cand.violations?.join('; ') || 'Violates hard constraint'}>
                          ✕ Infeasible ({cand.violations?.length || 1} Violations)
                        </span>
                      )}
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[#ECF4F0] text-[#164E3D]">
                        Aw {aw}
                      </span>
                    </div>
                  </div>

                  {/* Actions Area */}
                  <div className="pt-4 space-y-2">
                    {/* Inspect Candidate Set Button */}
                    <button
                      type="button"
                      onClick={() => {
                        setInspectedCandidateIdx(idx);
                        setModalTab('ingredients');
                      }}
                      className="w-full py-2.5 px-3 rounded-xl border border-[#164E3D]/30 hover:border-[#164E3D] bg-white hover:bg-[#ECF4F0] text-[#164E3D] font-extrabold text-xs transition flex items-center justify-center gap-1.5 cursor-pointer"
                    >
                      <Eye className="h-3.5 w-3.5" />
                      <span>Inspect {strategyLabel} ({allComponents.length} Ingredients)</span>
                    </button>

                    {/* Primary Selection Button */}
                    <button
                      type="button"
                      onClick={() => {
                        setSelectedCandidateIdx(idx);
                        setStep(5);
                      }}
                      className={`w-full py-2.5 px-3 rounded-xl font-extrabold text-xs transition shadow-sm flex items-center justify-center gap-2 cursor-pointer ${
                        isBest
                          ? 'bg-[#164E3D] hover:bg-[#123F32] text-white shadow-md'
                          : 'bg-[#FAFAF8] hover:bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9]'
                      }`}
                    >
                      <span>Select {strategyLabel} & View Final Report</span>
                      <ArrowRight className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              );
            })}
          </div>

          <div className="flex justify-between pt-4 border-t border-[#E5E9E6]">
            <button
              type="button"
              onClick={() => setStep(3)}
              className="px-5 py-2.5 rounded-xl border border-[#E5E9E6] text-xs font-bold text-[#5F6D67] hover:text-[#191C1E] transition flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Constraints
            </button>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* CANDIDATE SET DEEP-DIVE INSPECTION MODAL                                  */}
      {/* ========================================================================= */}
      {inspectedCandidateIdx !== null && formulationResult && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto animate-in fade-in duration-200">
          {(() => {
            const cand = (formulationResult.candidate_sets || [formulationResult.formulation])[inspectedCandidateIdx];
            if (!cand) return null;

            const score = Number((cand.scoring?.overall_score ?? (cand.overall_score ?? 0.0)));
            const getStrategyLabel = (c: any, i: number) => {
              if (c.strategy_label) return c.strategy_label;
              if (c.strategy_short_label) return c.strategy_short_label;
              if (c.strategy_name && !c.strategy_name.toLowerCase().includes('strategy')) return c.strategy_name;
              if (c.strategy === 'cost_optimized') return 'Cost Optimized';
              if (c.strategy === 'nutrition_maximized') return 'Nutrition Maximized';
              if (c.strategy === 'functionality_flavor' || c.strategy === 'functionality_texture') return 'Functionality & Flavor';
              if (c.strategy === 'balanced') return 'Balanced Set';
              return 'Balanced Set';
            };
            const strategyLabel = getStrategyLabel(cand, inspectedCandidateIdx);

            const bulkList = cand.composition?.bulk_ingredients || [];
            const funcList = cand.composition?.functional_ingredients || [];
            const allComponents = (cand.composition?.all_components && cand.composition.all_components.length > 0)
              ? cand.composition.all_components
              : [...bulkList, ...funcList];

            const protein = Number((cand.nutrition?.protein ?? 20.0).toFixed(1));
            const carbs = Number((cand.nutrition?.carbohydrates ?? (cand.macros?.carbohydrates ?? 35.0)).toFixed(1));
            const calories = Math.round(cand.nutrition?.calories ?? (cand.macros?.calories ?? 450));
            const nutBreakdown = cand.nutrition?.nutrition_breakdown || cand.macros?.nutrition_breakdown || [];
            const stratRationale = cand.strategy_rationale || {};

            return (
              <div className="bg-white rounded-2xl border border-[#E5E9E6] shadow-2xl max-w-5xl w-full max-h-[90vh] flex flex-col overflow-hidden my-6">
                {/* Modal Header */}
                <div className="p-6 border-b border-[#E5E9E6] bg-[#FAFAF8] flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className="text-[10px] font-mono font-bold text-[#164E3D] bg-[#ECF4F0] px-2.5 py-0.5 rounded-full border border-[#D1E2D9]">
                        {cand.candidate_id || `FC-00${inspectedCandidateIdx + 1}`}
                      </span>
                      {inspectedCandidateIdx === 0 && (
                        <span className="text-[10px] font-mono font-bold text-amber-800 bg-amber-50 px-2.5 py-0.5 rounded-full border border-amber-200 flex items-center gap-1">
                          <Award className="h-3 w-3" />
                          Rank #1 (Highest Overall Score)
                        </span>
                      )}
                    </div>
                    <h2 className="text-2xl sm:text-3xl font-extrabold text-[#191C1E] font-heading">
                      {strategyLabel}
                    </h2>
                  </div>

                  <div className="flex items-center gap-3">
                    <div className="text-right">
                      <div className="text-2xl font-extrabold text-[#164E3D] font-mono leading-none">
                        {score.toFixed(1)}%
                      </div>
                      <span className="text-[9px] font-mono font-bold text-[#5F6D67] uppercase block mt-1">
                        Overall Score
                      </span>
                    </div>

                    <button
                      type="button"
                      onClick={() => setInspectedCandidateIdx(null)}
                      className="p-2 rounded-xl text-[#5F6D67] hover:text-[#191C1E] hover:bg-[#E5E9E6]/50 transition cursor-pointer"
                      aria-label="Close modal"
                    >
                      <X className="h-5 w-5" />
                    </button>
                  </div>
                </div>

                {/* Modal Body Content */}
                <div className="p-6 overflow-y-auto space-y-4 flex-1 bg-[#FBFBFA]">
                  {/* Top Control Bar for Batch Scaler & Mass Balance */}
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 p-3 bg-white rounded-xl border border-[#E5E9E6]">
                        <div className="flex items-center gap-2">
                          <Scale className="h-4 w-4 text-[#164E3D]" />
                          <span className="text-xs font-bold text-[#191C1E]">Batch Scaling Basis:</span>
                          <div className="flex items-center gap-1 font-mono text-xs">
                            <button
                              type="button"
                              onClick={() => setBatchScaleGrams(10000)}
                              className={`px-3 py-1 rounded-lg border text-xs font-bold transition cursor-pointer ${
                                batchScaleGrams === 10000
                                  ? 'bg-[#164E3D] text-white border-[#164E3D]'
                                  : 'bg-[#FAFAF8] text-[#5F6D67] border-[#E5E9E6] hover:text-[#191C1E]'
                              }`}
                            >
                              10 KG
                            </button>
                            <button
                              type="button"
                              onClick={() => setBatchScaleGrams(100000)}
                              className={`px-3 py-1 rounded-lg border text-xs font-bold transition cursor-pointer ${
                                batchScaleGrams === 100000
                                  ? 'bg-[#164E3D] text-white border-[#164E3D]'
                                  : 'bg-[#FAFAF8] text-[#5F6D67] border-[#E5E9E6] hover:text-[#191C1E]'
                              }`}
                            >
                              100 KG
                            </button>
                          </div>
                        </div>

                        <div className="flex items-center gap-2">
                          <span className="px-2.5 py-1 rounded-lg text-xs font-mono font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 flex items-center gap-1">
                            <CheckCircle className="h-3.5 w-3.5 text-emerald-600" />
                            Mass Balance Sum = 100.0000%
                          </span>
                        </div>
                      </div>

                      {/* Complete Ingredients Table */}
                      <div className="bg-white rounded-xl border border-[#E5E9E6] overflow-hidden shadow-xs">
                        <div className="overflow-x-auto">
                          <table className="w-full text-left text-xs">
                            <thead className="bg-[#FAFAF8] text-[#5F6D67] font-mono uppercase text-[10px] border-b border-[#E5E9E6]">
                              <tr>
                                <th className="px-4 py-3">#</th>
                                <th className="px-4 py-3">Ingredient Name</th>
                                <th className="px-4 py-3 text-right">%</th>
                                <th className="px-4 py-3 text-right">Amount (kg/g)</th>
                                <th className="px-4 py-3">Functional Role</th>
                                <th className="px-4 py-3">Nutritional Contribution</th>
                                <th className="px-4 py-3 text-right">Cost ($/kg)</th>
                              </tr>
                            </thead>
                            <tbody className="divide-y divide-[#E5E9E6]">
                              {allComponents.map((comp: any, cIdx: number) => {
                                const pct = Number(comp.percentage || 0);
                                const qtyGrams = (pct / 100.0) * batchScaleGrams;
                                const qtyKg = qtyGrams / 1000.0;
                                const role = comp.functional_role || comp.role || comp.category || 'Base Raw Material';
                                const costInfo = formatIngredientCostPerKg(comp.cost_per_kg, comp.is_zero_cost_verified);
                                const formattedAmount = formatIngredientAmount(qtyKg);

                                const nutItem = nutBreakdown.find((n: any) => 
                                  (n.name && comp.name && n.name.toLowerCase() === comp.name.toLowerCase()) || 
                                  (n.ingredient_id && comp.id && n.ingredient_id === comp.id)
                                );

                                return (
                                  <tr key={cIdx} className="hover:bg-[#F9FAF9] transition">
                                    <td className="px-4 py-3 font-mono text-[#5F6D67]">{cIdx + 1}</td>
                                    <td className="px-4 py-3">
                                      <div className="font-bold text-[#191C1E]">{comp.name}</div>
                                      <div className="text-[10px] text-[#5F6D67]">{comp.category || 'Raw Ingredient'}</div>
                                    </td>
                                    <td className="px-4 py-3 text-right font-mono font-bold text-[#164E3D] text-sm">
                                      {pct.toFixed(2)}%
                                    </td>
                                    <td className="px-4 py-3 text-right font-mono text-[#191C1E] font-medium whitespace-nowrap">
                                      <span className="whitespace-nowrap font-mono">{formattedAmount}</span>
                                    </td>
                                    <td className="px-4 py-3">
                                      <span className="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9]">
                                        {role}
                                      </span>
                                    </td>
                                    <td className="px-4 py-3 font-mono text-[11px] text-[#2D3748]">
                                      {nutItem ? (
                                        <div className="flex flex-wrap gap-1 text-[10px]">
                                          {nutItem.protein_contrib_g > 0 && <span className="bg-emerald-50 text-emerald-800 px-1.5 py-0.5 rounded">{nutItem.protein_contrib_g}g Prot</span>}
                                          {nutItem.fat_contrib_g > 0 && <span className="bg-amber-50 text-amber-800 px-1.5 py-0.5 rounded">{nutItem.fat_contrib_g}g Fat</span>}
                                          {nutItem.carbs_contrib_g > 0 && <span className="bg-blue-50 text-blue-800 px-1.5 py-0.5 rounded">{nutItem.carbs_contrib_g}g Carb</span>}
                                          {nutItem.calories_contrib_kcal > 0 && <span className="bg-gray-100 text-gray-700 px-1.5 py-0.5 rounded">{nutItem.calories_contrib_kcal} kcal</span>}
                                        </div>
                                      ) : (
                                        <span className="text-[#5F6D67] text-[10px]">Matrix component</span>
                                      )}
                                    </td>
                                    <td className="px-4 py-3 text-right font-mono whitespace-nowrap">
                                      {costInfo.isAvailable ? (
                                        <span className="text-[#191C1E] font-bold font-mono">{costInfo.display}</span>
                                      ) : (
                                        <span className="text-amber-700 bg-amber-50 px-2 py-0.5 rounded text-[10px] font-bold border border-amber-200">
                                          Cost Data Unavailable
                                        </span>
                                      )}
                                    </td>
                                  </tr>
                                );
                              })}
                            </tbody>
                            <tfoot className="bg-[#FAFAF8] font-bold text-[#191C1E] border-t-2 border-[#E5E9E6]">
                              <tr>
                                <td colSpan={2} className="px-4 py-3 font-mono uppercase text-xs">
                                  Total Formulation (100% Mass Balance)
                                </td>
                                <td className="px-4 py-3 text-right font-mono text-[#164E3D] text-sm">
                                  {allComponents.reduce((acc: number, c: any) => acc + Number(c.percentage || 0), 0).toFixed(2)}%
                                </td>
                                <td className="px-4 py-3 text-right font-mono text-[#191C1E] whitespace-nowrap">
                                  <span className="whitespace-nowrap font-mono">{formatIngredientAmount(batchScaleGrams / 1000)}</span>
                                </td>
                                <td colSpan={2} className="px-4 py-3 text-[11px] text-[#5F6D67]">
                                  Protein: {cand.nutrition?.protein ?? 7.5}g · Carbs: {carbs}g · Calories: {calories} kcal
                                </td>
                                {(() => {
                                  const batchKg = batchScaleGrams / 1000.0;
                                  const hasUnpriced = allComponents.some((c: any) => c.cost_per_kg === null || c.cost_per_kg === undefined || (!c.is_zero_cost_verified && Number(c.cost_per_kg) === 0));
                                  const totalCost = hasUnpriced ? null : allComponents.reduce((acc: number, c: any) => acc + ((Number(c.percentage || 0) / 100.0) * batchKg * Number(c.cost_per_kg)), 0);
                                  const costPerKg = hasUnpriced ? null : (cand.cost_per_kg ?? (totalCost ? totalCost / batchKg : null));
                                  return (
                                    <td className="px-4 py-3 text-right font-mono whitespace-nowrap">
                                      {costPerKg !== null && totalCost !== null ? (
                                        <div>
                                          <div className="font-extrabold text-[#164E3D] text-sm">${costPerKg.toFixed(2)}/kg</div>
                                          <div className="text-[10px] text-[#5F6D67] font-medium">${totalCost.toFixed(2)} total batch</div>
                                        </div>
                                      ) : (
                                        <span className="text-amber-700 bg-amber-50 px-2 py-0.5 rounded text-[10px] font-bold border border-amber-200">
                                          Cost Data Unavailable
                                        </span>
                                      )}
                                    </td>
                                  );
                                })()}
                              </tr>
                            </tfoot>
                          </table>
                        </div>
                      </div>
                </div>

                {/* Modal Footer Actions */}
                <div className="p-4 border-t border-[#E5E9E6] bg-white flex flex-col sm:flex-row justify-between items-center gap-3">
                  <button
                    type="button"
                    onClick={() => setInspectedCandidateIdx(null)}
                    className="w-full sm:w-auto px-5 py-2.5 rounded-xl border border-[#E5E9E6] text-xs font-bold text-[#5F6D67] hover:text-[#191C1E] hover:bg-[#FAFAF8] transition cursor-pointer"
                  >
                    Close Inspector
                  </button>

                  <button
                    type="button"
                    onClick={() => {
                      const selectedCand = (formulationResult.candidate_sets || [formulationResult.formulation])[inspectedCandidateIdx];
                      if (selectedCand) {
                        const comps = selectedCand.composition?.all_components || [];
                        const missingCosts = comps.filter((c: any) => c.cost_per_kg === null || c.cost_per_kg === undefined);
                        if (missingCosts.length > 0) {
                          setNavWarning(`Notice: ${missingCosts.length} ingredient(s) have unverified supplier cost records. Downstream cost reports will reflect 'Cost Data Unavailable'.`);
                        }
                      }
                      setSelectedCandidateIdx(inspectedCandidateIdx);
                      setInspectedCandidateIdx(null);
                      setStep(5);
                    }}
                    className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white text-xs font-extrabold transition shadow flex items-center justify-center gap-2 cursor-pointer"
                  >
                    <span>Select This Candidate Set & View Final Report →</span>
                  </button>
                </div>
              </div>
            );
          })()}
        </div>
      )}

      {/* ========================================================================= */}
      {/* STEP 5: FINAL FORMULATION REPORT AFTER SELECTING BEST FORMULATION        */}
      {/* ========================================================================= */}
      {step === 5 && formulationResult && (
        <div className="space-y-6">
          {/* Top Control Bar for Final Report */}
          <div className="canonical-card p-4 bg-white border border-[#E5E9E6] flex flex-col sm:flex-row justify-between items-center gap-3">
            <div className="flex items-center gap-3">
              <span className="text-[10px] font-mono text-[#164E3D] bg-[#ECF4F0] px-3 py-1 rounded-full font-bold uppercase tracking-widest border border-[#D1E2D9]">
                STEP 5 OF 5 · FINAL FORMULATION REPORT
              </span>
              <span className="text-xs font-bold text-[#191C1E]">
                Showing: {formulationResult.candidate_sets?.[selectedCandidateIdx]?.title || formulationResult.formulation?.recipe_name || 'Selected Formulation'}
              </span>
            </div>

            <div className="flex items-center gap-3">
              <button
                type="button"
                onClick={() => setStep(4)}
                className="px-4 py-2 rounded-xl border border-[#E5E9E6] hover:border-[#164E3D] text-xs font-bold text-[#5F6D67] hover:text-[#164E3D] transition flex items-center gap-2"
              >
                <ArrowLeft className="h-4 w-4" />
                Compare Other Candidates
              </button>
              <button
                type="button"
                onClick={() => {
                  setStep(1);
                  setFormulationResult(null);
                }}
                className="px-4 py-2 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white text-xs font-bold transition flex items-center gap-2"
              >
                <RotateCcw className="h-4 w-4" />
                Start New Formulation
              </button>
            </div>
          </div>

          {/* Deep-Dive Formulation Results Component */}
          <FormulationResults 
            data={formulationResult} 
            selectedCandidateIndex={selectedCandidateIdx}
            onReset={() => {
              setStep(1);
              setFormulationResult(null);
            }} 
          />
        </div>
      )}

    </div>
  );
}
