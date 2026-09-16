import os
from typing import List, Dict, Any
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class RAGService:
    def __init__(self):
        # Mengambil konfigurasi model LLM dari environment variables
        self.model_name = os.getenv("LLM_MODEL_NAME", "Qwen/Qwen2.5-7B-Instruct")
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """
        Inisialisasi Large Language Model (LLM) Qwen menggunakan LangChain.
        Dapat dihubungkan ke endpoint API lokal (seperti vLLM/Ollama) atau HuggingFace pipeline.
        """
        try:
            # Placeholder inisialisasi LLM lokal (bisa disesuaikan dengan pipeline/klien model Anda)
            return None
        except Exception as e:
            print(f"Gagal menginisialisasi LLM: {e}")
            return None

    def generate_itinerary(self, user_profile: str, pois: List[Dict[str, Any]], constraints: Dict[str, Any]) -> str:
        """
        Melakukan Retrieval-Augmented Generation (RAG):
        Menggabungkan profil preferensi implisit, kandidat destinasi hasil semantic retrieval,
        serta batasan perjalanan (budget, durasi) ke dalam prompt untuk memandu penalaran LLM.
        """
        # Memformat daftar kandidat POI agar terstruktur dan mudah dibaca oleh LLM
        formatted_pois = "\n".join([
            f"- {p.get('name')} ({p.get('category')}): {p.get('description')} [Skor Kemiripan: {p.get('similarity_score', 0):.4f}]"
            for p in pois
        ])

        # Ekstraksi batasan perjalanan (constraints)
        budget = constraints.get("budget", "Standar")
        duration = constraints.get("duration_days", 3)
        location = constraints.get("location", "Destinasi Wisata")

        # Template Prompt untuk memastikan hasil memenuhi aspek feasibility, rationality, dan personalization
        template = """
        Anda adalah sistem asisten perencana perjalanan wisata profesional berbasis AI (PatchTrip). 
        Tugas Anda adalah menyusun rencana perjalanan (itinerary) yang layak (feasible), rasional secara spasial-temporal (rational), 
        dan sangat personal (personalized) berdasarkan data berikut[cite: 1, 3]:

        [PROFIL PREFERENSI IMPLISIT PENGGUNA]
        {user_profile}

        [BATASAN PERJALANAN (CONSTRAINTS)]
        - Lokasi Tujuan: {location}
        - Durasi Perjalanan: {duration} Hari
        - Kategori Anggaran: {budget}

        [KANDIDAT DESTINASI PILIHAN (HASIL SEMANTIC RETRIEVAL)]
        {formatted_pois}

        Instruksi Pembuatan:
        1. Pilih dan susun destinasi dari daftar kandidat di atas ke dalam jadwal harian (Hari 1 sampai Hari {duration}).
        2. Pastikan urutan kunjungan koheren secara geografis (efisien jarak/waktu tempuh) dan masuk akal.
        3. Sesuaikan pilihan aktivitas dengan profil preferensi jangka panjang pengguna dan batasan anggaran.
        4. Sajikan keluaran dalam format teks Markdown yang terstruktur dan rapi.

        Rencana Perjalanan (Itinerary):
        """

        prompt = PromptTemplate(
            input_variables=["user_profile", "location", "duration", "budget", "formatted_pois"],
            template=template
        )

        # Eksekusi rantai RAG (RAG Chain) menggunakan LangChain jika model LLM aktif
        if self.llm is not None:
            chain = prompt | self.llm | StrOutputParser()
            result = chain.invoke({
                "user_profile": user_profile,
                "location": location,
                "duration": duration,
                "budget": budget,
                "formatted_pois": formatted_pois
            })
            return result
        else:
            # Fallback struktur template prompt apabila LLM lokal belum dihubungkan secara aktif
            return (
                f"[SIMULASI RAG PIPELINE LANGCHAIN BERHASIL]\n"
                f"--------------------------------------------------\n"
                f"Lokasi Target: {location} | Durasi: {duration} Hari | Budget: {budget}\n"
                f"Jumlah Kandidat POI Dimasukkan ke Konteks: {len(pois)}\n\n"
                f"--- PRATINJAU PROMPT RAG YANG DISIAPKAN ---\n"
                f"Profil Pengguna: {user_profile[:120]}...\n"
                f"Destinasi Teratas: {pois[0]['name'] if pois else 'Tidak ada'}"
            )