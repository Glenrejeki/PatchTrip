"use client";
import React, { useState } from "react";

export default function DashboardPage() {
  const [loading, setLoading] = useState(false);
  const [outputResult, setOutputResult] = useState<string | null>(null);
  
  // State form input sederhana untuk simulasi perencanaan
  const [formData, setFormData] = useState({
    location: "Yogyakarta",
    duration_days: 3,
    budget: "Menengah",
    user_profile_text: "Saya menyukai wisata alam pantai, candi bersejarah, dan kuliner lokal."
  });

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setOutputResult(null);

    try {
      // Simulasi panggilan API ke Backend FastAPI /api/v1/...
      // Pada implementasi riil, Anda bisa menyambungkan fetch ke endpoint FastAPI yang sudah dibuat
      setTimeout(() => {
        setOutputResult(
          `=== SIMULASI HASIL GENERASI PATCHTRIP ===\n` +
          `Destinasi: ${formData.location}\n` +
          `Durasi: ${formData.duration_days} Hari | Budget: ${formData.budget}\n\n` +
          `[Hari 1]\n- 09:00: Kunjungan ke Candi Prambanan (Sejarah & Budaya)\n- 13:00: Wisata Kuliner Gudeg Jogja\n\n` +
          `[Hari 2]\n- 08:30: Eksplorasi Pantai Parangtritis (Alam & Pantai)\n\n` +
          `Status: Itinerary berhasil disusun secara personal berdasarkan profil implisit pengguna.`
        );
        setLoading(false);
      }, 1500);
    } catch (err) {
      console.error(err);
      setOutputResult("Terjadi kesalahan saat menghubungi server backend.");
      setLoading(false);
    }
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
      {/* Kolom Kiri: Form Input Parameter Perjalanan */}
      <div className="lg:col-span-1 bg-white p-6 rounded-2xl shadow-sm border border-slate-200 h-fit">
        <h2 className="text-lg font-bold text-slate-800 mb-4">Buat Rencana Perjalanan</h2>
        <form onSubmit={handleGenerate} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-600 uppercase mb-1">Lokasi Tujuan</label>
            <input 
              type="text" 
              value={formData.location}
              onChange={(e) => setFormData({...formData, location: e.target.value})}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              required 
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-600 uppercase mb-1">Durasi (Hari)</label>
              <input 
                type="number" 
                value={formData.duration_days}
                onChange={(e) => setFormData({...formData, duration_days: Number(e.target.value)})}
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
              value={formData.user_profile_text}
              onChange={(e) => setFormData({...formData, user_profile_text: e.target.value})}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 outline-none"
              placeholder="Ceritakan preferensi perjalanan masa lalu Anda..."
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg text-sm transition shadow-sm disabled:bg-blue-300"
          >
            {loading ? "Memproses AI RAG..." : "Generate Itinerary"}
          </button>
        </form>
      </div>

      {/* Kolom Kanan: Tampilan Output Hasil Itinerary */}
      <div className="lg:col-span-2 bg-white p-6 rounded-2xl shadow-sm border border-slate-200 flex flex-col">
        <h2 className="text-lg font-bold text-slate-800 mb-4">Hasil Rekomendasi Itinerary</h2>
        <div className="flex-grow bg-slate-900 text-slate-100 p-4 rounded-xl font-mono text-sm overflow-x-auto min-h-[300px] flex items-center justify-center">
          {loading ? (
            <div className="text-blue-400 animate-pulse">Menjalankan Hierarchical Compression & Qwen3-8B RAG...</div>
          ) : outputResult ? (
            <pre className="whitespace-pre-wrap w-full text-left">{outputResult}</pre>
          ) : (
            <span className="text-slate-500">Belum ada data. Silakan isi form di samping dan klik tombol Generate.</span>
          )}
        </div>
      </div>
    </div>
  );
}