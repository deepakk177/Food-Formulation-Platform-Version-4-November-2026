'use client';

import React, { useState, useEffect } from 'react';
import { 
  CheckCircle, Loader2, Sparkles, Database, ShieldCheck, 
  Workflow, Cpu, Award, Layers
} from 'lucide-react';

interface Stage {
  id: string;
  name: string;
  desc: string;
  icon: any;
}

const STAGES: Stage[] = [
  { id: '1', name: 'Product Brief Parsing', desc: 'Extracting structured dietary targets & constraints', icon: Sparkles },
  { id: '2', name: 'Knowledge Graph Retrieval', desc: 'Querying SQLite & Neo4j food science relationships', icon: Database },
  { id: '3', name: 'Ingredient Candidate Retrieval', desc: 'Filtering verified macro & micro ingredient profiles', icon: Layers },
  { id: '4', name: 'Constraint Veto Evaluation', desc: 'Enforcing non-GMO, vegan & allergen safety guards', icon: ShieldCheck },
  { id: '5', name: 'Compatibility Analysis', desc: 'Analyzing emulsion, moisture & matrix synergy', icon: Workflow },
  { id: '6', name: 'Formulation Optimization', desc: 'Solving linear exact formula balance (Sum = 100.0%)', icon: Cpu },
  { id: '7', name: 'Candidate Scoring & Compliance', desc: 'Computing multi-objective radar feasibility & EFSA/FDA rules', icon: Award }
];

interface AIProcessingStateProps {
  onComplete?: () => void;
}

export default function AIProcessingState({ onComplete }: AIProcessingStateProps) {
  const [currentIdx, setCurrentIdx] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentIdx((prev) => {
        if (prev < STAGES.length - 1) {
          return prev + 1;
        } else {
          clearInterval(timer);
          if (onComplete) onComplete();
          return prev;
        }
      });
    }, 550);

    return () => clearInterval(timer);
  }, [onComplete]);

  return (
    <div className="canonical-card p-6 border border-[#D1E2D9] space-y-6 shadow-md bg-white">
      {/* Processing Banner Header */}
      <div className="flex justify-between items-center border-b border-[#E5E9E6] pb-4">
        <div className="flex items-center gap-3">
          <div className="h-9 w-9 rounded-xl bg-[#ECF4F0] border border-[#D1E2D9] text-[#164E3D] flex items-center justify-center">
            <Cpu className="h-5 w-5 animate-pulse" />
          </div>
          <div>
            <span className="text-[10px] font-mono font-bold text-[#164E3D] uppercase tracking-wider block">
              A.I. FORMULATION PROCESSING ENGINE
            </span>
            <h3 className="text-sm font-bold text-[#191C1E]">
              Executing Scientific Knowledge-Graph Pipeline
            </h3>
          </div>
        </div>
        <span className="text-xs font-mono font-bold text-[#164E3D] bg-[#ECF4F0] px-3 py-1 rounded-full border border-[#D1E2D9]">
          Step {currentIdx + 1} of {STAGES.length}
        </span>
      </div>

      {/* Sequential Stages Flow */}
      <div className="space-y-3 font-sans">
        {STAGES.map((stage, idx) => {
          const isCompleted = idx < currentIdx;
          const isActive = idx === currentIdx;
          const isPending = idx > currentIdx;
          const Icon = stage.icon;

          return (
            <div 
              key={stage.id}
              className={`p-3.5 rounded-xl border transition-all duration-300 flex items-center justify-between ${
                isActive 
                  ? 'border-[#164E3D] bg-[#ECF4F0]/60 shadow-sm' 
                  : isCompleted 
                  ? 'border-[#E5E9E6] bg-white text-[#5F6D67]' 
                  : 'border-[#F1F5F3] bg-[#FAFAF8] opacity-60'
              }`}
            >
              <div className="flex items-center gap-3">
                <div className={`h-8 w-8 rounded-lg flex items-center justify-center text-xs font-bold font-mono transition ${
                  isCompleted ? 'bg-[#164E3D] text-white' :
                  isActive ? 'bg-[#164E3D] text-white animate-pulse' :
                  'bg-[#E5E9E6] text-[#5F6D67]'
                }`}>
                  {isCompleted ? <CheckCircle className="h-4 w-4" /> : <Icon className="h-4 w-4" />}
                </div>

                <div>
                  <h4 className={`text-xs font-bold ${isActive ? 'text-[#164E3D]' : isCompleted ? 'text-[#191C1E]' : 'text-[#5F6D67]'}`}>
                    {stage.name}
                  </h4>
                  <p className="text-[11px] text-[#5F6D67] font-mono">
                    {stage.desc}
                  </p>
                </div>
              </div>

              <div>
                {isActive && (
                  <div className="flex items-center gap-2 text-xs font-bold text-[#164E3D] font-mono">
                    <Loader2 className="h-4 w-4 animate-spin" />
                    <span>Processing...</span>
                  </div>
                )}
                {isCompleted && (
                  <span className="text-[10px] font-mono font-bold text-[#164E3D] bg-[#ECF4F0] px-2 py-0.5 rounded border border-[#D1E2D9]">
                    PASSED
                  </span>
                )}
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
}
