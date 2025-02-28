"use client";

import React, { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import useSWR from "swr";
import { FaEye } from "react-icons/fa";

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
    <div className="transition-all duration-300 flex w-full h-screen relative bg-[#f3f3f3] overflow-y-auto">
      <div className="flex bg-white w-full h-full rounded-[12px] p-4 gap-5 overflow-y-auto">
        <EntityList
          endpoint={`${API_BASE}/agents/agentsprofilelist/`}
          entityType="agent"
          onEntityClick={handleEntityClick}
        />
        <div className="flex w-full lg:gap-2 md:w-full sm:gap-4 h-full lg:flex-col md:flex-col md:overflow-y-auto md:gap-10 overflow-hidden">
        <CombinedCharts 
  entityType="agent" 
  entityName={selectedAgent?.agent_name || "Agent"} 
  selectedEntity={selectedAgent} 
/>


          <Bookingtable selectedEntity={selectedAgent} userType="agent" bookings={bookingData}/>
        </div>
      </div>
    </div>
  );
}


// for service.jsx's page.jsx
// "use client";

// import React, { useState, useEffect } from "react";
// import dynamic from "next/dynamic";
// import useSWR from "swr";
// import { fetchAgentProfile, fetchAgentBookings } from "../service";

// const EntityList = dynamic(() => import('../components/entitylist'), { ssr: false });
// const Bookingtable = dynamic(() => import('../components/Bookingtable'), { ssr: false });
// const CombinedCharts = dynamic(() => import('../components/charts/combinedcharts'), { ssr: false });

// const API_BASE = "http://127.0.0.1:8000/thisaiapi";

// const fetcher = (url) => fetch(`${API_BASE}/${url}`).then((res) => res.json());

// export default function Home() {
//   const { data, error } = useSWR('agents/agentsprofilelist/', fetcher);

//   const [selectedAgent, setSelectedAgent] = useState(null);
//   const [bookingData, setBookingData] = useState([]);
//   const [agentData, setAgentData] = useState(null);

//   const fetchAgentData = async (agent) => {
//     if (!agent?.agent_email) {
//       console.error("No agent email provided");
//       return;
//     }
  
//     try {
//       const profileData = await fetchAgentProfile(agent.agent_email);
//       setAgentData(profileData);
//     } catch (error) {
//       console.error("Failed to fetch agent data:", error);
//     }
//   };
  

//   useEffect(() => {
//     if (data && data.length > 0) {
//       const sortedAgents = data.sort((a, b) => a.agent_name.localeCompare(b.agent_name));
//       const firstAgent = sortedAgents[0];
//       setSelectedAgent(firstAgent);
//       fetchAgentData(firstAgent);
//     }
//   }, [data]);

//   const handleEntityClick = (agent) => {
//     if (agent?.agent_email !== selectedAgent?.agent_email) {
//       setSelectedAgent(agent);
//       setAgentData(null);
//       setBookingData([]);
//       fetchAgentData(agent);
//     }
//   };

//   if (error) return <div>Failed to load agents: {error.message}</div>;
//   if (!data) return <div>Loading...</div>;

//   return (
//     <div className="transition-all duration-300 flex w-full h-screen relative bg-[#f3f3f3] overflow-y-auto">
//       <div className="flex bg-white w-full h-full rounded-[12px] p-4 gap-5 overflow-y-auto">
//         <EntityList
//           endpoint="agents/agentsprofilelist/"
//           entityType="agent"
//           onEntityClick={handleEntityClick}
//         />
//         <div className="flex w-full lg:gap-2 md:w-full sm:gap-4 h-full lg:flex-col md:flex-col md:overflow-y-auto md:gap-10 overflow-hidden">
//           <CombinedCharts 
//             entityType="agent" 
//             entityName={selectedAgent?.agent_name || "Agent"} 
//             selectedEntity={selectedAgent} 
//           />
//           <Bookingtable selectedEntity={selectedAgent} userType="agent" bookings={bookingData} />
//         </div>
//       </div>
//     </div>
//   );
// }