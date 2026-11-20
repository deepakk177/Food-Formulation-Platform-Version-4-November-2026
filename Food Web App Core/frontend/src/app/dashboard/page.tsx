'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Sparkles, ArrowRight, Loader2, AlertTriangle, Check
} from 'lucide-react';
import {
  RESEARCH_BENCHMARK_BRIEFS,
  STORAGE_KEY_PRODUCT_BRIEF,
  BenchmarkBrief
} from '@/components/benchmark-briefs';

export default function DashboardPage() {
  const router = useRouter();

  // Initial default brief matches the prompt's suggested default
  const [prompt, setPrompt] = useState<string>(
    'Formulate a low-sodium, high-fibre snack targeting EFSA health claims for digestive health.'
  );
  const [selectedBenchmarkId, setSelectedBenchmarkId] = useState<string | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [isNavigating, setIsNavigating] = useState<boolean>(false);

  // Handle benchmark selection
  const handleSelectBenchmark = (benchmark: BenchmarkBrief) => {
    setPrompt(benchmark.text);
    setSelectedBenchmarkId(benchmark.id);
    setValidationError(null);
  };

  // Handle prompt change (allow user to edit freely)
  const handlePromptChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const val = e.target.value;
    setPrompt(val);
    setValidationError(null);

    // If edited text no longer matches the selected benchmark text, clear the selection highlight
    if (selectedBenchmarkId) {
      const match = RESEARCH_BENCHMARK_BRIEFS.find((b) => b.id === selectedBenchmarkId);
      if (match && match.text.trim() !== val.trim()) {
        setSelectedBenchmarkId(null);
      }
    }
  };

  // Single formulation entry point handler
  const handleStartFormulating = () => {
    if (isNavigating) return;

    const trimmedPrompt = prompt.trim();
    if (!trimmedPrompt) {
      setValidationError('Please enter a product brief or select an example product brief to start formulating.');
      return;
    }

    setValidationError(null);
    setIsNavigating(true);

    try {
      // 1. Save product brief & selected benchmark to sessionStorage
      if (typeof window !== 'undefined') {
        sessionStorage.setItem(STORAGE_KEY_PRODUCT_BRIEF, trimmedPrompt);
        if (selectedBenchmarkId) {
          sessionStorage.setItem('formulation_selected_benchmark_id', selectedBenchmarkId);
        } else {
          sessionStorage.removeItem('formulation_selected_benchmark_id');
        }
      }

      // 2. Build URL query parameters
      const params = new URLSearchParams();
      params.set('brief', trimmedPrompt);
      if (selectedBenchmarkId) {
        params.set('benchmark', selectedBenchmarkId);
      }

      // 3. Navigate to Step 1 (Product Brief) of the existing guided formulation workflow
      router.push(`/dashboard/formulate/guided?${params.toString()}`);
    } catch {
      setIsNavigating(false);
    }
  };

  return (
    <div className="w-full max-w-[1600px] mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8 font-sans">

      {/* 1. Dashboard Heading and Description */}
      <div className="text-center space-y-4 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-[#ECF4F0] border border-[#D1E2D9] text-xs font-bold text-[#164E3D]">
          <Sparkles className="h-4 w-4 text-[#164E3D]" />
          <span>Knowledge Graph powered food intelligence platform</span>
        </div>

        <h1 className="text-4xl sm:text-5xl font-extrabold text-[#191C1E] tracking-tight leading-tight font-heading">
          Accelerating Scientific Food Formulation Through AI
        </h1>

        <p className="text-[#5F6D67] text-sm sm:text-base leading-relaxed font-bold">
          Transform product requirements into explainable, compliance-aware formulations powered by food science intelligence and constraint optimization.
        </p>
      </div>

      {/* 2. Product Brief Input Card (Chatbox / Textarea) */}
      <div className="canonical-card p-5 sm:p-6 shadow-sm space-y-4 bg-white border border-[#E5E9E6] rounded-2xl max-w-4xl mx-auto">
        <div className="space-y-2">
          <label htmlFor="dashboard-brief-input" className="text-xs font-bold text-[#191C1E] flex items-center justify-between">
            <span>Natural Language Product Specification</span>
            <span className="text-[10px] font-mono text-[#5F6D67]">Scientific NLP Engine Active</span>
          </label>

          <textarea
            id="dashboard-brief-input"
            rows={5}
            value={prompt}
            onChange={handlePromptChange}
            placeholder="Formulate a product requirements brief (e.g. Create a high-protein vegan chocolate bar with at least 25% cocoa butter...)"
            className="w-full bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl p-4 text-sm font-medium text-[#191C1E] placeholder-[#5F6D67] focus:outline-none focus:border-[#164E3D] focus:bg-white transition leading-relaxed font-sans shadow-inner resize-y"
          />
        </div>

        <div className="flex flex-col sm:flex-row justify-between items-center gap-2 pt-2 border-t border-[#E5E9E6]">
          <span className="text-xs font-mono font-bold text-[#5F6D67] flex items-center gap-2">
            <span className="h-2.5 w-2.5 rounded-full bg-[#164E3D]" />
            AI · Knowledge Graph · Compliance-aware
          </span>
          <span className="text-[11px] text-[#5F6D67] font-medium">
            5-Stage Guided Scientific Formulation Workflow
          </span>
        </div>
      </div>

      {/* 3. Example Product Briefs Section with Three Cards */}
      <div className="max-w-4xl mx-auto space-y-3.5">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 px-1">
          <div>
            <h3 className="text-sm sm:text-base font-extrabold text-[#191C1E] font-heading">
              Try an Example Product Brief
            </h3>
            <p className="text-xs text-[#5F6D67]">
              Select a research benchmark to populate the brief, or edit it directly above.
            </p>
          </div>
          <span className="text-[10px] font-mono text-[#164E3D] font-bold uppercase tracking-wider hidden sm:inline">
            Interactive Benchmarks
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3.5">
          {RESEARCH_BENCHMARK_BRIEFS.map((benchmark) => {
            const isSelected =
              selectedBenchmarkId === benchmark.id ||
              prompt.trim() === benchmark.text.trim();

            return (
              <button
                key={benchmark.id}
                type="button"
                onClick={() => handleSelectBenchmark(benchmark)}
                className={`p-4 text-left rounded-2xl border transition text-xs space-y-2 group relative flex flex-col justify-between cursor-pointer ${
                  isSelected
                    ? 'border-[#164E3D] bg-[#ECF4F0] ring-2 ring-[#164E3D]/30 shadow-sm'
                    : 'border-[#E5E9E6] bg-white hover:border-[#164E3D]/50 hover:bg-[#ECF4F0]/30 shadow-2xs'
                }`}
              >
                <div className="space-y-1.5">
                  <div className="flex items-center justify-between gap-1">
                    <span
                      className={`text-[9px] font-mono px-2 py-0.5 rounded font-bold ${
                        isSelected
                          ? 'bg-[#164E3D] text-white'
                          : 'bg-[#E5E9E6] text-[#5F6D67]'
                      }`}
                    >
                      {benchmark.category}
                    </span>
                    {isSelected && (
                      <span className="flex items-center text-[10px] font-bold text-[#164E3D]">
                        <Check className="h-3 w-3 mr-0.5" /> Selected
                      </span>
                    )}
                  </div>

                  <h4
                    className={`font-extrabold text-xs line-clamp-1 ${
                      isSelected
                        ? 'text-[#164E3D]'
                        : 'text-[#191C1E] group-hover:text-[#164E3D]'
                    }`}
                  >
                    {benchmark.title}
                  </h4>

                  <p className="text-[11px] text-[#5F6D67] leading-relaxed line-clamp-3">
                    {benchmark.text}
                  </p>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Validation Warning Alert if Brief is Empty */}
      {validationError && (
        <div className="p-3.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs font-bold flex items-center justify-center gap-2 max-w-lg mx-auto shadow-sm">
          <AlertTriangle className="h-4 w-4 text-amber-600 shrink-0" />
          <span>{validationError}</span>
        </div>
      )}

      {/* 4. Single Primary Action: Start Formulating -> */}
      <div className="flex justify-center items-center pt-2">
        <button
          type="button"
          onClick={handleStartFormulating}
          disabled={isNavigating}
          className="flex items-center gap-2.5 px-8 py-3.5 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white font-extrabold text-sm transition shadow-md disabled:opacity-60 cursor-pointer"
        >
          {isNavigating ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              <span>Launching Formulation Workflow...</span>
            </>
          ) : (
            <>
              <span>Start Formulating</span>
              <ArrowRight className="h-4 w-4" />
            </>
          )}
        </button>
      </div>

    </div>
  );
}
