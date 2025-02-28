"use client";

import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";

const Bookingtable = dynamic(() => import("../components/Bookingtable"), { ssr: false });
const CombinedCharts = dynamic(() => import("../components/charts/combinedcharts"), { ssr: false });

export default function BookingPage() {
  const [bookingData, setBookingData] = useState([]);

  const fetchBookingData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/thisaiapi/bookings/allbookingslist/");
      const data = await response.json();
      console.log("API Response:", data); // Check actual response structure
      setBookingData(Array.isArray(data) ? data : data.bookings || []);
    } catch (error) {
      console.error("Network error fetching booking data:", error);
      setBookingData([]);
    }
  };
  

  useEffect(() => {
    fetchBookingData();
  }, []);

  return (
   
<div className="transition-all duration-300 flex w-full h-screen relative bg-[#f3f3f3] overflow-y-auto">
      <div className="flex bg-white w-full h-full rounded-[12px] p-4 gap-5 overflow-y-auto">
        
        <div className="flex w-full lg:gap-2 md:w-full sm:gap-4 h-full lg:flex-col md:flex-col md:overflow-y-auto md:gap-10 overflow-hidden">
        <CombinedCharts entityType="booking" />


        <Bookingtable selectedEntity={{ bookings: bookingData }} userType="booking" />
        </div>
      </div>
    </div>
  );
}






