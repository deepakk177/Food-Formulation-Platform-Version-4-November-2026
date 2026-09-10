'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import {
  FolderGit2, MoreVertical, ExternalLink, Copy, Archive, Trash2, Edit3,
  CheckCircle, Clock, ShieldCheck, Activity, Award, Scale, Sparkles, X
} from 'lucide-react';

export interface ProjectData {
  id: string;
  name: string;
  category: string;
  query?: string;
  status: string;
  created_at: string;
  updated_at: string;
  version?: string;
  formulation_id?: string;
}

interface ProjectCardProps {
  project: ProjectData;
  onRename?: (id: string, newName: string) => void;
  onDuplicate?: (id: string) => void;
  onArchive?: (id: string) => void;
  onDelete?: (id: string) => void;
}

export default function ProjectCard({
  project,
  onRename,
  onDuplicate,
  onArchive,
  onDelete
}: ProjectCardProps) {
  const [showMenu, setShowMenu] = useState(false);
  const [isRenaming, setIsRenaming] = useState(false);
  const [renameInput, setRenameInput] = useState(project.name);

  const statusBadgeColor = (status: string) => {
    if (status === 'Approved' || status === 'Formulated') return 'bg-[#ECF4F0] text-[#164E3D] border-[#D1E2D9]';
    if (status === 'Archived') return 'bg-slate-100 text-slate-600 border-slate-300';
    return 'bg-amber-50 text-amber-900 border-amber-300';
  };

  const formattedCreated = new Date(project.created_at || Date.now()).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });

  const formattedModified = new Date(project.updated_at || project.created_at || Date.now()).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric'
  });

  const handleSaveRename = () => {
    if (renameInput.trim() && onRename) {
      onRename(project.id, renameInput.trim());
    }
    setIsRenaming(false);
  };

  return (
    <div className="bg-white rounded-2xl border border-[#E5E9E6] p-5 space-y-4 shadow-sm hover:border-[#164E3D] transition relative flex flex-col justify-between group">
      
      {/* Top Title & Status Header */}
      <div className="space-y-2">
        <div className="flex items-start justify-between gap-3">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-xl bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9] flex items-center justify-center shrink-0">
              <FolderGit2 className="h-4 w-4" />
            </div>
            <div>
              <span className="text-[10px] font-mono font-bold text-[#5F6D67] uppercase tracking-wider block">
                {project.category || 'Food Category'}
              </span>
              {isRenaming ? (
                <div className="flex items-center gap-1 mt-1">
                  <input
                    type="text"
                    value={renameInput}
                    onChange={(e) => setRenameInput(e.target.value)}
                    className="border border-[#164E3D] rounded-lg px-2 py-1 text-xs font-bold text-[#191C1E] focus:outline-none"
                    autoFocus
                  />
                  <button onClick={handleSaveRename} className="p-1 bg-[#164E3D] text-white rounded-lg text-xs font-bold">Save</button>
                  <button onClick={() => setIsRenaming(false)} className="p-1 text-[#5F6D67] text-xs">Cancel</button>
                </div>
              ) : (
                <h3 className="text-base font-extrabold text-[#191C1E] font-heading group-hover:text-[#164E3D] transition">
                  {project.name}
                </h3>
              )}
            </div>
          </div>

          {/* Action Popover Menu */}
          <div className="relative">
            <button
              onClick={() => setShowMenu(!showMenu)}
              className="p-1.5 rounded-lg text-[#5F6D67] hover:text-[#191C1E] hover:bg-[#F4F6F5] transition"
              title="Project options"
            >
              <MoreVertical className="h-4 w-4" />
            </button>

            {showMenu && (
              <div className="absolute right-0 mt-1 w-44 bg-white rounded-xl border border-[#E5E9E6] shadow-xl z-20 overflow-hidden font-sans p-1 text-xs font-bold space-y-0.5">
                <Link
                  href="/dashboard/formulate/guided"
                  onClick={() => setShowMenu(false)}
                  className="flex items-center gap-2 px-3 py-2 rounded-lg text-[#191C1E] hover:bg-[#ECF4F0] hover:text-[#164E3D]"
                >
                  <ExternalLink className="h-3.5 w-3.5" /> Open Project
                </Link>
                <button
                  onClick={() => {
                    setShowMenu(false);
                    setIsRenaming(true);
                  }}
                  className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-[#191C1E] hover:bg-[#ECF4F0] hover:text-[#164E3D] text-left"
                >
                  <Edit3 className="h-3.5 w-3.5" /> Rename
                </button>
                {onDuplicate && (
                  <button
                    onClick={() => {
                      setShowMenu(false);
                      onDuplicate(project.id);
                    }}
                    className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-[#191C1E] hover:bg-[#ECF4F0] hover:text-[#164E3D] text-left"
                  >
                    <Copy className="h-3.5 w-3.5" /> Duplicate
                  </button>
                )}
                {onArchive && (
                  <button
                    onClick={() => {
                      setShowMenu(false);
                      onArchive(project.id);
                    }}
                    className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-[#191C1E] hover:bg-[#ECF4F0] hover:text-[#164E3D] text-left"
                  >
                    <Archive className="h-3.5 w-3.5" /> {project.status === 'Archived' ? 'Unarchive' : 'Archive'}
                  </button>
                )}
                {onDelete && (
                  <button
                    onClick={() => {
                      setShowMenu(false);
                      if (confirm(`Delete project "${project.name}" permanently?`)) {
                        onDelete(project.id);
                      }
                    }}
                    className="w-full flex items-center gap-2 px-3 py-2 rounded-lg text-red-600 hover:bg-red-50 text-left"
                  >
                    <Trash2 className="h-3.5 w-3.5" /> Delete
                  </button>
                )}
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2 pt-1">
          <span className={`px-2.5 py-0.5 rounded-full text-[10px] font-bold font-mono border ${statusBadgeColor(project.status)}`}>
            {project.status || 'Formulated'}
          </span>
          <span className="text-[10px] font-mono text-[#5F6D67] font-bold">
            v{project.version || '1.0'}
          </span>
        </div>
      </div>

      {/* Key Formulation Metrics Summary Bar */}
      <div className="grid grid-cols-4 gap-1.5 p-2 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6] font-mono text-center text-[10px] my-3">
        <div>
          <span className="text-[#5F6D67] block font-bold uppercase text-[8px]">PROTEIN</span>
          <span className="font-extrabold text-[#191C1E]">35.5g</span>
        </div>
        <div>
          <span className="text-[#5F6D67] block font-bold uppercase text-[8px]">Aw</span>
          <span className="font-extrabold text-[#164E3D]">0.61</span>
        </div>
        <div>
          <span className="text-[#5F6D67] block font-bold uppercase text-[8px]">COST/KG</span>
          <span className="font-extrabold text-[#191C1E]">$31.60</span>
        </div>
        <div>
          <span className="text-[#5F6D67] block font-bold uppercase text-[8px]">SCORE</span>
          <span className="font-extrabold text-emerald-700">92%</span>
        </div>
      </div>

      {/* Footer Info & Open Link */}
      <div className="pt-3 border-t border-[#E5E9E6] flex items-center justify-between text-[11px] font-mono text-[#5F6D67]">
        <div className="space-y-0.5">
          <div>Created: {formattedCreated}</div>
          <div>Modified: {formattedModified}</div>
        </div>

        <Link
          href="/dashboard/formulate/guided"
          className="px-3 py-1.5 rounded-xl bg-[#ECF4F0] hover:bg-[#D1E2D9] text-[#164E3D] font-bold transition text-xs flex items-center gap-1"
        >
          Open <ExternalLink className="h-3 w-3" />
        </Link>
      </div>

    </div>
  );
}
