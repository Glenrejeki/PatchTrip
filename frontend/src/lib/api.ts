const API_BASE_URL = "http://localhost:8000/api/v1";

export async function generateItinerary(payload: {
  destination: string;
  duration: number;
  budget: string;
  preferences: string;
}) {
  const response = await fetch(`${API_BASE_URL}/generator/generate`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error("Gagal terhubung ke backend FastAPI.");
  }

  const data = await response.json();
  return data.itinerary; // Mengembalikan teks hasil RAG
}