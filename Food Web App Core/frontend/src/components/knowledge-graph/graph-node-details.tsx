'use client';

import React from 'react';
import { GraphNode, GraphEdge } from '@/types/graph';
import { X, Network, Database, Layers, ArrowRight, ShieldCheck, Cpu, Award } from 'lucide-react';
import { NODE_COLORS } from './graph-canvas';

interface GraphNodeDetailsProps {
  selectedNode: GraphNode | null;
  selectedEdge: GraphEdge | null;
  onClose: () => void;
  onExpandNode?: (nodeId: string) => void;
}

export default function GraphNodeDetails({
  selectedNode,
  selectedEdge,
  onClose,
  onExpandNode,
}: GraphNodeDetailsProps) {
  if (!selectedNode && !selectedEdge) return null;

  const isNode = Boolean(selectedNode);
  const title = isNode ? selectedNode?.label : selectedEdge?.type;
  const typeLabel = isNode ? selectedNode?.type : 'Relationship';
  const propsDict = isNode ? selectedNode?.properties || {} : selectedEdge?.properties || {};
  const color = isNode && selectedNode ? NODE_COLORS[selectedNode.type] || NODE_COLORS.Ingredient : { bg: '#164E3D', border: '#D1E2D9', text: '#FFF' };

  return (
    <div className="w-full lg:w-96 bg-white rounded-2xl border border-[#E5E9E6] p-5 space-y-5 shadow-lg font-sans text-[#191C1E] relative shrink-0">
      
      {/* Header Title & Close Button */}
      <div className="flex justify-between items-start border-b border-[#E5E9E6] pb-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <span
              className="px-2.5 py-0.5 rounded-full text-[10px] font-bold font-mono border uppercase tracking-wider"
              style={{ backgroundColor: color.bg, color: color.text, borderColor: color.border }}
            >
              {typeLabel}
            </span>
            <span className="text-[10px] font-mono text-[#5F6D67]">
              ID: {isNode ? selectedNode?.id : selectedEdge?.id}
            </span>
          </div>
          <h3 className="text-lg font-extrabold text-[#191C1E] font-heading leading-snug">
            {title}
          </h3>
        </div>

        <button
          onClick={onClose}
          className="p-1 rounded-lg text-[#5F6D67] hover:text-[#191C1E] hover:bg-[#FAFAF8] transition"
        >
          <X className="h-4 w-4" />
        </button>
      </div>

      {/* Relationship Source/Target Summary */}
      {!isNode && selectedEdge && (
        <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6] space-y-2 text-xs font-mono">
          <div className="flex items-center justify-between">
            <span className="text-[#5F6D67] text-[10px] uppercase font-bold">Source Node:</span>
            <span className="font-extrabold text-[#164E3D]">{selectedEdge.source}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-[#5F6D67] text-[10px] uppercase font-bold">Relationship:</span>
            <span className="font-extrabold text-purple-700">{selectedEdge.type}</span>
          </div>
          <div className="flex items-center justify-between">
            <span className="text-[#5F6D67] text-[10px] uppercase font-bold">Target Node:</span>
            <span className="font-extrabold text-[#164E3D]">{selectedEdge.target}</span>
          </div>
        </div>
      )}

      {/* Node / Relationship Properties Table */}
      <div className="space-y-2">
        <h4 className="text-xs font-bold text-[#5F6D67] uppercase tracking-wider font-mono">
          Attributes & Properties
        </h4>
        <div className="bg-[#FAFAF8] rounded-xl border border-[#E5E9E6] p-3 space-y-1.5 font-mono text-xs max-h-56 overflow-y-auto">
          {Object.keys(propsDict).length > 0 ? (
            Object.entries(propsDict).map(([key, val]) => (
              <div key={key} className="flex justify-between items-center border-b border-[#E5E9E6]/60 pb-1 last:border-none">
                <span className="text-[#5F6D67] text-[11px] font-bold">{key}:</span>
                <span className="text-[#191C1E] font-bold truncate max-w-[180px] text-[11px]">
                  {typeof val === 'object' ? JSON.stringify(val) : String(val)}
                </span>
              </div>
            ))
          ) : (
            <div className="text-[#5F6D67] text-center py-2 text-xs">No extra properties recorded.</div>
          )}
        </div>
      </div>

      {/* Formulation Reasoning Chain (Principle 20) */}
      {isNode && selectedNode?.type === 'Ingredient' && (
        <div className="space-y-2 pt-1 border-t border-[#E5E9E6]">
          <h4 className="text-xs font-bold text-[#164E3D] uppercase tracking-wider font-mono flex items-center gap-1.5">
            <Network className="h-3.5 w-3.5 text-[#164E3D]" /> Formulation Reasoning Chain
          </h4>

          <div className="p-3 bg-[#ECF4F0] rounded-xl border border-[#D1E2D9] space-y-2 font-mono text-[11px] text-[#164E3D]">
            <div className="flex items-center gap-2">
              <span className="font-extrabold">1. Ingredient:</span>
              <span className="bg-white px-2 py-0.5 rounded border border-[#D1E2D9] font-bold text-[#191C1E]">
                {selectedNode.label}
              </span>
            </div>
            <div className="flex items-center justify-center text-[#5F6D67]"><ArrowRight className="h-3.5 w-3.5 rotate-90" /></div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold">2. Key Property:</span>
              <span className="bg-white px-2 py-0.5 rounded border border-[#D1E2D9] font-bold text-blue-700">
                Protein {propsDict.protein_g || 35.5}g/100g
              </span>
            </div>
            <div className="flex items-center justify-center text-[#5F6D67]"><ArrowRight className="h-3.5 w-3.5 rotate-90" /></div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold">3. Functional Role:</span>
              <span className="bg-white px-2 py-0.5 rounded border border-[#D1E2D9] font-bold text-purple-700">
                {propsDict.functional_role || 'Protein Source'}
              </span>
            </div>
            <div className="flex items-center justify-center text-[#5F6D67]"><ArrowRight className="h-3.5 w-3.5 rotate-90" /></div>
            <div className="flex items-center gap-2">
              <span className="font-extrabold">4. Safety Constraint:</span>
              <span className="bg-white px-2 py-0.5 rounded border border-[#D1E2D9] font-bold text-amber-700">
                {propsDict.allergen && propsDict.allergen !== 'None' ? `Allergen: ${propsDict.allergen}` : 'Non-GMO / Clean Label'}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Expand Action Button */}
      {isNode && onExpandNode && selectedNode && (
        <button
          onClick={() => onExpandNode(selectedNode.id)}
          className="w-full py-2.5 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white font-extrabold text-xs transition shadow-sm flex items-center justify-center gap-2 font-sans"
        >
          <Layers className="h-4 w-4" /> Expand Node Connections
        </button>
      )}

    </div>
  );
}
