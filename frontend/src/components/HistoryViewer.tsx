"use client";

import React, { useState } from "react";
import ProfileCard from "./ProfileCard";
import ItineraryView from "./ItineraryView";

export default function HistoryViewer() {
  // Data simulasi interaktif untuk visualisasi frontend
  const [profileData] = useState({
    userId: "USR-8821",
    totalTrips: 4,
    profileSummary: "Pengguna menunjukkan konsistensi tinggi terhadap destinasi wisata alam pegunungan, pantai tropis, serta situs peninggalan sejarah kuno dengan preferensi gaya perjalanan moderat."
  });

  const [sampleItinerary] = useState({
    title: "Eksplorasi Budaya & Alam Nusantara",
    destination: "Yogyakarta & Sekitarnya",
    durationDays: 2,
    budget: "Menengah",
    schedule: [
      {
        day: 1,
        theme: "Jejak Peradaban & Sejarah",
        activities: [
          {
            time: "08:30 - 11:30",
            poi_name: "Candi Prambanan",
            category: "Sejarah & Budaya",
            description: "Kunjungan ke situs warisan dunia UNESCO dengan relief arsitektur Hindu klasik."
          },
          {
            time: "13:00 - 15:00",
            poi_name: "Keraton Yogyakarta",
            category: "Budaya",
            description: "Eksplorasi museum dan pusat kebudayaan Kesultanan."
          }
        ]
      },
      {
        day: 2,
        theme: "Panorama Alam Terbuka",
        activities: [
          {
            time: "08:00 - 11:00",
            poi_name: "Pantai Parangtritis",
            category: "Wisata Alam",
            description: "Menikmati lanskap pesisir selatan yang eksotis."
          }
        ]
      }
    ]
  });

  return (
    <div className="space-y-6">
      {/* Bagian Profil Implisit Hasil Kompresi */}
      <ProfileCard 
        userId={profileData.userId}
        totalTripsAnalyzed={profileData.totalTrips}
        preferenceProfile={profileData.profileSummary}
      />

      {/* Bagian Hasil Akhir Itinerary */}
      <ItineraryView 
        title={sampleItinerary.title}
        destination={sampleItinerary.destination}
        durationDays={sampleItinerary.durationDays}
        budget={sampleItinerary.budget}
        schedule={sampleItinerary.schedule}
      />
    </div>
  );
}