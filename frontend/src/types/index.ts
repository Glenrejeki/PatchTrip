/**
 * Definisi TypeScript Interfaces & Types untuk Sistem PatchTrip Frontend
 */

// ==========================================
// 1. DATA PENGGUNA & RIWAYAT PERJALANAN
// ==========================================

export interface TripItem {
    name: string;
    category: string;
    note?: string;
  }
  
  export interface HistoricalTrip {
    trip_id: string;
    trip_name: string;
    date?: string;
    items: TripItem[];
  }
  
  export interface UserHistoryPayload {
    user_id: string;
    total_trips: number;
    historical_trips: HistoricalTrip[];
  }
  
  // ==========================================
  // 2. MODUL HIERARCHICAL COMPRESSION
  // ==========================================
  
  export interface CompressionRequest {
    user_id: string;
    raw_trips: Record<string, any>[];
  }
  
  export interface CompressionResponse {
    status: string;
    message: string;
    user_id: string;
    preference_profile: string; // Hasil User Preference Profile (Level 3)
  }
  
  // ==========================================
  // 3. MODUL SEMANTIC RETRIEVAL (POI)
  // ==========================================
  
  export interface POIItem {
    id?: number;
    poi_id?: number;
    name: string;
    category?: string;
    description?: string;
    location?: string;
    latitude?: number;
    longitude?: number;
    similarity_score?: number; // Skor kemiripan dari FAISS ANN search
  }
  
  export interface RetrievalRequest {
    user_preference_profile: string;
    top_k?: number;
  }
  
  export interface RetrievalResponse {
    status: string;
    message: string;
    query_profile: string;
    total_retrieved: number;
    candidates: POIItem[];
  }
  
  // ==========================================
  // 4. MODUL RAG & GENERATOR (ITINERARY)
  // ==========================================
  
  export interface TravelConstraints {
    location: string;
    duration_days: number;
    budget: "Hemat" | "Menengah" | "Mewah" | string;
  }
  
  export interface GenerationRequest {
    user_preference_profile: string;
    retrieved_pois: POIItem[];
    constraints: TravelConstraints;
  }
  
  export interface GenerationResponse {
    status: string;
    message: string;
    itinerary: string; // Teks lengkap hasil keluaran model Qwen3-8B
  }
  
  // ==========================================
  // 5. STRUKTUR RENDER ITINERARY UI
  // ==========================================
  
  export interface ItineraryActivity {
    time: string;
    poi_name: string;
    category: string;
    description: string;
    similarity_score?: number;
  }
  
  export interface DaySchedule {
    day_number: number;
    theme: string;
    activities: ItineraryActivity[];
  }
  
  export interface StructuredItinerary {
    title: string;
    destination: string;
    duration_days: number;
    budget_level: string;
    generated_at?: string;
    user_profile_summary: string;
    days: DaySchedule[];
  }