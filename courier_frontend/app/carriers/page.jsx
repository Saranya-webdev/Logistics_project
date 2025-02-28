"use client";

import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import useSWR from "swr";
import { FaEye } from "react-icons/fa";

const fetcher = (url) => fetch(url).then((res) => res.json());

const EntityList = dynamic(() => import('../components/entitylist'), { ssr: false });
const CombinedCharts = dynamic(() => import('../components/charts/combinedcharts'), { ssr: false });

const API_BASE = "http://127.0.0.1:8000/thisaiapi";

export default function Home() {
  const { data, error } = useSWR(`${API_BASE}/carriers/carriersprofilelist/`, fetcher);

  const [selectedcarrier, setSelectedcarrier] = useState(null);
//   const [bookingData, setBookingData] = useState([]);
  const [carrierData, setcarrierData] = useState(null);

  const fetchcarrierData = async (carrier) => {
    if (!carrier?.carrier_email) {
      console.error("No carrier email provided");
      return;
    }
  
    const encodedEmail = encodeURIComponent(carrier.carrier_email);
  
    try {
      const profileRes = await fetch(`${API_BASE}/carriers/${encodedEmail}/profile/`);
      
  
      if (!profileRes.ok) {
        const errorText = await profileRes.text();
        console.error("carrier profile fetch error:", errorText);
        return;
      }
      setcarrierData(await profileRes.json());
    } catch (error) {
      console.error("Network error fetching carrier data:", error);
    }
  };
  

  useEffect(() => {
    if (data && data.length > 0) {
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
    <div className="transition-all duration-300 flex w-full h-screen relative bg-[#f3f3f3] overflow-y-auto">
      <div className="flex bg-white w-full h-full rounded-[12px] p-4 gap-5 overflow-y-auto">
        <EntityList
          endpoint={`${API_BASE}/carriers/carriersprofilelist/`}
          entityType="carrier"
          onEntityClick={handleEntityClick}
        />
        <div className="flex w-full lg:gap-2 md:w-full sm:gap-4 h-full lg:flex-col md:flex-col md:overflow-y-auto md:gap-10 overflow-hidden">
        <CombinedCharts 
  entityType="carrier" 
  entityName={selectedcarrier?.carrier_name || "carrier"} 
  selectedEntity={selectedcarrier} 
/>
        </div>
      </div>
    </div>
  );
}