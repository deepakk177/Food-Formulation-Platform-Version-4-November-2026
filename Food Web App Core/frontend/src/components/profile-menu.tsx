'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { useStore } from '@/store/useStore';
import { User, FolderGit2, Settings, LogOut, ChevronDown, ShieldCheck, Sparkles, Clock } from 'lucide-react';

export default function ProfileMenu() {
  const { user, token, logout } = useStore();
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const router = useRouter();

  const userName = user?.username || 'Dr. Jane Smith';
  const userRole = user?.role || 'Senior R&D Scientist';
  const userEmail = user?.email || 'jane.smith@tcs.com';
  const initials = userName
    .split(' ')
    .map((n) => n[0])
    .join('')
    .substring(0, 3)
    .toUpperCase() || 'DJS';

  // Close popover when clicking outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="relative" ref={menuRef}>
      {/* Profile Trigger Button matching current UI */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2.5 p-1 rounded-full hover:bg-[#F4F6F5] transition text-left focus:outline-none"
      >
        <div className="h-9 w-9 rounded-full bg-[#ECF4F0] border border-[#D1E2D9] text-[#164E3D] font-extrabold text-xs flex items-center justify-center font-mono shadow-2xs">
          {initials}
        </div>
        <div className="hidden sm:flex flex-col text-left">
          <span className="text-xs font-bold text-[#191C1E] leading-tight">{userName}</span>
          <span className="text-[9px] font-mono text-[#5F6D67] uppercase tracking-wider leading-tight">
            {userRole}
          </span>
        </div>
        <ChevronDown className={`h-4 w-4 text-[#5F6D67] transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {/* Popover Menu */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-72 bg-white rounded-2xl border border-[#E5E9E6] shadow-xl z-50 overflow-hidden font-sans space-y-1 p-2">
          
          {/* Header User Card */}
          <div className="p-3 bg-[#FAFAF8] rounded-xl border border-[#E5E9E6] space-y-1">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-full bg-[#164E3D] text-white font-extrabold text-xs flex items-center justify-center font-mono shadow-xs">
                {initials}
              </div>
              <div className="overflow-hidden">
                <div className="text-sm font-extrabold text-[#191C1E] truncate">{userName}</div>
                <div className="text-[10px] text-[#5F6D67] font-mono truncate">{userEmail}</div>
              </div>
            </div>
            <div className="mt-2 pt-2 border-t border-[#E5E9E6] flex justify-between items-center text-[10px] font-mono text-[#164E3D] font-bold">
              <span>R&D Scientist • Tier 1</span>
              <span className="px-2 py-0.5 rounded-full bg-[#ECF4F0] border border-[#D1E2D9]">Active</span>
            </div>
          </div>

          {/* Quick Menu Options */}
          <div className="space-y-0.5 pt-1">
            <Link
              href="/dashboard/profile"
              onClick={() => setIsOpen(false)}
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-[#191C1E] hover:bg-[#ECF4F0] hover:text-[#164E3D] transition"
            >
              <User className="h-4 w-4 text-[#164E3D]" />
              <span>Profile & Project History</span>
            </Link>

            <Link
              href="/dashboard/profile#projects"
              onClick={() => setIsOpen(false)}
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-[#191C1E] hover:bg-[#ECF4F0] hover:text-[#164E3D] transition"
            >
              <FolderGit2 className="h-4 w-4 text-[#164E3D]" />
              <span>My Projects & Formulations</span>
            </Link>

            <Link
              href="/dashboard/profile#activity"
              onClick={() => setIsOpen(false)}
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-[#191C1E] hover:bg-[#ECF4F0] hover:text-[#164E3D] transition"
            >
              <Clock className="h-4 w-4 text-[#164E3D]" />
              <span>Recent Activity Log</span>
            </Link>

            <Link
              href="/dashboard/profile#preferences"
              onClick={() => setIsOpen(false)}
              className="flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-[#191C1E] hover:bg-[#ECF4F0] hover:text-[#164E3D] transition"
            >
              <Settings className="h-4 w-4 text-[#5F6D67]" />
              <span>Account Preferences</span>
            </Link>
          </div>

          {/* Sign Out Action */}
          <div className="border-t border-[#E5E9E6] pt-1">
            <button
              onClick={() => {
                setIsOpen(false);
                logout();
                router.push('/login');
              }}
              className="w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold text-red-600 hover:bg-red-50 transition text-left"
            >
              <LogOut className="h-4 w-4" />
              <span>Sign Out</span>
            </button>
          </div>

        </div>
      )}
    </div>
  );
}
