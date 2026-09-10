'use client';

import React, { useState, useEffect } from 'react';
import { useStore } from '@/store/useStore';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { ChefHat, Loader2, Lock, Mail, User } from 'lucide-react';

export default function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('Guided User');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const { token, setToken, setUser } = useStore();
  const router = useRouter();

  useEffect(() => {
    if (token) {
      router.push('/dashboard');
    }
  }, [token, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const api_url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${api_url}/api/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, role }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || 'Registration failed');
      }

      const data = await response.json();
      setToken(data.access_token);
      
      const userProfile = {
        username: data.username,
        email: data.email,
        role: data.role
      };
      
      setUser(userProfile);
      if (typeof window !== 'undefined') {
        localStorage.setItem('tf_user', JSON.stringify(userProfile));
      }

      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Username or email already registered');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-[80vh] items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8 glass-panel p-8 rounded-2xl border border-slate-900 shadow-xl relative">
        <div className="text-center">
          <div className="mx-auto h-12 w-12 flex items-center justify-center rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 mb-4">
            <ChefHat className="h-6 w-6" />
          </div>
          <h2 className="text-3xl font-extrabold tracking-tight text-white">Get Started</h2>
          <p className="mt-2 text-sm text-slate-400">
            Create an account to join the TCS Food Formulation platform
          </p>
        </div>

        {error && (
          <div className="rounded-lg bg-red-950/20 border border-red-800/50 p-4 text-sm text-red-400">
            {error}
          </div>
        )}

        <form className="mt-8 space-y-6" onSubmit={handleSubmit}>
          <div className="space-y-4 rounded-md shadow-sm">
            <div>
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Username</label>
              <div className="relative">
                <User className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-500" />
                <input
                  type="text"
                  required
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  className="w-full pl-11 pr-4 py-3 bg-slate-950/80 border border-slate-800 rounded-xl text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition text-sm"
                  placeholder="johndoe"
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-500" />
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full pl-11 pr-4 py-3 bg-slate-950/80 border border-slate-800 rounded-xl text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition text-sm"
                  placeholder="name@company.com"
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">Password</label>
              <div className="relative">
                <Lock className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4.5 w-4.5 text-slate-500" />
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full pl-11 pr-4 py-3 bg-slate-950/80 border border-slate-800 rounded-xl text-white placeholder-slate-600 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition text-sm"
                  placeholder="••••••••"
                />
              </div>
            </div>

            <div>
              <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider block mb-1.5">User Role</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full px-4 py-3 bg-slate-950/80 border border-slate-800 rounded-xl text-white focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition text-sm appearance-none"
              >
                <option value="Guided User">Guided User (Stepper Wizard)</option>
                <option value="Expert User">Expert User (Drag & Drop Canvas)</option>
                <option value="Administrator">Administrator</option>
              </select>
            </div>
          </div>

          <div>
            <button
              type="submit"
              disabled={loading}
              className="group relative flex w-full justify-center rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 px-4 py-3 text-sm font-semibold text-white hover:opacity-95 transition shadow-lg shadow-indigo-500/10 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Creating Account...
                </>
              ) : (
                'Register'
              )}
            </button>
          </div>
        </form>

        <div className="text-center mt-4">
          <p className="text-xs text-slate-500">
            Already have an account?{' '}
            <Link href="/login" className="text-indigo-400 hover:text-indigo-300 font-medium">
              Log in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
