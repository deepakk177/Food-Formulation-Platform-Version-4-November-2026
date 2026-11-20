'use client';

import React from 'react';
import {
  Sparkles, FileText, CheckCircle, Copy, Scale, Layers, Clock, ShieldCheck
} from 'lucide-react';

export interface ActivityItem {
  id: string;
  type: 'formulate' | 'export' | 'compliance' | 'duplicate' | 'compare';
  title: string;
  detail: string;
  timestamp: string;
}

interface RecentActivityProps {
  activities?: ActivityItem[];
}

export default function RecentActivity({ activities }: RecentActivityProps) {
  const items = activities && activities.length > 0 ? activities : [];

  const getIcon = (type: string) => {
    switch (type) {
      case 'formulate': return <Sparkles className="h-4 w-4 text-[#164E3D]" />;
      case 'compliance': return <ShieldCheck className="h-4 w-4 text-emerald-600" />;
      case 'export': return <FileText className="h-4 w-4 text-[#2563EB]" />;
      case 'duplicate': return <Copy className="h-4 w-4 text-amber-600" />;
      case 'compare': return <Scale className="h-4 w-4 text-[#7C3AED]" />;
      default: return <Clock className="h-4 w-4 text-[#5F6D67]" />;
    }
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E5E9E6] p-5 space-y-4 shadow-sm font-sans">
      <div className="flex justify-between items-center border-b border-[#E5E9E6] pb-3">
        <h3 className="text-base font-extrabold text-[#191C1E] font-heading flex items-center gap-2">
          <Clock className="h-4 w-4 text-[#164E3D]" /> Recent Activity Log
        </h3>
        <span className="text-[10px] font-mono font-bold text-[#5F6D67] uppercase bg-[#FAFAF8] px-2 py-0.5 rounded border border-[#E5E9E6]">
          Last 7 Days
        </span>
      </div>

      <div className="space-y-3 font-mono text-xs">
        {items.length === 0 ? (
          <div className="py-8 text-center text-[#5F6D67] font-sans text-xs font-bold">
            No recent activity recorded.
          </div>
        ) : (
          items.map((act) => (
            <div key={act.id} className="flex items-start gap-3 p-3 rounded-xl border border-[#E5E9E6] bg-[#FAFAF8] hover:border-[#164E3D] transition">
              <div className="p-2 rounded-xl bg-white border border-[#E5E9E6] shrink-0 shadow-2xs">
                {getIcon(act.type)}
              </div>
              <div className="space-y-0.5 flex-1">
                <div className="flex justify-between items-center">
                  <span className="font-sans font-extrabold text-[#191C1E] text-xs">{act.title}</span>
                  <span className="text-[10px] text-[#5F6D67] font-bold">{act.timestamp}</span>
                </div>
                <p className="text-[11px] text-[#5F6D67] font-sans font-bold leading-relaxed">{act.detail}</p>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
