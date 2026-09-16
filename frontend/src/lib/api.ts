import axios, { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from "axios";

// Menentukan URL dasar backend (mengambil dari environment variable Next.js atau fallback ke localhost:8000)
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

/**
 * Konfigurasi utama instance Axios untuk komunikasi frontend dan backend PatchTrip.
 */
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // Batas waktu tunggu (timeout) 30 detik untuk proses AI RAG yang berat
  headers: {
    "Content-Type": "application/json",
    "Accept": "application/json",
  },
});

// Interceptor Request: Dijalankan sebelum permintaan dikirim ke backend
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Anda dapat menyisipkan token autentikasi (Bearer Token) di sini jika diperlukan nanti
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor Response: Dijalankan saat menerima respons dari backend
apiClient.interceptors.response.use(
  (response: AxiosResponse) => {
    return response;
  },
  (error) => {
    // Penanganan terpusat untuk error jaringan atau respons server
    const errorMessage =
      error.response?.data?.detail ||
      error.message ||
      "Terjadi kesalahan pada server PatchTrip.";
    
    console.error("[API Error Interceptor]:", errorMessage);
    return Promise.reject(new Error(errorMessage));
  }
);

/**
 * Kumpulan fungsi helper untuk mempermudah pemanggilan endpoint backend PatchTrip
 */
export const patchTripApi = {
  // 1. Endpoint Kompresi Hierarkis (Hierarchical Patch Compression)
  compressHistory: async (userId: string, rawTrips: any[]) => {
    const response = await apiClient.post("/compression/compress-history", {
      user_id: userId,
      raw_trips: rawTrips,
    });
    return response.data;
  },

  // 2. Endpoint Pencarian Semantik POI (Semantic Dense Retrieval - BGE-M3 & FAISS)
  semanticSearch: async (userPreferenceProfile: string, topK: number = 5) => {
    const response = await apiClient.post("/retrieval/semantic-search", {
      user_preference_profile: userPreferenceProfile,
      top_k: topK,
    });
    return response.data;
  },

  // 3. Endpoint Generasi RAG Itinerary (LangChain & Qwen3-8B)
  generateItinerary: async (userPreferenceProfile: string, retrievedPois: any[], constraints: any) => {
    const response = await apiClient.post("/generator/generate-itinerary", {
      user_preference_profile: userPreferenceProfile,
      retrieved_pois: retrievedPois,
      constraints: constraints,
    });
    return response.data;
  },
};