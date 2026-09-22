import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import React from "react";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "PatchTrip - AI Personalized Travel Planner",
  description: "Sistem perencanaan perjalanan wisata cerdas berbasis Hierarchical Patch Compression dan RAG.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <body className={`${inter.className} bg-slate-50 text-slate-900 antialiased min-h-screen flex flex-col`}>
        {/* Navbar Global */}
        <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <span className="bg-blue-600 text-white font-bold px-3 py-1.5 rounded-lg text-lg shadow-sm">PT</span>
              <h1 className="text-xl font-extrabold tracking-tight text-slate-800">PatchTrip AI</h1>
            </div>
            <div className="text-sm font-medium text-slate-500">
              Thesis Project - Smart Itinerary Generator
            </div>
          </div>
        </header>

        {/* Konten Utama Halaman */}
        <main className="flex-grow max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {children}
        </main>

        {/* Footer Global */}
        <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-400">
          &copy; {new Date().getFullYear()} PatchTrip System. All rights reserved.
        </footer>
      </body>
    </html>
  );
}