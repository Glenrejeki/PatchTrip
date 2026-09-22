"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";

export default function DashboardPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    destination: "",
    duration: 3,
    budget: "Menengah",
    preferences: ""
  });

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      // Simpan parameter input ke localStorage agar bisa diakses dinamis oleh halaman hasil/itinerary
      localStorage.setItem("target_destination", formData.destination);
      localStorage.setItem("target_duration", String(formData.duration));
      localStorage.setItem("target_budget", formData.budget);
      localStorage.setItem("target_preferences", formData.preferences);

      // Panggil endpoint backend FastAPI untuk memastikan koneksi hidup sebelum navigasi
      const response = await fetch("http://127.0.0.1:8000/api/v1/generator/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_id: "user_thesis_123",
          query: `Buatkan itinerary liburan di ${formData.destination}`,
          destination: formData.destination,
          duration: Number(formData.duration),
          budget: formData.budget,
          preferences: formData.preferences
        }),
      });

      if (!response.ok) throw new Error("Gagal terhubung ke backend FastAPI");

      // Arahkan ke halaman itinerary hasil generate
      router.push("/itinerary");
    } catch (err) {
      console.error(err);
      alert("Gagal terhubung ke server backend FastAPI. Pastikan server aktif di port 8000.");
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto bg-white p-8 rounded-2xl shadow-sm border border-slate-200">
      <h2 className="text-xl font-bold text-slate-800 mb-6">Buat Rencana Perjalanan AI</h2>
      <form onSubmit={handleGenerate} className="space-y-4">
        <div>
          <label className="block text-xs font-semibold text-slate-600 uppercase mb-1">Lokasi Tujuan</label>
          <input 
            type="text" 
            value={formData.destination}
            onChange={(e) => setFormData({...formData, destination: e.target.value})}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
            placeholder="Contoh: Yogyakarta"
            required 
          />
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <label className="block text-xs font-semibold text-slate-600 uppercase mb-1">Durasi (Hari)</label>
            <input 
              type="number" 
              value={formData.duration}
              onChange={(e) => setFormData({...formData, duration: Number(e.target.value)})}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              min={1} max={14}
              required 
            />
          </div>
          <div>
            <label className="block text-xs font-semibold text-slate-600 uppercase mb-1">Anggaran</label>
            <select 
              value={formData.budget}
              onChange={(e) => setFormData({...formData, budget: e.target.value})}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none bg-white"
            >
              <option value="Hemat">Hemat</option>
              <option value="Menengah">Menengah</option>
              <option value="Mewah">Mewah</option>
            </select>
          </div>
        </div>

        <div>
          <label className="block text-xs font-semibold text-slate-600 uppercase mb-1">Preferensi & Catatan Pengguna</label>
          <textarea 
            rows={4}
            value={formData.preferences}
            onChange={(e) => setFormData({...formData, preferences: e.target.value})}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
            placeholder="Ceritakan preferensi wisata Anda..."
            required
          />
        </div>

        <button 
          type="submit" 
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg text-sm transition shadow-sm disabled:bg-blue-300 cursor-pointer"
        >
          {loading ? "Memproses RAG & FAISS..." : "Generate Itinerary"}
        </button>
      </form>
    </div>
  );
}