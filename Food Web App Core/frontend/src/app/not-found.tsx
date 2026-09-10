'use client';

import Link from 'next/link';
import { ChefHat, ArrowLeft, Home, Compass } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="min-h-[70vh] flex flex-col items-center justify-center text-center py-16 px-4">
      <div className="h-16 w-16 rounded-2xl bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 flex items-center justify-center mb-6 shadow-xl">
        <Compass className="h-8 w-8 animate-pulse" />
      </div>

      <span className="text-xs font-mono font-bold text-emerald-400 uppercase tracking-widest bg-emerald-950/60 px-3 py-1 rounded-full border border-emerald-800/50 mb-3">
        404 — Page Not Found
      </span>

      <h1 className="text-3xl sm:text-4xl font-extrabold text-white tracking-tight mb-3">
        Looking for a Formulation Route?
      </h1>

      <p className="text-slate-400 text-sm max-w-md mx-auto mb-8 leading-relaxed">
        The page or route you requested could not be located in our AI Food Formulator directory.
      </p>

      <div className="flex flex-wrap justify-center gap-4">
        <Link
          href="/dashboard"
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-700 hover:bg-emerald-600 text-white font-semibold text-xs transition shadow-lg"
        >
          <Home className="h-4 w-4" />
          Return to Dashboard
        </Link>

        <Link
          href="/dashboard/formulate/guided"
          className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-300 hover:text-white font-semibold text-xs transition"
        >
          <ChefHat className="h-4 w-4 text-indigo-400" />
          Guided Formulator
        </Link>
      </div>
    </div>
  );
}
