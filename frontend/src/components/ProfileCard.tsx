"use client";

import React from "react";

interface ProfileCardProps {
  userId: string;
  totalTripsAnalyzed: number;
  preferenceProfile: string;
}

export default function ProfileCard({
  userId,
  totalTripsAnalyzed,
  preferenceProfile,
}: ProfileCardProps) {
  return (
    <div className="bg-gradient-to-br from-blue-900 to-slate-900 text-white p-6 rounded-2xl shadow-md border border-blue-800">
      <div className="flex items-center justify-between border-b border-blue-800/60 pb-4 mb-4">
        <div>
          <span className="text-xs font-bold uppercase tracking-wider text-blue-400 bg-blue-950 px-2.5 py-1 rounded-full border border-blue-700/50">
            User Preference Profile (Level-3 Compression)
          </span>
          <h2 className="text-lg font-bold mt-2">Profil Implisit Pengguna: {userId}</h2>
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-400 block">Riwayat Dianalisis</span>
          <span className="text-xl font-black text-blue-300">{totalTripsAnalyzed} Trip</span>
        </div>
      </div>

      <div className="bg-slate-950/50 p-4 rounded-xl border border-blue-900/40">
        <p className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1">
        Abstraksi Preferensi Jangka Panjang:
        </p>
        <p className="text-sm text-slate-200 leading-relaxed italic">
          &ldquo;{preferenceProfile}&rdquo;
        </p>
      </div>

      <div className="mt-4 flex items-center gap-2 text-[11px] text-slate-400">
        <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
        <span>Kompresi hierarkis aktif: Mereduksi noise perjalanan masa lalu secara efektif.</span>
      </div>
    </div>
  );
}