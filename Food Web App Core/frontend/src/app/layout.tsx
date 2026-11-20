import React from 'react';
import type { Metadata } from 'next';
import AppShell from '@/components/app-shell';
import './globals.css';

export const metadata: Metadata = {
  title: 'Food Formulator — AI-Powered Food Intelligence Platform',
  description: 'Accelerating Scientific Food Formulation Through AI, Knowledge-Graph Intelligence, and Compliance Audits.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#F7F9F8] text-[#191C1E] antialiased selection:bg-[#164E3D] selection:text-white flex flex-col">
        <AppShell>
          {children}
        </AppShell>
      </body>
    </html>
  );
}
