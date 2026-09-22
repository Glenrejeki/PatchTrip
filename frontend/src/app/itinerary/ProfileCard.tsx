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
  // Contoh data riwayat tiruan (bisa diganti dengan data array dinamis dari backend)
  const pastTrips = [
    { destination: "Bali", theme: "Pantai & Sunset", year: "2025" },
    { destination: "Bandung", theme: "Kuliner & Alam", year: "2025" },
    { destination: "Lombok", theme: "Wisata Bahari", year: "2024" },
    { destination: "Malang", theme: "Pegunungan", year: "2024" },
  ];

  return (
    <div className="space-y-4">
      {/* Kartu Profil Utama */}
      <div className="bg-white px-5 py-4 rounded-xl border border-slate-200/80 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-sm">
        <div className="flex items-center gap-3">
          <span className="w-2 h-2 rounded-full bg-blue-600 shrink-0"></span>
          <div>
            <span className="font-semibold text-slate-800">Profil: {userId || "Pengguna"}</span>
            <span className="text-slate-400 mx-2">&middot;</span>
            <span className="text-slate-600 italic">&ldquo;{preferenceProfile || "Belum ada preferensi"}&rdquo;</span>
          </div>
        </div>
        
        <div className="text-xs text-slate-500 font-medium shrink-0 sm:text-right border-t sm:border-t-0 pt-2 sm:pt-0 border-slate-100">
          Analisis: <span className="font-bold text-slate-700">{totalTripsAnalyzed || 4} Trip</span>
        </div>
      </div>

      {/* Kotak Riwayat Perjalanan (History Viewer Section) */}
      <div className="bg-slate-50 p-4 rounded-xl border border-slate-200/60 text-xs text-slate-600 space-y-2">
        <span className="font-bold uppercase tracking-wider text-slate-400 block">
          Rekam Jejak Riwayat Perjalanan (Hierarchical Patch Source):
        </span>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {pastTrips.slice(0, totalTripsAnalyzed).map((trip, idx) => (
            <div key={idx} className="bg-white p-2.5 rounded-lg border border-slate-200 shadow-2xs">
              <span className="font-bold text-slate-800 block">{trip.destination}</span>
              <span className="text-slate-500">{trip.theme} ({trip.year})</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}