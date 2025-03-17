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
  const { data, error } = useSWR(`${API_BASE}/customers/customerprofilelist/`, fetcher);
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [bookingData, setBookingData] = useState([]);
  const [customerData, setCustomerData] = useState(null);

  const fetchCustomerData = async (customer) => {
    if (!customer?.customer_email) {
      console.error("No customer email provided");
      return;
    }

    const encodedEmail = encodeURIComponent(customer.customer_email);
    
    try {
      const [profileRes, bookingRes] = await Promise.all([
        fetch(`${API_BASE}/customers/customer/${encodedEmail}/`),
        fetch(`${API_BASE}/customers/${encodedEmail}/bookinglist/`)
      ]);

      if (profileRes.ok) {
        setCustomerData(await profileRes.json());
      } else {
        console.error("Failed to fetch customer profile");
      }

      if (bookingRes.ok) {
        const bookingData = await bookingRes.json();
        setBookingData(Array.isArray(bookingData?.bookings) ? bookingData.bookings : []);

      } else {
        console.error("Failed to fetch booking data");
      }
    } catch (error) {
      console.error("Failed to fetch customer data:", error);
    }
  };

  useEffect(() => {
    if (data && data.length > 0) {
      const sortedCustomers = data.sort((a, b) => a.customer_name.localeCompare(b.customer_name));
      const firstCustomer = sortedCustomers[0];
      setSelectedCustomer(firstCustomer);
      fetchCustomerData(firstCustomer);
    }
  }, [data]);

  const handleEntityClick = (customer) => {
    if (customer?.customer_email !== selectedCustomer?.customer_email) {
      setSelectedCustomer(customer);
      setCustomerData(null);
      setBookingData([]);
      fetchCustomerData(customer);
    }
  };

  if (error) return <div>Failed to load customers: {error.message}</div>;
  if (!data) return <div>Loading...</div>;

  return (
    <div className="flex bg-white h-[100%] w-[100%] rounded-[12px] p-4 gap-5 ">
        <EntityList
          endpoint={`${API_BASE}/customers/customerprofilelist/`}
          entityType="customer"
          onEntityClick={handleEntityClick}
        />
        <div className="flex w-[100%] lg:w-[100%] lg:gap-2 md:w-[100%] sm:gap-4 h-[100%] md:flex-col overflow-y-auto no-scrollbar overflow-hidden md:gap-6 ">
        <CombinedCharts 
  entityType="customer" 
  entityName={selectedCustomer?.customer_name || "Customer"} 
  selectedEntity={selectedCustomer} 
/>
          {selectedCustomer?.customer_email ? (
  <Bookingtable selectedEntity={selectedCustomer} bookings={bookingData} userType="customer" />
) : (
  <div>Loading Customer Data...</div>
)}

        </div>
      </div>
   
  );
}