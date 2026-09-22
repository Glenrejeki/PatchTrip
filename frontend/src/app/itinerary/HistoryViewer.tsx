"use client";

import React from "react";
import ProfileCard from "./ProfileCard";

interface Activity {
  time: string;
  poi_name: string;
  category: string;
  description: string;
  similarity_score?: number;
}

interface DaySchedule {
  day_number: number;
  theme: string;
  activities: Activity[];
}

// 1. DEFINISIKAN PROPS INTERFACE DI SINI AGAR TIDAK ERROR
interface HistoryViewerProps {
  userId: string;
  totalTrips: number;
  profileSummary: string;
  destination: string;
  title: string;
  durationDays: number;
  budgetLevel: string;
  days: DaySchedule[];
}

export default function HistoryViewer({
  userId,
  totalTrips,
  profileSummary,
  destination,
  title,
  durationDays,
  budgetLevel,
  days,
}: HistoryViewerProps) {
  return (
    <div className="space-y-6">
      {/* Profile Card (Menampilkan Abstraksi Profil & Riwayat) */}
      <ProfileCard 
        userId={userId}
        totalTripsAnalyzed={totalTrips}
        preferenceProfile={profileSummary}
      />

      {/* Informasi Utama Itinerary */}
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <span className="bg-blue-100 text-blue-700 text-xs font-bold px-2.5 py-1 rounded-full uppercase">
          {destination}
        </span>
        <h1 className="text-2xl font-black text-slate-800 mt-2">{title}</h1>
        <p className="text-sm text-slate-500 mt-1">
          Durasi: <span className="font-semibold text-slate-700">{durationDays} Hari</span> | 
          Budget: <span className="font-semibold text-slate-700">{budgetLevel}</span>
        </p>
      </div>

      {/* Daftar Jadwal Harian & Skor FAISS */}
      <div className="space-y-6">
        {days.map((day) => (
          <div key={day.day_number} className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
            <div className="border-b border-slate-100 pb-3 mb-4">
              <span className="text-xs font-bold uppercase tracking-wider text-blue-600">Hari ke-{day.day_number}</span>
              <h2 className="text-lg font-bold text-slate-800">{day.theme}</h2>
            </div>

            <div className="space-y-4">
              {day.activities.map((act, index) => (
                <div key={index} className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl bg-slate-50 border border-slate-100 hover:border-slate-200 transition">
                  <div className="flex gap-4 items-start">
                    <div className="font-mono text-xs font-bold text-slate-500 bg-white px-2.5 py-1.5 rounded-lg border border-slate-200 h-fit mt-0.5">
                      {act.time}
                    </div>
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <h3 className="font-bold text-slate-800">{act.poi_name}</h3>
                        <span className="text-[10px] font-medium bg-slate-200 text-slate-700 px-2 py-0.5 rounded">
                          {act.category}
                        </span>
                      </div>
                      <p className="text-sm text-slate-600 mt-1">{act.description}</p>
                    </div>
                  </div>

                  {act.similarity_score !== undefined && (
                    <div className="bg-blue-50 border border-blue-100 px-3 py-1.5 rounded-lg text-right shrink-0">
                      <span className="text-[10px] text-blue-600 font-semibold block uppercase">FAISS Match</span>
                      <span className="font-mono text-xs font-bold text-blue-700">
                        {(act.similarity_score * 100).toFixed(1)}%
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}