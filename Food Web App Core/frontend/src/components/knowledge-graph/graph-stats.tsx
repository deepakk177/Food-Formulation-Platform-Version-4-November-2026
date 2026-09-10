'use client';

import React from 'react';
import { GraphStats as StatsType } from '@/types/graph';
import { Network, Sliders, ShieldCheck, Cpu, Award, FileText, Zap } from 'lucide-react';

interface GraphStatsProps {
  stats: StatsType;
}

export default function GraphStats({ stats }: GraphStatsProps) {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 md:grid-cols-7 gap-2.5 font-mono text-center text-xs">
      <div className="p-2.5 bg-white rounded-xl border border-[#E5E9E6] shadow-2xs">
        <span className="text-[9px] text-[#5F6D67] font-bold uppercase tracking-wider block">CONNECTED NODES</span>
        <span className="text-base font-extrabold text-[#164E3D]">{stats.totalNodes || 0}</span>
      </div>

      <div className="p-2.5 bg-white rounded-xl border border-[#E5E9E6] shadow-2xs">
        <span className="text-[9px] text-blue-600 font-bold uppercase tracking-wider block">PROPERTIES</span>
        <span className="text-base font-extrabold text-blue-700">{stats.properties || 0}</span>
      </div>

      <div className="p-2.5 bg-white rounded-xl border border-[#E5E9E6] shadow-2xs">
        <span className="text-[9px] text-purple-600 font-bold uppercase tracking-wider block">FUNCTIONS</span>
        <span className="text-base font-extrabold text-purple-700">{stats.functions || 0}</span>
      </div>

      <div className="p-2.5 bg-white rounded-xl border border-[#E5E9E6] shadow-2xs">
        <span className="text-[9px] text-amber-600 font-bold uppercase tracking-wider block">CONSTRAINTS</span>
        <span className="text-base font-extrabold text-amber-700">{stats.constraints || 0}</span>
      </div>

      <div className="p-2.5 bg-white rounded-xl border border-[#E5E9E6] shadow-2xs">
        <span className="text-[9px] text-slate-600 font-bold uppercase tracking-wider block">PROCESSES</span>
        <span className="text-base font-extrabold text-slate-700">{stats.processes || 0}</span>
      </div>

      <div className="p-2.5 bg-white rounded-xl border border-[#E5E9E6] shadow-2xs">
        <span className="text-[9px] text-teal-600 font-bold uppercase tracking-wider block">NUTRIENTS</span>
        <span className="text-base font-extrabold text-teal-700">{stats.nutrients || 0}</span>
      </div>

      <div className="p-2.5 bg-white rounded-xl border border-[#E5E9E6] shadow-2xs">
        <span className="text-[9px] text-red-600 font-bold uppercase tracking-wider block">ALLERGENS</span>
        <span className="text-base font-extrabold text-red-700">{stats.allergens || 0}</span>
      </div>
    </div>
  );
}
