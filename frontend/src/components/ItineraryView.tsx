"use client";

import React from "react";

interface Activity {
  time: string;
  poi_name: string;
  category: string;
  description: string;
  feasibility_notes?: string;
}

interface DaySchedule {
  day: number;
  theme: string;
  activities: Activity[];
}

interface ItineraryViewProps {
  title: string;
  destination: string;
  durationDays: number;
  budget: string;
  schedule: DaySchedule[];
}

export default function ItineraryView({
  title,
  destination,
  durationDays,
  budget,
  schedule,
}: ItineraryViewProps) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 space-y-6">
      {/* Header Itinerary */}
      <div className="border-b border-slate-100 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-2.5 py-1 rounded-full uppercase">
            {destination}
          </span>
          <h2 className="text-xl font-extrabold text-slate-800 mt-2">{title}</h2>
        </div>
        <div className="flex gap-2 text-xs font-medium">
          <span className="bg-slate-100 text-slate-700 px-3 py-1.5 rounded-lg border border-slate-200">
            Durasi: {durationDays} Hari
          </span>
          <span className="bg-slate-100 text-slate-700 px-3 py-1.5 rounded-lg border border-slate-200">
            Budget: {budget}
          </span>
        </div>
      </div>

      {/* Indikator Evaluasi Sistem (Feasibility, Rationality, Personalization) */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs bg-slate-50 p-3 rounded-xl border border-slate-100">
        <div className="flex items-center gap-2">
          <span className="text-emerald-600 font-bold">&#x2713; Feasibility</span>
          <span className="text-slate-500">Waktu & Tempat Layak</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-blue-600 font-bold">&#x2713; Rationality</span>
          <span className="text-slate-500">Rute Spasial Koheren</span>
        </div>
        <div className="flex items-center gap-2">
          <span className="text-purple-600 font-bold">&#x2713; Personalization</span>
          <span className="text-slate-500">Sesuai Profil Implisit</span>
        </div>
      </div>

      {/* Timeline Jadwal Harian */}
      <div className="space-y-6">
        {schedule.map((dayItem) => (
          <div key={dayItem.day} className="border border-slate-200 rounded-xl p-5 bg-slate-50/50">
            <div className="flex items-center justify-between mb-3 border-b border-slate-200/60 pb-2">
              <h3 className="font-bold text-slate-800 text-sm">
                Hari ke-{dayItem.day}: <span className="text-blue-600 font-medium">{dayItem.theme}</span>
              </h3>
            </div>

            <div className="space-y-3">
              {dayItem.activities.map((act, idx) => (
                <div key={idx} className="bg-white p-3.5 rounded-lg border border-slate-200/80 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                  <div className="flex items-start gap-3">
                    <span className="font-mono text-xs font-bold text-slate-500 bg-slate-100 px-2 py-1 rounded border border-slate-200 mt-0.5">
                      {act.time}
                    </span>
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-slate-800 text-sm">{act.poi_name}</span>
                        <span className="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium">
                          {act.category}
                        </span>
                      </div>
                      <p className="text-xs text-slate-600 mt-1">{act.description}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}