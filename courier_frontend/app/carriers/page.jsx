"use client";

import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import useSWR from "swr";
import { FaEye } from "react-icons/fa";

const fetcher = (url) => fetch(url).then((res) => res.json());

const EntityList = dynamic(() => import('../components/entitylist'), { ssr: false });
const CombinedCharts = dynamic(() => import('../components/charts/combinedcharts'), { ssr: false });
const Bookingtable = dynamic(() => import('../components/Bookingtable'), { ssr: false });


const API_BASE = "http://127.0.0.1:8000/thisaiapi";

export default function Home() {
  const { data, error } = useSWR(`${API_BASE}/carriers/carriersprofilelist/`, fetcher);

  const [selectedcarrier, setSelectedcarrier] = useState(null);
  const [carrierData, setcarrierData] = useState(null);
  const [bookingData, setBookingData] = useState([]);

  const fetchcarrierData = async (carrier) => {
    if (!carrier?.carrier_email) {
      console.error("No carrier email provided");
      return;
    }
  
    const encodedEmail = encodeURIComponent(carrier.carrier_email);
    console.log("Fetching carrier profile for:", encodedEmail);
  
    try {
      const profileRes = await fetch(`${API_BASE}/carriers/${encodedEmail}/profile`);
  
      if (!profileRes.ok) {
        const errorText = await profileRes.text();
        console.error("Carrier profile fetch error:", errorText);
        return;
      }
  
      const carrierData = await profileRes.json();
      console.log("Carrier Data:", carrierData);
      setcarrierData(carrierData);
    } catch (error) {
      console.error("Network error fetching carrier data:", error);
    }
  };
  
  

  useEffect(() => {
    if (data && data.length > 0) {
      console.log("Fetched Carrier List:", data);
      
      const sortedcarriers = data.sort((a, b) => a.carrier_name.localeCompare(b.carrier_name));
      const firstcarrier = sortedcarriers[0];
      setSelectedcarrier(firstcarrier);
      fetchcarrierData(firstcarrier);
    }
  }, [data]);
  

  const handleEntityClick = (carrier) => {
    if (carrier?.carrier_email !== selectedcarrier?.carrier_email) {
      setSelectedcarrier(carrier);
      setcarrierData(null);
      setBookingData([]);
      fetchcarrierData(carrier);
    }
  };

  if (error) return <div>Failed to load carriers: {error.message}</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="flex bg-white h-[100%] w-[100%] rounded-[12px] p-4 gap-5">
        <EntityList
          endpoint={`${API_BASE}/carriers/carriersprofilelist/`}
          entityType="carrier"
          onEntityClick={handleEntityClick}
        />
        <div className="flex w-[100%] lg:w-[100%] lg:gap-2 md:w-[100%] sm:gap-4 h-[100%] md:flex-col overflow-y-auto no-scrollbar overflow-hidden md:gap-6">
        <CombinedCharts 
  entityType="carrier" 
  entityName={selectedcarrier?.carrier_name || "carrier"} 
  selectedEntity={selectedcarrier} 
/>
        

{selectedcarrier?.carrier_email ? (
  <Bookingtable selectedEntity={selectedcarrier} bookings={bookingData} userType="carrier" />
) : (
  <div>Loading Carrier Data...</div>
)}
        </div>
     
    </div>
  );
}