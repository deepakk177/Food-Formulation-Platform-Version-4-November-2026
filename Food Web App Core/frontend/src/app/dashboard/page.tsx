'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import {
  Sparkles, ArrowRight, Play, Loader2, Database, Workflow,
  CheckCircle, AlertTriangle, Send
} from 'lucide-react';
import FormulationResults from '@/components/formulation-results';
import AIProcessingState from '@/components/ai-processing-state';

export default function DashboardPage() {
  const [prompt, setPrompt] = useState('Formulate a low-sodium, high-fibre snack targeting EFSA health claims for digestive health.');
  const [loading, setLoading] = useState(false);
  const [formulationResult, setFormulationResult] = useState<any>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const router = useRouter();

  const handleFormulateSubmit = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!prompt.trim() || loading) return;

    setLoading(true);
    setErrorMessage(null);
    setFormulationResult(null);

    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${api_url}/api/formulation/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: prompt.trim() })
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Formulation execution failed.');
      }

      const data = await response.json();
      setFormulationResult(data);
    } catch (err: any) {
      setErrorMessage(err.message || 'Formulation pipeline error.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-[1600px] mx-auto py-8 px-4 sm:px-6 lg:px-8 space-y-8 font-sans">

      {/* Hero Header Section */}
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

      {/* ChatGPT Style Product Brief Input Card (Image 1 Exact Match) */}
      <div className="canonical-card p-5 sm:p-6 shadow-sm space-y-4 bg-white">
        <form onSubmit={handleFormulateSubmit} className="space-y-4">
          <textarea
            rows={4}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Formulate a product requirements brief..."
            className="w-full bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl p-4 text-sm font-bold text-[#191C1E] placeholder-[#5F6D67] focus:outline-none focus:border-[#164E3D] focus:bg-white transition leading-relaxed font-sans"
          />

          <div className="flex flex-col sm:flex-row justify-between items-center gap-3 border-t border-[#E5E9E6] pt-3">
            <span className="text-xs font-mono font-bold text-[#5F6D67] flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-[#164E3D]" />
              AI · Knowledge Graph · Compliance-aware
            </span>

            <button
              type="submit"
              disabled={loading || !prompt.trim()}
              className="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white font-extrabold text-xs transition shadow-sm disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {loading ? <Loader2 className="h-4 w-4 animate-spin" /> : <Send className="h-4 w-4" />}
              Formulate
            </button>
          </div>
        </form>
      </div>

      {/* Action Buttons below Input Box */}
      <div className="flex flex-wrap justify-center items-center gap-4">
        <button
          onClick={() => router.push('/dashboard/formulate/guided')}
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white font-extrabold text-xs transition shadow-md"
        >
          Start Formulating
          <ArrowRight className="h-4 w-4" />
        </button>

        <button
          type="button"
          className="flex items-center gap-2 px-6 py-3 rounded-xl bg-white border border-[#E5E9E6] hover:border-[#164E3D] text-[#191C1E] font-extrabold text-xs transition shadow-sm"
        >
          <Play className="h-4 w-4 text-[#164E3D] fill-[#164E3D]" />
          Watch Platform Demo
        </button>
      </div>

      {/* AI Processing Animation */}
      {loading && (
        <AIProcessingState onComplete={() => { }} />
      )}

      {/* Error View */}
      {errorMessage && (
        <div className="p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs font-bold flex items-start gap-3">
          <AlertTriangle className="h-5 w-5 text-red-600 shrink-0 mt-0.5" />
          <div>
            <span className="font-extrabold block text-sm">Formulation Pipeline Error</span>
            <p className="mt-0.5 leading-relaxed">{errorMessage}</p>
          </div>
        </div>
      )}

      {/* Results View */}
      {formulationResult && !loading && (
        <div className="pt-6">
          <FormulationResults data={formulationResult} onReset={() => setFormulationResult(null)} />
        </div>
      )}

    </div>
  );
}
