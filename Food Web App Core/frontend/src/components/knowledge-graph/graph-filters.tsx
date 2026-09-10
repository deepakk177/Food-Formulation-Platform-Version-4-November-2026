'use client';

import React from 'react';

interface GraphFiltersProps {
  selectedFilter: string;
  onFilterChange: (filter: string) => void;
}

export const NODE_TYPES = [
  'All',
  'Ingredient',
  'Property',
  'Function',
  'Constraint',
  'Process',
  'Nutrient',
  'Allergen',
  'Claim',
];

export default function GraphFilters({ selectedFilter, onFilterChange }: GraphFiltersProps) {
  return (
    <div className="flex flex-wrap items-center gap-1.5 font-sans text-xs font-bold">
      <span className="text-[11px] text-[#5F6D67] font-mono mr-1">Filter Nodes:</span>
      {NODE_TYPES.map((type) => {
        const isActive = selectedFilter === type;
        return (
          <button
            key={type}
            onClick={() => onFilterChange(type)}
            className={`px-3 py-1 rounded-full border transition text-xs ${
              isActive
                ? 'bg-[#164E3D] text-white border-[#164E3D] shadow-2xs font-extrabold'
                : 'bg-white text-[#5F6D67] border-[#E5E9E6] hover:border-[#164E3D] hover:text-[#191C1E]'
            }`}
          >
            {type}
          </button>
        );
      })}
    </div>
  );
}
