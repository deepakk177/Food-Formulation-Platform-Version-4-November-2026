'use client';

import React from 'react';
import {
  ZoomIn, ZoomOut, Maximize2, RefreshCw, Layers, Search, SlidersHorizontal
} from 'lucide-react';

interface GraphToolbarProps {
  depth: number;
  onDepthChange: (depth: number) => void;
  onZoomIn?: () => void;
  onZoomOut?: () => void;
  onFit?: () => void;
  onReset?: () => void;
  searchTerm: string;
  onSearchChange: (q: string) => void;
  onSearchSubmit: (e: React.FormEvent) => void;
  layoutName: string;
  onLayoutChange: (layout: string) => void;
}

export default function GraphToolbar({
  depth,
  onDepthChange,
  onZoomIn,
  onZoomOut,
  onFit,
  onReset,
  searchTerm,
  onSearchChange,
  onSearchSubmit,
  layoutName,
  onLayoutChange
}: GraphToolbarProps) {
  return (
    <div className="bg-white p-3 rounded-2xl border border-[#E5E9E6] shadow-sm flex flex-col md:flex-row items-center justify-between gap-3 font-sans text-xs font-bold">
      
      {/* Search Input Box */}
      <form onSubmit={onSearchSubmit} className="relative w-full md:w-72">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-[#5F6D67]" />
        <input
          type="text"
          value={searchTerm}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="Search Knowledge Graph..."
          className="w-full bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl pl-9 pr-4 py-1.5 text-xs text-[#191C1E] placeholder-[#5F6D67] focus:outline-none focus:border-[#164E3D] transition"
        />
      </form>

      {/* Controls: Depth, Layout, Zoom, Fit, Reset */}
      <div className="flex flex-wrap items-center gap-2.5 w-full md:w-auto justify-end">
        
        {/* Depth Selector (1..3) */}
        <div className="flex items-center gap-1.5 bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl px-2.5 py-1">
          <Layers className="h-3.5 w-3.5 text-[#164E3D]" />
          <span className="text-[#5F6D67] text-[11px]">Depth:</span>
          <div className="flex gap-1 font-mono">
            {[1, 2, 3].map((d) => (
              <button
                key={d}
                type="button"
                onClick={() => onDepthChange(d)}
                className={`h-5 w-5 rounded text-[10px] font-extrabold transition ${
                  depth === d
                    ? 'bg-[#164E3D] text-white shadow-2xs'
                    : 'text-[#5F6D67] hover:bg-[#ECF4F0] hover:text-[#164E3D]'
                }`}
              >
                {d}
              </button>
            ))}
          </div>
        </div>

        {/* Layout Selector */}
        <div className="flex items-center gap-1 bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl px-2.5 py-1">
          <SlidersHorizontal className="h-3.5 w-3.5 text-[#5F6D67]" />
          <select
            value={layoutName}
            onChange={(e) => onLayoutChange(e.target.value)}
            className="bg-transparent text-xs font-bold text-[#191C1E] focus:outline-none cursor-pointer"
          >
            <option value="cose">Force-Directed (COSE)</option>
            <option value="concentric">Concentric Circles</option>
          </select>
        </div>

        {/* Zoom & Fit Action Buttons */}
        <div className="flex items-center gap-1">
          {onZoomIn && (
            <button
              onClick={onZoomIn}
              className="p-1.5 rounded-lg border border-[#E5E9E6] bg-[#FAFAF8] hover:bg-[#ECF4F0] hover:text-[#164E3D] transition text-[#5F6D67]"
              title="Zoom In"
            >
              <ZoomIn className="h-4 w-4" />
            </button>
          )}

          {onZoomOut && (
            <button
              onClick={onZoomOut}
              className="p-1.5 rounded-lg border border-[#E5E9E6] bg-[#FAFAF8] hover:bg-[#ECF4F0] hover:text-[#164E3D] transition text-[#5F6D67]"
              title="Zoom Out"
            >
              <ZoomOut className="h-4 w-4" />
            </button>
          )}

          {onFit && (
            <button
              onClick={onFit}
              className="p-1.5 rounded-lg border border-[#E5E9E6] bg-[#FAFAF8] hover:bg-[#ECF4F0] hover:text-[#164E3D] transition text-[#5F6D67]"
              title="Fit to Screen"
            >
              <Maximize2 className="h-4 w-4" />
            </button>
          )}

          {onReset && (
            <button
              onClick={onReset}
              className="p-1.5 rounded-lg border border-[#E5E9E6] bg-[#FAFAF8] hover:bg-[#ECF4F0] hover:text-[#164E3D] transition text-[#5F6D67]"
              title="Reset Graph"
            >
              <RefreshCw className="h-4 w-4" />
            </button>
          )}
        </div>

      </div>

    </div>
  );
}
