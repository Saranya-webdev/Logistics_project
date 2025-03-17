"use client";

import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import Barchart from "../components/charts/Barchart";
import Doughnut from "../components/charts/Doughnut";

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
   
<div className=" h-[100%] w-[100%] rounded-[12px] p-4">
        
        <div className="flex w-[100%] lg:w-[100%] lg:gap-2 md:w-[100%] bg-white p-4 rounded-xl sm:gap-4 h-[100%] flex-col overflow-y-auto no-scrollbar overflow-hidden md:gap-6 ">
        <CombinedCharts entityType="booking" />

        <Bookingtable selectedEntity={{ bookings: bookingData }} userType="booking" className="max-w-full overflow-hidden"/>
      </div>
    </div>
  );
}






