"use client";

import React from "react";

interface Activity {
  time: string;
  poi_name: string;
  category: string;
  description: string;
  feasibility_notes?: string;
  similarity_score?: number;
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
  schedule = [],
}: ItineraryViewProps) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200 space-y-6">
      {/* Header Itinerary */}
      <div className="border-b border-slate-100 pb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <span className="bg-emerald-100 text-emerald-800 text-xs font-bold px-2.5 py-1 rounded-full uppercase">
            {destination || "Destinasi AI"}
          </span>
          <h2 className="text-xl font-extrabold text-slate-800 mt-2">
            {title || "Belum ada rencana perjalanan"}
          </h2>
        </div>
        <div className="flex gap-2 text-xs font-medium">
          <span className="bg-slate-100 text-slate-700 px-3 py-1.5 rounded-lg border border-slate-200">
            Durasi: {durationDays || 0} Hari
          </span>
          <span className="bg-slate-100 text-slate-700 px-3 py-1.5 rounded-lg border border-slate-200">
            Budget: {budget || "-"}
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
        {schedule && schedule.length > 0 ? (
          schedule.map((dayItem) => (
            <div key={dayItem.day} className="border border-slate-200 rounded-xl p-5 bg-slate-50/50">
              <div className="flex items-center justify-between mb-3 border-b border-slate-200/60 pb-2">
                <h3 className="font-bold text-slate-800 text-sm">
                  Hari ke-{dayItem.day}: <span className="text-blue-600 font-medium">{dayItem.theme}</span>
                </h3>
              </div>

              <div className="space-y-3">
                {dayItem.activities && dayItem.activities.map((act, idx) => (
                  <div key={idx} className="bg-white p-3.5 rounded-lg border border-slate-200/80 shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="flex items-start gap-3">
                      <span className="font-mono text-xs font-bold text-slate-500 bg-slate-100 px-2 py-1 rounded border border-slate-200 mt-0.5">
                        {act.time}
                      </span>
                      <div>
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="font-bold text-slate-800 text-sm">{act.poi_name}</span>
                          <span className="text-[10px] bg-slate-100 text-slate-600 px-2 py-0.5 rounded font-medium">
                            {act.category}
                          </span>
                        </div>
                        <p className="text-xs text-slate-600 mt-1 whitespace-pre-wrap">{act.description}</p>
                      </div>
                    </div>

                    {/* Menampilkan Skor Semantic Retrieval FAISS jika tersedia */}
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
          ))
        ) : (
          <div className="text-center py-8 text-slate-400 text-sm italic">
            Belum ada jadwal harian yang dimuat dari sistem backend.
          </div>
        )}
      </div>
    </div>
  );
}