'use client';

import React, { useEffect } from 'react';
import { useStore } from '@/store/useStore';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Leaf, LayoutDashboard, FileText, Database, ShieldCheck,
  Search, Bell, Settings, User as UserIcon, Network
} from 'lucide-react';
import ProfileMenu from '@/components/profile-menu';

export default function AppShell({
  children,
}: {
  children: React.ReactNode;
}) {
  const { initializeAuth } = useStore();
  const pathname = usePathname();

  useEffect(() => {
    initializeAuth();
  }, [initializeAuth]);

  const navItems = [
    { label: 'Dashboard', href: '/dashboard', icon: LayoutDashboard },
    { label: 'Ingredient Library', href: '/dashboard/ingredients', icon: Database },
    { label: 'Knowledge Graph', href: '/dashboard/knowledge-graph', icon: Network },
    { label: 'Profile & History', href: '/dashboard/profile', icon: UserIcon },
  ];

  const projectsList = [
    { name: 'Vegan Protein Bar', href: '/dashboard/formulate/guided' },
    { name: 'Low-Sugar Beverage', href: '/dashboard/formulate/guided' },
    { name: 'Keto Snack Mix', href: '/dashboard/formulate/guided' },
  ];

  return (
    <>
      {/* Canonical Top Navigation Header */}
      <header className="sticky top-0 z-40 w-full bg-white border-b border-[#E5E9E6] h-16 px-4 lg:px-6 flex items-center justify-between shadow-sm">
        {/* Left Brand Identifier */}
        <div className="flex items-center gap-3 w-64">
          <Link href="/" className="flex items-center gap-2.5 group">
            <div className="h-9 w-9 rounded-xl bg-[#164E3D] text-white flex items-center justify-center shadow-md group-hover:bg-[#123F32] transition">
              <Leaf className="h-5 w-5" />
            </div>
            <span className="font-extrabold text-lg text-[#191C1E] tracking-tight font-heading">
              Food Formulator
            </span>
          </Link>
        </div>

        {/* Center Search Input (⌘K) */}
        <div className="flex-1 max-w-md mx-4 hidden md:block">
          <div className="relative">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-[#5F6D67]" />
            <input
              type="text"
              placeholder="Search projects, ingredients..."
              className="w-full bg-[#F7F9F8] border border-[#E5E9E6] rounded-full pl-10 pr-12 py-2 text-xs text-[#191C1E] placeholder-[#5F6D67] focus:outline-none focus:border-[#164E3D] focus:bg-white transition"
            />
            <span className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] font-mono font-bold text-[#5F6D67] bg-[#E5E9E6]/60 px-1.5 py-0.5 rounded">
              ⌘K
            </span>
          </div>
        </div>

        {/* Right User Status & Actions */}
        <div className="flex items-center gap-4">
          <button type="button" className="p-2 text-[#5F6D67] hover:text-[#164E3D] hover:bg-[#F7F9F8] rounded-full transition relative" title="Notifications">
            <Bell className="h-5 w-5" />
            <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-[#164E3D]" />
          </button>

          <Link href="/dashboard/profile#preferences" className="p-2 text-[#5F6D67] hover:text-[#164E3D] hover:bg-[#F7F9F8] rounded-full transition" title="Settings & Preferences">
            <Settings className="h-5 w-5" />
          </Link>

          <div className="h-6 w-[1px] bg-[#E5E9E6]" />

          {/* Profile Popover Menu */}
          <ProfileMenu />
        </div>
      </header>

      {/* App Shell Container (Sidebar + Main View) */}
      <div className="flex-1 flex min-h-[calc(100vh-4rem)]">
        {/* Canonical Left Sidebar Navigation */}
        <aside className="w-64 border-r border-[#E5E9E6] bg-white hidden lg:flex flex-col justify-between p-4 shrink-0 sticky top-16 h-[calc(100vh-4rem)] overflow-y-auto">
          <div className="space-y-6">
            {/* Main Menu Links */}
            <div>
              <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-[#5F6D67] px-3 block mb-2">
                MAIN MENU
              </span>
              <nav className="space-y-1">
                {navItems.map((item) => {
                  const Icon = item.icon;
                  const isActive =
                    item.href === '/dashboard'
                      ? pathname === '/dashboard' || pathname === '/'
                      : pathname.startsWith(item.href);
                  return (
                    <Link
                      key={item.label}
                      href={item.href}
                      className={`flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold transition ${isActive
                          ? 'bg-[#ECF4F0] border border-[#D1E2D9] text-[#164E3D] shadow-sm'
                          : 'text-[#5F6D67] hover:text-[#191C1E] hover:bg-[#F7F9F8]'
                        }`}
                    >
                      <Icon className={`h-4 w-4 ${isActive ? 'text-[#164E3D]' : 'text-[#5F6D67]'}`} />
                      <span>{item.label}</span>
                    </Link>
                  );
                })}
              </nav>
            </div>

            {/* Projects List */}
            <div>
              <span className="text-[10px] font-mono font-bold uppercase tracking-wider text-[#5F6D67] px-3 block mb-2">
                PROJECTS
              </span>
              <div className="space-y-1">
                {projectsList.map((proj) => (
                  <Link
                    key={proj.name}
                    href={proj.href}
                    className="flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs text-[#5F6D67] hover:text-[#164E3D] hover:bg-[#F7F9F8] transition"
                  >
                    <span className="h-2 w-2 rounded-full bg-[#164E3D] shrink-0" />
                    <span className="font-semibold truncate">{proj.name}</span>
                  </Link>
                ))}
              </div>
            </div>
          </div>
        </aside>

        {/* Main Body Page View */}
        <main className="flex-1 min-w-0 p-4 lg:p-8 bg-[#F7F9F8]">
          {children}
        </main>
      </div>
    </>
  );
}
