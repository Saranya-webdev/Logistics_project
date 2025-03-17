"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ParentOverlayManager from "@/app/components/CreateBookings/CreateBooking";


const QuotationReview = ({ selectedQuotation,onClose, formData: initialFormData }) => {
  const router = useRouter();
  const [localFormData, setLocalFormData] = useState(initialFormData || {});
  const [isLoading, setIsLoading] = useState(false);
  const [showOverlay, setShowOverlay] = useState(false); 
  const [currentStep, setCurrentStep] = useState(1);
  const [showBookingFlow, setShowBookingFlow] = useState(false);


  useEffect(() => {
    if (!initialFormData) {
      const storedFormData = localStorage.getItem("formData");
      console.log("Stored FormData:", storedFormData);
      if (storedFormData) {
        setLocalFormData(JSON.parse(storedFormData));
      }
    } else {
      setLocalFormData(initialFormData);
    }
  }, [initialFormData]);


  const handleProceedToBooking = () => {
    console.log("Proceeding with Quotation:", selectedQuotation);
    setShowBookingFlow(true);
  };
  

  // Ensure package details are properly structured
  useEffect(() => {
    if (localFormData?.package_count > 0) {
      setLocalFormData((prevData) => ({
        ...prevData,
        package_details: Array.from(
          { length: prevData.package_count || 0 },
          (_, index) => prevData?.package_details?.[index] ?? {
            length: "",
            width: "",
            height: "",
            weight: "",
            package_type: "",
          }
        ),
      }));
    }
  }, [localFormData?.package_count]);
  

  const handleFinalSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    if (!localFormData) {
      alert("No quotation data found.");
      setIsLoading(false);
      return;
    }

    // Construct the API request payload with corrected structure
    const transformedData = {
      customer_id: localFormData.customer_id || 138,
      ship_to_address: {
        to_name: localFormData.ship_to_address?.Name || "-",
        to_mobile: localFormData.ship_to_address?.Mobile || "-",
        to_email: localFormData.ship_to_address?.Email || "-",
        to_address: localFormData.ship_to_address?.Address || "-",
        to_city: localFormData.ship_to_address?.City || "-",
        to_state: localFormData.ship_to_address?.StateProvinceCode || "-",
        to_pincode: localFormData.ship_to_address?.PostalCode || "-",
        to_country: localFormData.ship_to_address?.CountryCode || "-",
      },
      ship_from_address: {
        from_name: localFormData.ship_from_address?.Name || "-",
        from_mobile: localFormData.ship_from_address?.Mobile || "-",
        from_email: localFormData.ship_from_address?.Email || "-",
        from_address: localFormData.ship_from_address?.Address || "-",
        from_city: localFormData.ship_from_address?.City || "-",
        from_state: localFormData.ship_from_address?.StateProvinceCode || "-",
        from_pincode: localFormData.ship_from_address?.PostalCode || "-",
        from_country: localFormData.ship_from_address?.CountryCode || "-",
      },
      pickup_date: localFormData.pickup_date || "",
      pickup_time: localFormData.pickup_time || "",

      package_details: localFormData.package_details.map((item) => ({
        carrier_name: localFormData?.selectedRate?.carrier_name || "",
        service_code: localFormData?.selectedRate?.service_code || "",
        carrier_plan: localFormData?.selectedRate?.carrier_plan || "",
        package_count: localFormData.package_count || 1,
        est_cost: localFormData?.selectedRate?.total_charges || 50.0,
        total_cost: localFormData?.selectedRate?.total_charges || 50.0,
        est_delivery_date: localFormData?.selectedRate?.estimated_arrival_date
          ? new Date(localFormData.selectedRate.estimated_arrival_date + " UTC")
              .toISOString()
              .split("T")[0]
          : "",
     })),
     

      booking_items: localFormData.package_details.map((item) => ({
        weight: item.weight || 7,
        length: item.length || 20,
        width: item.width || 10,
        height: item.height || 10,
        package_type: item.package_type || "",
        package_cost: localFormData?.selectedRate?.total_charges || 50,
      })),
    };

    console.log("Final Data Before Submission:", transformedData);

    await handleBookingSubmission(transformedData);
  };


    const handleBookingSubmission = async (finalFormData) => {
      setIsLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/thisaiapi/bookings/create_booking/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(finalFormData),
        }
      );

      if (!response.ok) {
        const errorResponse = await response.json();
        console.error("Error Response from Backend:", errorResponse);
        alert(
          "Error: " + (errorResponse.message || JSON.stringify(errorResponse))
        );
        setIsLoading(false);
        return;
      }

      const responseData = await response.json();
      console.log("Booking Created Successfully:", responseData);
      setShowOverlay(false);
      // router.push("/booking");

    } catch (error) {
      alert("An error occurred while submitting the booking.");
    } finally {
      setIsLoading(false);
    }
  };

  if (!localFormData) {
    return <p>Loading...</p>;
  }

  return (
    <div className="w-full h-full flex flex-col gap-4 bg-[#ffffff] px-4 py-4 rounded-xl overflow-y-auto overflow-hidden">
      <div className="flex flex-col w-[660px] mb-11">
            <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
              Address
            </h1>
            <div className="flex gap-[40px]">
              {/* <div className="flex gap-[219px]"> */}
                <h1 className="text-[#718096] text-lg font-bold font-Inria">
                  From
                </h1>
                <p className="text-gray-900 text-base font-normal font-Mono">
      {localFormData.from_pincode}<br/>
      {localFormData.ship_from_address?.CountryCode || "-"}
</p>
            
              {/* </div> */}

              <h1 className="text-[#718096] text-lg font-bold font-Inria pl-32">To</h1>
              <p className="text-gray-900 text-base font-normal font-Mono">
      {localFormData.to_pincode}<br/>
      {localFormData.ship_to_address?.CountryCode || "-"}</p>
    
                
            </div>
          </div>

      {/* Package & Instructions */}
      <div className="flex w-full justify-between">
      <div className="flex flex-col w-[35%] gap-[16px]">
              <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
                Package Details
              </h1>
              <div className="flex flex-col gap-[10px]">
                <div className="flex gap-[120px]">
                  <p className="text-[#718096] text-lg font-normal font-Inria">
                    No. of Packages
                  </p>
                  <p className="text-gray-900 text-base font-normal font-Mono">
                    {localFormData.package_count}
                  </p>
                </div>
                <div className="flex gap-[148px]">
                  <p className="text-[#718096] text-lg font-normal font-Inria">
                    Pickup Date
                  </p>
                  <p className="text-gray-900 text-base font-normal font-Mono">
                    {localFormData.pickup_date}
                  </p>
                </div>
  
                <div className="flex gap-[144px]">
                  <p className="text-[#718096] text-lg font-normal font-Inria">
                    Pickup Time
                  </p>
                  <p className="text-gray-900 text-base font-normal font-Mono">
                    {localFormData.pickup_time}
                  </p>
                </div>
    
                <div className="flex gap-[130px]">
                  <p className="text-[#718096] text-lg font-normal font-Inria">
                    Package Type
                  </p>
                  <p className="text-gray-900 text-base font-normal font-Mono px-2 rounded">
                    {localFormData.package_type}
                  </p>
                </div>
              </div>
            </div>
 {/* carrier plan display */}
 <div className="flex flex-col w-[35%] gap-[16px]">
    <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
      Carrier
    </h1>
    <div className="flex flex-col gap-[10px]">
      <div className="flex justify-between">
        <p className="text-[#718096] text-lg font-normal font-Inria">
          Carrier Name
        </p>
        <p className="text-gray-900 text-base font-normal font-Mono">
        {localFormData.selectedRate?.carrier_name}
        </p>
      </div>

      <div className="flex justify-between">
        <p className="text-[#718096] text-lg font-normal font-Inria">
          Carrier Plan
        </p>
        <p className="text-gray-900 text-base font-normal font-Mono">
        {localFormData.selectedRate?.carrier_plan}
        </p>
      </div>

      <div className="flex justify-between">
        <p className="text-[#718096] text-lg font-normal font-Inria">
          Est. Cost
        </p>
        <p className="text-gray-900 text-base font-normal font-Mono">
        ${localFormData.selectedRate?.total_charges}
        </p>
      </div>

      <div className="flex justify-between">
        <p className="text-[#718096] text-lg font-normal font-Inria">
          Est. Delivery Date
        </p>
        <p className="text-gray-900 text-base font-normal font-Mono">
        {localFormData.selectedRate?.estimated_arrival_date}
        </p>
      </div>
    </div>
  </div>
  <div className="flex flex-col gap-1 w-[25%]">
              <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
                Instructions
              </h1>
              <div className="w-[290px] p-4 bg-neutral-50 rounded-xl shadow-[0px_0px_1px_0px_rgba(0,0,0,0.25)] justify-start items-start">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
                ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
                aliquip
              </div>
            </div>
          </div>

          <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
  Item Details
</h1>
<div className="w-full flex gap-3 bg-[#edf2fa] p-4 rounded-xl shadow-md">
      {localFormData.package_details?.map((pkg, index) => (
        <div key={index} className="w-[320px] bg-white p-4 rounded-xl shadow-md flex flex-col gap-2">
          <h1 className="text-[#4972b4] text-[18px] font-bold font-Condensed">
        Item {index + 1}
      </h1>
      <div className="w-full flex flex-col gap-2 pb-2">
        <div className="flex justify-between">
          <p className="text-[#718096] font-Mono">Length:</p>
          <p className="text-gray-900 font-Mono">
            {pkg.length ? `${pkg.length} cm` : "-"}
          </p>
        </div>

        <div className="flex justify-between">
          <p className="text-[#718096] font-Mono">Width:</p>
          <p className="text-gray-900 font-Mono">
            {pkg.width ? `${pkg.width} cm` : "-"}
          </p>
        </div>


        <div className="flex justify-between">
          <p className="text-[#718096] font-Mono">Height:</p>
          <p className="text-gray-900 font-Mono">
            {pkg.height ? `${pkg.height} cm` : "-"}
          </p>
        </div>

        <div className="flex justify-between">
          <p className="text-[#718096] font-Mono">Weight:</p>
          <p className="text-gray-900 font-Mono">
            {pkg.weight ? `${pkg.weight} kg` : "-"}
          </p>
        </div>
      </div>

        </div>
      ))}
      </div>

      <div className="flex justify-end">

      <button
        type="button"
        className="submit px-2 py-2 bg-red-500 text-white rounded-md"
        onClick={handleProceedToBooking} // Open overlay instead of submitting
        disabled={isLoading}
      >
        {isLoading ? "Processing..." : "Proceed"}
      </button>

      {showBookingFlow && (
        <ParentOverlayManager
          onClose={onClose}
          startFromQuotation={true}
          quotationData={selectedQuotation || localFormData}
        />
      )}

     
    </div>
    </div>
  );
};

export default QuotationReview;
