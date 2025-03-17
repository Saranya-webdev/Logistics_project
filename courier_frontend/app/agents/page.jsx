"use client";

import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import useSWR from "swr";

const fetcher = (url) => fetch(url).then((res) => res.json());

const EntityList = dynamic(() => import('../components/entitylist'), { ssr: false });
const Bookingtable = dynamic(() => import('../components/Bookingtable'), { ssr: false });
const CombinedCharts = dynamic(() => import('../components/charts/combinedcharts'), { ssr: false });

const API_BASE = "http://127.0.0.1:8000/thisaiapi";

export default function Home() {
  const { data, error } = useSWR(`${API_BASE}/agents/agentsprofilelist/`, fetcher);

  const [selectedAgent, setSelectedAgent] = useState(null);
  const [bookingData, setBookingData] = useState([]);
  const [agentData, setAgentData] = useState(null);

  const fetchAgentData = async (agent) => {
    if (!agent?.agent_email) {
      console.error("No agent email provided");
      return;
    }
  
    const encodedEmail = encodeURIComponent(agent.agent_email);
  
    try {
      const profileRes = await fetch(`${API_BASE}/agents/${encodedEmail}/profile/`);
      const bookingRes = await fetch(`${API_BASE}/agents/${encodedEmail}/bookings/`);
  
      if (!profileRes.ok) {
        console.error("Agent profile fetch error:", await profileRes.text());
        return;
      }
      setAgentData(await profileRes.json());
  
      // Reset bookings before fetching new data
      setBookingData([]);
  
      if (!bookingRes.ok) {
        const errorText = await bookingRes.text();
        console.error("Booking fetch error:", errorText);
        
        // Handle "No bookings found" error gracefully
        if (errorText.includes("No bookings found")) {
          setBookingData([]);  // Ensure previous bookings are cleared
          return;
        }
  
        return;
      }
  
      const bookingData = await bookingRes.json();
      setBookingData(bookingData.bookings || []);
  
    } catch (error) {
      console.error("Network error fetching agent data:", error);
      setBookingData([]); // Ensure bookings reset on network errors
    }
  };
  
  useEffect(() => {
    if (data && data.length > 0) {
      const sortedAgents = data.sort((a, b) => a.agent_name.localeCompare(b.agent_name));
      const firstAgent = sortedAgents[0];
      setSelectedAgent(firstAgent);
      fetchAgentData(firstAgent);
    }
  }, [data]);

  const handleEntityClick = (agent) => {
    if (agent?.agent_email !== selectedAgent?.agent_email) {
      setSelectedAgent(agent);
      setAgentData(null);
      setBookingData([]);
      fetchAgentData(agent);
    }
  };

  if (error) return <div>Failed to load agents: {error.message}</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="flex bg-white h-[100%] w-[100%] rounded-[12px] p-4 gap-5">
        <EntityList
          endpoint={`${API_BASE}/agents/agentsprofilelist/`}
          entityType="agent"
          onEntityClick={handleEntityClick}
        />
        <div className="flex w-[100%] lg:w-[100%] lg:gap-2 md:w-[100%] sm:gap-4 h-[100%] md:flex-col overflow-y-auto no-scrollbar overflow-hidden md:gap-6 ">
        <CombinedCharts 
  entityType="agent" 
  entityName={selectedAgent?.agent_name || "Agent"} 
  selectedEntity={selectedAgent} 
/>


{selectedAgent?.agent_email ? (
  <Bookingtable selectedEntity={selectedAgent} bookings={bookingData} userType="agent" />
) : (
  <div>Loading Agent Data...</div>
)}
        </div>
      </div>
  );
}
