'use client';

import React from 'react';

export default function GraphLegend() {
  const legendItems = [
    { label: 'Ingredient', bg: '#164E3D', border: '#D1E2D9' },
    { label: 'Property', bg: '#2563EB', border: '#93C5FD' },
    { label: 'Function', bg: '#7C3AED', border: '#C4B5FD' },
    { label: 'Constraint', bg: '#D97706', border: '#FDE68A' },
    { label: 'Process', bg: '#475569', border: '#CBD5E1' },
    { label: 'Nutrient', bg: '#0D9488', border: '#99F6E4' },
    { label: 'Allergen', bg: '#DC2626', border: '#FCA5A5' },
    { label: 'Claim', bg: '#EAB308', border: '#FEF08A' },
  ];

  return (
    <div className="bg-white p-3 rounded-2xl border border-[#E5E9E6] shadow-2xs font-sans text-xs font-bold space-y-2">
      <div className="text-[10px] font-mono text-[#5F6D67] uppercase tracking-wider font-extrabold">
        Knowledge Graph Node Schema Legend
      </div>
      <div className="flex flex-wrap items-center gap-3">
        {legendItems.map((item) => (
          <div key={item.label} className="flex items-center gap-1.5 text-xs text-[#191C1E]">
            <span
              className="h-3.5 w-3.5 rounded-full border shadow-2xs shrink-0"
              style={{ backgroundColor: item.bg, borderColor: item.border }}
            />
            <span>{item.label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
