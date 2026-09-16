"use client";

import React, { useState } from "react";
import Link from "next/link";

export default function ItineraryResultPage() {
  // Simulasi data itinerary hasil generate dari backend RAG & Qwen3-8B
  const [itineraryData, setItineraryData] = useState({
    title: "Eksplorasi Budaya & Alam Yogyakarta",
    destination: "Yogyakarta, Indonesia",
    duration_days: 2,
    budget_level: "Menengah",
    generated_at: "2026-06-06",
    user_profile_summary: "Pecinta wisata alam pantai, candi bersejarah, dan kuliner tradisional.",
    days: [
      {
        day_number: 1,
        theme: "Jejak Sejarah & Budaya Klasik",
        activities: [
          {
            time: "08:30 - 11:30",
            poi_name: "Candi Prambanan",
            category: "Sejarah & Budaya",
            description: "Menjelajahi kompleks candi Hindu terbesar yang kaya akan relief bersejarah.",
            similarity_score: 0.8921
          },
          {
            time: "12:30 - 14:00",
            poi_name: "Sentra Kuliner Gudeg Yu Djum",
            category: "Kuliner Lokal",
            description: "Menikmati makan siang khas tradisional Yogyakarta.",
            similarity_score: 0.8450
          },
          {
            time: "15:30 - 18:00",
            poi_name: "Keraton Yogyakarta",
            category: "Budaya & Edukasi",
            description: "Mengunjungi istana resmi Kesultanan Ngayogyakarta Hadiningrat.",
            similarity_score: 0.8210
          }
        ]
      },
      {
        day_number: 2,
        theme: "Eksplorasi Keindahan Pesisir Selatan",
        activities: [
          {
            time: "08:00 - 11:00",
            poi_name: "Pantai Parangtritis",
            category: "Wisata Alam & Pantai",
            description: "Menikmati pemandangan laut lepas Samudra Hindia dan panorama bukit pasir.",
            similarity_score: 0.9102
          },
          {
            time: "13:00 - 15:00",
            poi_name: "Hutan Pinus Mangunan",
            category: "Wisata Alam",
            description: "Menghirup udara sejuk di kawasan hutan pinus dataran tinggi.",
            similarity_score: 0.8655
          }
        ]
      }
    ]
  });

  const handleSaveToDatabase = () => {
    alert("Berhasil! Itinerary telah disimpan ke riwayat akun database PostgreSQL Anda.");
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Tombol Kembali & Aksi */}
      <div className="flex items-center justify-between">
        <Link 
          href="/" 
          className="text-sm font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1 transition"
        >
          &larr; Buat Itinerary Baru
        </Link>
        <button
          onClick={handleSaveToDatabase}
          className="bg-emerald-600 hover:bg-emerald-700 text-white font-medium px-4 py-2 rounded-lg text-sm transition shadow-sm"
        >
          Simpan ke Database
        </button>
      </div>

      {/* Header Ringkasan Itinerary */}
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <span className="bg-blue-100 text-blue-700 text-xs font-bold px-2.5 py-1 rounded-full uppercase">
              {itineraryData.destination}
            </span>
            <h1 className="text-2xl font-black text-slate-800 mt-2">{itineraryData.title}</h1>
            <p className="text-sm text-slate-500 mt-1">
              Durasi: <span className="font-semibold text-slate-700">{itineraryData.duration_days} Hari</span> | 
              Budget: <span className="font-semibold text-slate-700">{itineraryData.budget_level}</span>
            </p>
          </div>
          <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 max-w-xs text-xs text-slate-600">
            <span className="font-bold block text-slate-700 mb-1">Profil Implisit Pengguna:</span>
            {itineraryData.user_profile_summary}
          </div>
        </div>
      </div>

      {/* Daftar Jadwal Harian (Day-by-Day Timeline) */}
      <div className="space-y-6">
        {itineraryData.days.map((day) => (
          <div key={day.day_number} className="bg-white p-6 rounded-2xl shadow-sm border border-slate-200">
            <div className="border-b border-slate-100 pb-3 mb-4">
              <span className="text-xs font-bold uppercase tracking-wider text-blue-600">Hari ke-{day.day_number}</span>
              <h2 className="text-lg font-bold text-slate-800">{day.theme}</h2>
            </div>

            <div className="space-y-4">
              {day.activities.map((act, index) => (
                <div key={index} className="flex gap-4 p-4 rounded-xl bg-slate-50 border border-slate-100 hover:border-slate-200 transition">
                  <div className="font-mono text-xs font-bold text-slate-500 bg-white px-2.5 py-1.5 rounded-lg border border-slate-200 h-fit">
                    {act.time}
                  </div>
                  <div className="flex-grow">
                    <div className="flex items-center justify-between">
                      <h3 className="font-bold text-slate-800">{act.poi_name}</h3>
                      <span className="text-[10px] font-medium bg-slate-200 text-slate-700 px-2 py-0.5 rounded">
                        {act.category}
                      </span>
                    </div>
                    <p className="text-sm text-slate-600 mt-1">{act.description}</p>
                    <div className="text-[11px] text-slate-400 mt-2 font-mono">
                      Skor Kedekatan Semantic Retrieval: {act.similarity_score}
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