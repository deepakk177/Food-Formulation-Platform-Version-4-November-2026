'use client';

import React, { useState, useEffect } from 'react';
import { useStore } from '@/store/useStore';
import { useRouter } from 'next/navigation';
import {
  User, ShieldCheck, FolderGit2, Search, Filter, Plus, SlidersHorizontal,
  Activity, Clock, Settings, Building, Mail, Award, CheckCircle, Database,
  RefreshCw, Sparkles
} from 'lucide-react';
import ProjectCard, { ProjectData } from '@/components/project-card';
import RecentActivity from '@/components/recent-activity';

export default function ProfileAndHistoryPage() {
  const { user, token, projects, fetchProjects, setProjects } = useStore();
  const router = useRouter();

  // Profile data
  const userName = user?.username || 'Dr. Jane Smith';
  const userRole = user?.role || 'Senior R&D Scientist';
  const userEmail = user?.email || 'jane.smith@tcs.com';
  const department = 'Plant-Based Food Formulations & Innovation';
  const organization = 'TCS Food Formulations R&D Center';
  const initials = userName
    .split(' ')
    .map((n) => n[0])
    .join('')
    .substring(0, 3)
    .toUpperCase() || 'DJS';

  // Filters & Search state
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedStatus, setSelectedStatus] = useState('All');
  const [sortBy, setSortBy] = useState<'modified' | 'created' | 'name'>('modified');

  // Preferences state
  const [defaultUnits, setDefaultUnits] = useState('Metric (kg, g, °C)');
  const [complianceAlerts, setComplianceAlerts] = useState(true);
  const [autoSave, setAutoSave] = useState(true);
  const [ragMode, setRagMode] = useState('Deep KG Embedding');

  useEffect(() => {
    fetchProjects();
  }, []);

  // Default initial projects list if backend empty
  const defaultProjectsList: ProjectData[] = [
    {
      id: 'proj_001',
      name: 'Protein Chocolate Snack Mix',
      category: 'Confectionery & Chocolate',
      query: 'Optimized 35.5g protein per serving while maintaining Aw below 0.65.',
      status: 'Approved',
      created_at: '2026-08-20T10:15:00Z',
      updated_at: '2026-08-24T08:30:00Z',
      version: '1.0',
      formulation_id: 'FC-001'
    },
    {
      id: 'proj_002',
      name: 'Vegan High-Protein Bar',
      category: 'Bakery & Cereals',
      query: 'High protein yellow pea isolate formulation with prebiotic corn fiber.',
      status: 'Formulated',
      created_at: '2026-08-18T14:20:00Z',
      updated_at: '2026-08-23T16:45:00Z',
      version: '2.4',
      formulation_id: 'FC-002'
    },
    {
      id: 'proj_003',
      name: 'Low-Sugar Electrolyte Beverage',
      category: 'Beverages',
      query: 'Natural monk fruit sweetened hydration matrix with zero glycemic load.',
      status: 'In Development',
      created_at: '2026-08-15T09:00:00Z',
      updated_at: '2026-08-22T11:10:00Z',
      version: '1.2',
      formulation_id: 'FC-003'
    },
    {
      id: 'proj_004',
      name: 'Keto Nut Butter Snack Matrix',
      category: 'Snacks & Extruded',
      query: 'Almond butter and lecithin emulsion for thermal extruded slabs.',
      status: 'Approved',
      created_at: '2026-08-10T11:30:00Z',
      updated_at: '2026-08-21T15:20:00Z',
      version: '1.1',
      formulation_id: 'FC-004'
    },
    {
      id: 'proj_005',
      name: 'Plant-Based Burger Binder',
      category: 'Meat Analogues',
      query: 'Potato protein gelling agent for cold-pressed patties.',
      status: 'Archived',
      created_at: '2026-08-01T08:00:00Z',
      updated_at: '2026-08-14T17:00:00Z',
      version: '0.9',
      formulation_id: 'FC-005'
    }
  ];

  const activeProjectsList = projects && projects.length > 0 ? projects : defaultProjectsList;

  // Project Action Handlers (Rename, Duplicate, Archive, Delete)
  const handleRenameProject = async (id: string, newName: string) => {
    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      await fetch(`${api_url}/api/projects/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: newName })
      });
      fetchProjects();
    } catch (err) {
      console.error('Rename error:', err);
    }
  };

  const handleDuplicateProject = async (id: string) => {
    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      await fetch(`${api_url}/api/projects/${id}/duplicate`, { method: 'POST' });
      fetchProjects();
    } catch (err) {
      console.error('Duplicate error:', err);
    }
  };

  const handleArchiveProject = async (id: string) => {
    try {
      const proj = activeProjectsList.find(p => p.id === id);
      const newStatus = proj?.status === 'Archived' ? 'Formulated' : 'Archived';
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      await fetch(`${api_url}/api/projects/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: newStatus })
      });
      fetchProjects();
    } catch (err) {
      console.error('Archive error:', err);
    }
  };

  const handleDeleteProject = async (id: string) => {
    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      await fetch(`${api_url}/api/projects/${id}`, { method: 'DELETE' });
      fetchProjects();
    } catch (err) {
      console.error('Delete error:', err);
    }
  };

  // Filter & Sort Logic
  const filteredProjects = activeProjectsList.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          p.category.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          (p.query && p.query.toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'All' || p.category === selectedCategory;
    const matchesStatus = selectedStatus === 'All' || p.status === selectedStatus;
    return matchesSearch && matchesCategory && matchesStatus;
  }).sort((a, b) => {
    if (sortBy === 'name') return a.name.localeCompare(b.name);
    if (sortBy === 'created') return new Date(b.created_at).getTime() - new Date(a.created_at).getTime();
    return new Date(b.updated_at || b.created_at).getTime() - new Date(a.updated_at || a.created_at).getTime();
  });

  return (
    <div className="space-y-8 max-w-7xl mx-auto font-sans text-[#191C1E] py-4">

      {/* SECTION 1: USER PROFILE HEADER CARD */}
      <div className="bg-white rounded-2xl border border-[#E5E9E6] p-6 sm:p-7 shadow-sm space-y-6">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 border-b border-[#E5E9E6] pb-6">
          
          <div className="flex items-center gap-5">
            <div className="h-16 w-16 rounded-full bg-[#164E3D] text-white font-extrabold text-xl flex items-center justify-center font-mono shadow-md border-2 border-[#ECF4F0]">
              {initials}
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <h1 className="text-2xl font-extrabold text-[#191C1E] font-heading">{userName}</h1>
                <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-[#ECF4F0] text-[#164E3D] border border-[#D1E2D9] font-mono">
                  Verified R&D Account
                </span>
              </div>
              <p className="text-xs text-[#5F6D67] font-bold font-mono">
                {userRole} • {department}
              </p>
              <div className="flex flex-wrap items-center gap-4 text-xs text-[#5F6D67] font-bold pt-0.5">
                <span className="flex items-center gap-1.5"><Building className="h-3.5 w-3.5 text-[#164E3D]" /> {organization}</span>
                <span className="flex items-center gap-1.5"><Mail className="h-3.5 w-3.5 text-[#164E3D]" /> {userEmail}</span>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 self-start md:self-auto">
            <button
              onClick={() => router.push('/dashboard/formulate/guided')}
              className="px-4 py-2.5 rounded-xl bg-[#164E3D] hover:bg-[#123F32] text-white font-extrabold text-xs transition shadow-sm flex items-center gap-2"
            >
              <Plus className="h-4 w-4" /> New Formulation Project
            </button>
          </div>

        </div>

        {/* Account Statistics Counter Strip */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 font-mono text-center">
          <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
            <span className="text-[10px] text-[#5F6D67] font-bold uppercase tracking-wider block">Total Projects</span>
            <span className="text-2xl font-extrabold text-[#164E3D]">{activeProjectsList.length}</span>
          </div>
          <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
            <span className="text-[10px] text-[#5F6D67] font-bold uppercase tracking-wider block">Formulations Synthesized</span>
            <span className="text-2xl font-extrabold text-[#191C1E]">14</span>
          </div>
          <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
            <span className="text-[10px] text-[#5F6D67] font-bold uppercase tracking-wider block">Compliance Audit Rate</span>
            <span className="text-2xl font-extrabold text-emerald-700">100%</span>
          </div>
          <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6]">
            <span className="text-[10px] text-[#5F6D67] font-bold uppercase tracking-wider block">Avg Feasibility Score</span>
            <span className="text-2xl font-extrabold text-[#164E3D]">93.4%</span>
          </div>
        </div>
      </div>

      {/* SECTION 2: MY PROJECTS & SEARCH / FILTERS */}
      <div id="projects" className="space-y-5">
        
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 className="text-xl font-extrabold text-[#191C1E] font-heading flex items-center gap-2">
              <FolderGit2 className="h-5 w-5 text-[#164E3D]" /> My Formulation Projects
            </h2>
            <p className="text-xs text-[#5F6D67] font-bold mt-0.5">
              Manage, duplicate, archive, and open all your authenticated food formulation projects.
            </p>
          </div>
        </div>

        {/* Search and Filters Bar */}
        <div className="bg-white p-4 rounded-2xl border border-[#E5E9E6] shadow-sm flex flex-col md:flex-row items-center justify-between gap-4 font-sans text-xs font-bold">
          
          {/* Search Box */}
          <div className="relative w-full md:w-80">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-[#5F6D67]" />
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Search project name or query..."
              className="w-full bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl pl-10 pr-4 py-2.5 text-xs text-[#191C1E] placeholder-[#5F6D67] focus:outline-none focus:border-[#164E3D] transition"
            />
          </div>

          {/* Filter Dropdowns */}
          <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
            
            <div className="flex items-center gap-1.5">
              <span className="text-[#5F6D67]">Category:</span>
              <select
                value={selectedCategory}
                onChange={(e) => setSelectedCategory(e.target.value)}
                className="bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl px-3 py-2 text-xs font-bold text-[#191C1E] focus:outline-none"
              >
                <option value="All">All Categories</option>
                <option value="Confectionery & Chocolate">Confectionery & Chocolate</option>
                <option value="Bakery & Cereals">Bakery & Cereals</option>
                <option value="Beverages">Beverages</option>
                <option value="Dairy & Alternatives">Dairy & Alternatives</option>
                <option value="Snacks & Extruded">Snacks & Extruded</option>
                <option value="Meat Analogues">Meat Analogues</option>
              </select>
            </div>

            <div className="flex items-center gap-1.5">
              <span className="text-[#5F6D67]">Status:</span>
              <select
                value={selectedStatus}
                onChange={(e) => setSelectedStatus(e.target.value)}
                className="bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl px-3 py-2 text-xs font-bold text-[#191C1E] focus:outline-none"
              >
                <option value="All">All Statuses</option>
                <option value="Approved">Approved</option>
                <option value="Formulated">Formulated</option>
                <option value="In Development">In Development</option>
                <option value="Archived">Archived</option>
              </select>
            </div>

            <div className="flex items-center gap-1.5">
              <span className="text-[#5F6D67]">Sort:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl px-3 py-2 text-xs font-bold text-[#191C1E] focus:outline-none font-mono"
              >
                <option value="modified">Recently Modified</option>
                <option value="created">Created Date</option>
                <option value="name">Name (A-Z)</option>
              </select>
            </div>

          </div>
        </div>

        {/* Projects Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProjects.map((project) => (
            <ProjectCard
              key={project.id}
              project={project}
              onRename={handleRenameProject}
              onDuplicate={handleDuplicateProject}
              onArchive={handleArchiveProject}
              onDelete={handleDeleteProject}
            />
          ))}
        </div>

      </div>

      {/* SECTION 3: RECENT ACTIVITY & ACCOUNT PREFERENCES */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Recent Activity Log (LG: 7 COLS) */}
        <div id="activity" className="lg:col-span-7">
          <RecentActivity />
        </div>

        {/* Account Preferences & Settings (LG: 5 COLS) */}
        <div id="preferences" className="lg:col-span-5 bg-white rounded-2xl border border-[#E5E9E6] p-5 space-y-4 shadow-sm font-sans">
          <div className="border-b border-[#E5E9E6] pb-3">
            <h3 className="text-base font-extrabold text-[#191C1E] font-heading flex items-center gap-2">
              <Settings className="h-4 w-4 text-[#164E3D]" /> Preferences & Settings
            </h3>
          </div>

          <div className="space-y-4 text-xs font-bold text-[#191C1E]">
            
            {/* Units Preference */}
            <div className="space-y-1.5">
              <label className="block text-[#5F6D67] font-bold">Default Measurement System:</label>
              <select
                value={defaultUnits}
                onChange={(e) => setDefaultUnits(e.target.value)}
                className="w-full bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl p-2.5 text-xs font-bold text-[#191C1E] focus:outline-none"
              >
                <option value="Metric (kg, g, °C)">Metric (kg, g, °C)</option>
                <option value="Imperial (lbs, oz, °F)">Imperial (lbs, oz, °F)</option>
              </select>
            </div>

            {/* AI Engine Mode */}
            <div className="space-y-1.5">
              <label className="block text-[#5F6D67] font-bold">Formulation Reasoning Mode:</label>
              <select
                value={ragMode}
                onChange={(e) => setRagMode(e.target.value)}
                className="w-full bg-[#FAFAF8] border border-[#E5E9E6] rounded-xl p-2.5 text-xs font-bold text-[#191C1E] focus:outline-none font-mono"
              >
                <option value="Deep KG Embedding">Deep Knowledge-Graph Embedding (Grounded)</option>
                <option value="Fast Heuristic">Fast Heuristic Optimization</option>
              </select>
            </div>

            {/* Toggles */}
            <div className="space-y-3 border-t border-[#E5E9E6] pt-3">
              <label className="flex items-center justify-between cursor-pointer">
                <span>Regional Compliance Alerts</span>
                <input
                  type="checkbox"
                  checked={complianceAlerts}
                  onChange={(e) => setComplianceAlerts(e.target.checked)}
                  className="h-4 w-4 accent-[#164E3D] rounded"
                />
              </label>

              <label className="flex items-center justify-between cursor-pointer">
                <span>Formulation Auto-Save to SQLite</span>
                <input
                  type="checkbox"
                  checked={autoSave}
                  onChange={(e) => setAutoSave(e.target.checked)}
                  className="h-4 w-4 accent-[#164E3D] rounded"
                />
              </label>
            </div>

            {/* Organization Info Box */}
            <div className="p-3 bg-[#ECF4F0] rounded-xl border border-[#D1E2D9] text-[11px] text-[#164E3D] font-mono font-bold space-y-1">
              <div>ORGANIZATION ID: TCS-FOOD-RD-2026</div>
              <div>LICENSED TO: {organization}</div>
              <div className="text-[9px] text-[#5F6D67]">All formulation data protected under Enterprise Confidentiality Agreement.</div>
            </div>

          </div>
        </div>

      </div>

    </div>
  );
}
