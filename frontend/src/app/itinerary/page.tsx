"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import HistoryViewer from "./HistoryViewer";
import "../globals.css";

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

interface ItineraryData {
  title: string;
  destination: string;
  duration_days: number;
  budget_level: string;
  generated_at: string;
  user_profile_summary: string;
  total_trips_analyzed?: number;
  days: DaySchedule[];
}

export default function ItineraryResultPage() {
  const [itineraryData, setItineraryData] = useState<ItineraryData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function fetchGeneratedItinerary() {
      try {
        setLoading(true);

        const activeDestination = localStorage.getItem("target_destination") || "Yogyakarta";
        const activeDuration = Number(localStorage.getItem("target_duration")) || 3;
        const activeBudget = localStorage.getItem("target_budget") || "Menengah";
        const activePreferences = localStorage.getItem("target_preferences") || "wisata alam dan sejarah";

        const response = await fetch("http://127.0.0.1:8000/api/v1/generator/generate", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            user_id: "user_thesis_123",
            query: `Buatkan itinerary liburan di ${activeDestination}`,
            destination: activeDestination,
            duration: activeDuration,
            budget: activeBudget,
            preferences: activePreferences
          }),
        });

        if (!response.ok) throw new Error(`Gagal mengambil data dari server (Status: ${response.status})`);

        const data = await response.json();

        if (data && data.status === "success") {
          setItineraryData({
            title: data.itinerary_title || `Rencana Perjalanan ${activeDestination}`,
            destination: data.destination || activeDestination,
            duration_days: data.duration || activeDuration,
            budget_level: data.budget || activeBudget,
            generated_at: new Date().toISOString().split('T')[0],
            user_profile_summary: data.query_profile || activePreferences,
            total_trips_analyzed: data.total_trips || 4,
            days: data.days && data.days.length > 0 ? data.days : [
              {
                day_number: 1,
                theme: "Hasil RAG & Retrieval FAISS",
                activities: data.raw_pois ? data.raw_pois.map((poi: any, idx: number) => ({
                  time: `08:00 - 11:00 (Sesi ${idx + 1})`,
                  poi_name: poi.name,
                  category: poi.city || "Rekomendasi Sistem",
                  description: poi.description,
                  similarity_score: poi.score || 0.8500
                })) : []
              }
            ]
          });
        } else {
          setError("Format respons backend tidak valid.");
        }
      } catch (err: any) {
        console.error("Fetch error:", err);
        setError("Gagal terhubung ke server backend FastAPI.");
      } finally {
        setLoading(false);
      }
    }

    fetchGeneratedItinerary();
  }, []);

  const handleSaveToDatabase = async () => {
    try {
      setSaving(true);
      const response = await fetch("http://127.0.0.1:8000/api/v1/generator/save", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "user_thesis_123",
          itinerary_content: itineraryData
        }),
      });

      if (!response.ok) throw new Error("Gagal menyimpan ke database.");
      alert("Berhasil! Itinerary telah disimpan ke database PostgreSQL.");
    } catch (err) {
      console.error(err);
      alert("Gagal menghubungi server untuk menyimpan data.");
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[400px]">
        <p className="text-blue-600 font-medium animate-pulse">Menyusun Itinerary dengan AI RAG & FAISS...</p>
      </div>
    );
  }

  if (error || !itineraryData) {
    return (
      <div className="max-w-md mx-auto mt-12 p-6 bg-red-50 border border-red-200 text-red-600 rounded-xl text-center">
        <p className="font-semibold">Terjadi Kesalahan</p>
        <p className="text-sm mt-1">{error || "Data tidak ditemukan."}</p>
        <Link href="/" className="mt-4 inline-block text-xs font-bold underline text-blue-600">
          Kembali ke Beranda
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Tombol Navigasi & Simpan */}
      <div className="flex items-center justify-between">
        <Link 
          href="/" 
          className="text-sm font-semibold text-blue-600 hover:text-blue-800 flex items-center gap-1 transition"
        >
          &larr; Buat Itinerary Baru
        </Link>
        <button
          onClick={handleSaveToDatabase}
          disabled={saving}
          className="bg-emerald-600 hover:bg-emerald-700 text-white font-medium px-4 py-2 rounded-lg text-sm transition shadow-sm disabled:bg-emerald-300 cursor-pointer"
        >
          {saving ? "Menyimpan..." : "Simpan ke Database"}
        </button>
      </div>

      {/* Memanggil HistoryViewer Secara Dinamis */}
      <HistoryViewer 
        userId="user_thesis_123"
        totalTrips={itineraryData.total_trips_analyzed || 4}
        profileSummary={itineraryData.user_profile_summary}
        destination={itineraryData.destination}
        title={itineraryData.title}
        durationDays={itineraryData.duration_days}
        budgetLevel={itineraryData.budget_level}
        days={itineraryData.days}
      />
    </div>
  );
}