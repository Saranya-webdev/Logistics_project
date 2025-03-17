"use client";

import React, { useState, useEffect, Suspense } from "react";
import dynamic from "next/dynamic";
import { useSearchParams } from "next/navigation";  
import { FaPlus } from "react-icons/fa";

const CreateQuotation = dynamic(() => import("../components/CreateQuotation/CreateQuotation"), { ssr: false });
const Bookingtable = dynamic(() => import("../components/Bookingtable"), { ssr: false });

export default function QuotationContent() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <QuotationContentComponent />
    </Suspense>
  );
}

function QuotationContentComponent() {
  const [quotationData, setQuotationData] = useState([]);
  const [showCreateModal, setShowCreateModal] = useState(false);

  const searchParams = useSearchParams(); 
  const selectedEntityParam = searchParams.get("selectedEntity");
  const userType = searchParams.get("userType");


  let selectedEntity = { quotations: [] };
  try {
    selectedEntity = selectedEntityParam ? JSON.parse(selectedEntityParam) : { quotations: [] };
  } catch (error) {
    console.error("Invalid selectedEntity JSON:", error);
  }

  // Fetch Quotation Data
  const fetchQuotationData = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/thisaiapi/quotations/allquotations");
      console.log("API Response Status:", response.status);
      const data = await response.json();
      console.log("Full API Response:", data);

      setQuotationData(
        Array.isArray(data)
          ? data.map(quotation => ({
              ...quotation,
              from_pincode: quotation.from_pincode ?? "",
              to_pincode: quotation.to_pincode ?? "",
              package_count: quotation.package_count ?? 1,
              pickup_date: quotation.pickup_date ?? "",
              pickup_time: quotation.pickup_time ?? "",
            }))
          : []
      );
    } catch (error) {
      console.error("Error fetching quotations:", error);
      setQuotationData([]);
    }
  };

  useEffect(() => {
    fetchQuotationData();
  }, [selectedEntityParam, userType]); //  Re-fetch when params change

  useEffect(() => {
    console.log("Updated Quotation Data:", quotationData);
  }, [quotationData]);

  return (
    <div className="flex bg-white h-[100%] w-[100%] rounded-[12px] p-4 gap-5">
      <div className="flex w-full lg:gap-2 md:w-full sm:gap-4 h-full lg:flex-col md:flex-col md:overflow-y-auto md:gap-10 overflow-hidden">
        
        {/* Create Quotation Button */}
        <div className="flex justify-end mb-4">
          <button
            className="btn mt-6 rounded-xl px-8 py-3 text-lg text-center bg-blue-500 text-white w-[130px]"
            onClick={() => setShowCreateModal(true)}
          >
            <FaPlus /> Create
          </button>
        </div>

        {/* Quotation Table */}
        <Bookingtable
          selectedEntity={selectedEntity}
          userType={userType || "quotation"}
        />

        {/* Overlay and Modal */}
        {showCreateModal && (
          <>
            {/* Blur Background */}
            <div className="fixed inset-0 bg-black bg-opacity-40 backdrop-blur-sm z-40" onClick={() => setShowCreateModal(false)}></div>

            {/* Modal */}
            <div className="fixed inset-0 flex items-center justify-center z-50">
              <CreateQuotation onClose={() => setShowCreateModal(false)} />
            </div>
          </>
        )}
      </div>
    </div>
  );
}
