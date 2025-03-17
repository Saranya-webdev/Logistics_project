"use client";
import React, { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import ShipmentComponent from "@/app/components/ShipmentLable/ShipmentComponent";

const BookingReviewPage = ({ onClose, formData: initialFormData }) => {
    const router = useRouter();
    const [localFormData, setLocalFormData] = useState(initialFormData || null);
    const [labelPath, setLabelPath] = useState(null);
    const [hasSubmitted, setHasSubmitted] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [showShipment, setShowShipment] = useState(false);
    const [shipmentResponse, setShipmentResponse] = useState(null);
    const [trackingNumber, setTrackingNumber] = useState("");
  
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
  
    useEffect(() => {
      if (localFormData && localFormData.package_count > 0) {
        setLocalFormData((prevData) => {
          const updatedPackageDetails = Array.from(
            { length: prevData.package_count },
            (_, index) => {
              // Only use defaults if the detail doesn't exist
              return prevData.package_details[index]
                ? { ...prevData.package_details[index] }
                : {
                    length: "",
                    width: "",
                    height: "",
                    weight: "",
                    package_type:"",
                    // pickup_date:""
                  };
            }
          );
  
          return { ...prevData, package_details: updatedPackageDetails };
        });
      }
    }, [localFormData?.package_count]);
  
  

    useEffect(() => {
        if (shipmentResponse?.tracking_number) {
          setTrackingNumber(shipmentResponse.tracking_number);
        }
      }, [shipmentResponse]);
      
    
      const handleFinalSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
    
        if (!localFormData) {
          alert("No booking data found.");
          setIsLoading(false);
          return;
        }

    const transformedData = {
      customer_id: localFormData.customer_id || 138,
      ship_to_address: {
        to_name:
          localFormData.to_name || localFormData.ship_to_address?.Name || "-",
        to_mobile:
          localFormData.to_mobile || localFormData.ship_to_address?.Mobile || "-",
        to_email:
          localFormData.to_email || localFormData.ship_to_address?.Email || "-",
        to_address:
          localFormData.to_address ||
          localFormData.ship_to_address?.Address ||
          "-",
        to_city:
          localFormData.to_city || localFormData.ship_to_address?.City || "-",
        to_state:
          localFormData.to_state ||
          localFormData.ship_to_address?.StateProvinceCode ||
          "-",
        to_pincode:
          localFormData.to_pincode ||
          localFormData.ship_to_address?.PostalCode ||
          "-",
        to_country:
          localFormData.to_country ||
          localFormData.ship_to_address?.CountryCode ||
          "-",
      },
      ship_from_address: {
        from_name:
          localFormData.from_name ||
          localFormData.ship_from_address?.Name ||
          "-",
        from_mobile:
          localFormData.from_mobile ||
          localFormData.ship_from_address?.Mobile ||
          "-",
        from_email:
          localFormData.from_email ||
          localFormData.ship_from_address?.Email ||
          "-",
        from_address:
          localFormData.from_address ||
          localFormData.ship_from_address?.Address ||
          "-",
        from_city:
          localFormData.from_city ||
          localFormData.ship_from_address?.City ||
          "-",
        from_state:
          localFormData.from_state ||
          localFormData.ship_from_address?.StateProvinceCode ||
          "-",
        from_pincode:
          localFormData.from_pincode ||
          localFormData.ship_from_address?.PostalCode ||
          "-",
        from_country:
          localFormData.from_country ||
          localFormData.ship_from_address?.CountryCode ||
          "-",
      },
      pickup_date: localFormData?.pickup_date || "",
      pickup_time: localFormData?.pickup_time || "",
      package_details: {
        carrier_name:
          localFormData?.selectedRate?.carrier_name ||
          localFormData?.carrier_name ||
          "",
        service_code:
          localFormData?.selectedRate?.service_code ||
          localFormData?.service_code ||
          "",
        carrier_plan:
          localFormData?.selectedRate?.carrier_plan ||
          localFormData?.carrier_plan ||
          "",
        package_count: localFormData.package_count || 1,
        est_cost: localFormData?.selectedRate?.total_charges || 50.0,
        total_cost: localFormData?.selectedRate?.total_charges || 50.0,
        est_delivery_date: localFormData?.selectedRate?.estimated_arrival_date
          ? new Date(
              localFormData.selectedRate.estimated_arrival_date + " UTC"
            )
              .toISOString()
              .split("T")[0]
          : "",
        booking_date: new Date().toISOString(), // Stores current date and time
        booking_by: "user",
      },
      booking_items: Array.isArray(localFormData.package_details)
  ? localFormData.package_details.map((item) => ({
        weight: parseFloat(item.weight),  // Ensure weight is a float
        length: item.length ? parseFloat(item.length) : 0.0,
width: item.width ? parseFloat(item.width) : 0.0,
height: item.height ? parseFloat(item.height) : 0.0,

        package_type: item.package_type || "",
        package_cost: parseFloat(localFormData?.selectedRate?.total_charges) || 0.0,  // Ensure package_cost is a float
      }))
  : [],

    };

    console.log("Final Data Before Submission:", transformedData);
    console.log(
      "Pickup date from BookingReview:",
      localFormData.pickup_date
    );
    console.log(
      "Pickup time from BookingReview:",
      localFormData.pickup_time
    );
    console.log("Package Details:", localFormData.package_details);

    console.log(
      "Parsed Estimated Delivery Date:",
      new Date(localFormData.selectedRate.estimated_arrival_date + " UTC")
        .toISOString()
        .split("T")[0]
    );

    try {
      console.log(
        "Submitting Booking Data:",
        JSON.stringify(transformedData, null, 2)
      );

      const response = await fetch(
        "http://127.0.0.1:8000/thisaiapi/bookings/create_booking/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(transformedData),
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
      console.log("Shipment Response: ", responseData);

      setShipmentResponse(responseData);

      if (responseData.tracking_number) {
        setTrackingNumber(responseData.tracking_number);
      }

      if (
        !responseData.shipment_id ||
        !responseData.total_charges ||
        !responseData.base_service_charge ||
        !responseData.label_filename
      ) {
        alert("Error: Incomplete shipment response from backend.");
        return;
      }

      setShipmentResponse(responseData);

      if (responseData.label_filename) {
        const fullPath = `/shipment_labels/${responseData.label_filename
          .split("/")
          .pop()}`;

        setLabelPath(fullPath); // Update state with label path
        setShowShipment(true); // Ensure ShipmentComponent is displayed
        console.log("Final Label Path:", fullPath);

        setHasSubmitted(true);
      } else {
        alert("Booking created successfully!");
        onClose && onClose();
      }
    } catch (error) {
      alert("An error occurred while submitting the booking.");
    } finally {
      setIsLoading(false);
    }
  };

  if (!localFormData) {
    return <p>Loading...</p>;
  }
  const bookings = localFormData ? [localFormData] : [];

  const {
    ship_from_address,
    ship_to_address,
    package_count,
    pickup_date,
    pickup_time,
    package_details,
    selectedRate,
    from_name,
    from_mobile,
    from_email,
    from_address,
    from_city,
    from_state,
    from_pincode,
    from_country,
    to_name,
    to_mobile,
    to_email,
    to_address,
    to_city,
    to_state,
    to_pincode,
    to_country,
  } = localFormData || {};

  return (
    <div className="w-full h-full flex flex-col gap-4 bg-[#ffffff] px-4 py-4 rounded-xl overflow-y-auto overflow-hidden no-scrollbar">
      {hasSubmitted ? (
        <>
          <h2 className="text-[#4972b4] text-[24px] font-bold font-Condensed  ">
            Shipping Label
          </h2>
          {showShipment && labelPath && trackingNumber && (
            <ShipmentComponent
              labelPath={labelPath}
              trackingNumber={trackingNumber}
              onClose={() => setShowShipment(false)}
            />
          )}
        </>
      ) : (
        <>
          {/* Address Details */}
          <div className="flex flex-col w-[660px] mb-11">
            <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
              Address
            </h1>
            <div className="flex gap-[40px]">
              <h1 className="text-[#718096] text-lg font-bold font-Inria">
                From
              </h1>
              <p className="text-gray-900 text-base font-normal font-Mono">
                {from_name || ship_from_address?.Name || "-"} <br />
                {from_address || ship_from_address?.Address || "-"}, <br />
                {from_city || ship_from_address?.City || "-"},{" "}
                {from_state || ship_from_address?.StateProvinceCode || "-"} <br />
                {from_pincode || ship_from_address?.PostalCode || "-"},{" "}
                {from_country || ship_from_address?.CountryCode || "-"}
              </p>

              <h1 className="text-[#718096] text-lg font-bold font-Inria pl-32">
                To
              </h1>
              <p className="text-gray-900 text-base font-normal font-Mono">
                {to_name || ship_to_address?.Name || "-"} <br />
                {to_address || ship_to_address?.Address || "-"}, <br />
                {to_city || ship_to_address?.City || "-"},{" "}
                {to_state || ship_to_address?.StateProvinceCode || "-"} <br />
                {to_pincode || ship_to_address?.PostalCode || "-"},{" "}
                {to_country || ship_to_address?.CountryCode || "-"}
              </p>
            </div>
          </div>

          {/* Package & Instructions */}
          <div className="flex  w-full justify-between">
          <div className="flex flex-col w-[35%] gap-[16px]">
          <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
                Package
              </h1>
              <div className="flex flex-col gap-[10px]">
                <div className="flex gap-[120px]">
                  <p className="text-[#718096] text-lg font-normal font-Inria">
                    No. of Packages
                  </p>
                  <p className="text-gray-900 text-base font-normal font-Mono">
                    {package_count ?? "-"}
                  </p>
                </div>
                <div className="flex gap-[148px]">
                  <p className="text-[#718096] text-lg font-normal font-Inria">
                    Pickup Date
                  </p>
                  <p className="text-gray-900 text-base font-normal font-Mono">
                    {pickup_date ? pickup_date.split("T")[0] : "Not Set"}
                  </p>
                </div>
                <div className="flex gap-[144px]">
                  <p className="text-[#718096] text-lg font-normal font-Inria">
                    Pickup Time
                  </p>
                  <p className="text-gray-900 text-base font-normal font-Mono">
                    {pickup_time ? pickup_time : "Not Set"}
  
                  </p>
                </div>
                <div className="flex gap-[130px]">
                  <p className="text-[#718096] text-lg font-normal font-Inria">
                    Package Type
                  </p>
                  <p className="text-gray-900 text-base font-normal font-Mono px-2 rounded">
                    {package_details[0]?.package_type || "-"}
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
          {selectedRate?.carrier_name || "-"}
        </p>
      </div>
      <div className="flex justify-between">
        <p className="text-[#718096] text-lg font-normal font-Inria">
          Carrier Plan
        </p>
        <p className="text-gray-900 text-base font-normal font-Mono">
          {selectedRate?.carrier_plan || "-"}
        </p>
      </div>
      <div className="flex justify-between">
        <p className="text-[#718096] text-lg font-normal font-Inria">
          Est. Cost
        </p>
        <p className="text-gray-900 text-base font-normal font-Mono">
        ${selectedRate?.total_charges || "-"}
        </p>
      </div>
      <div className="flex justify-between">
        <p className="text-[#718096] text-lg font-normal font-Inria">
          Est. Delivery Date
        </p>
        <p className="text-gray-900 text-base font-normal font-Mono">
          {selectedRate?.estimated_arrival_date
            ? new Date(selectedRate.estimated_arrival_date).toLocaleDateString()
            : "-"}
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

          {/* Item Details */}
          <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
  Item 
</h1>
<div className="w-full flex gap-3 bg-[#edf2fa] p-4 rounded-xl shadow-md">
{localFormData?.package_details?.map((item, index) => (
    <div key={index} className="w-[320px] bg-white p-4 rounded-xl shadow-md flex flex-col gap-2">
      <h1 className="text-[#4972b4] text-[18px] font-bold font-Condensed">
        Item {index + 1}
      </h1>
      <div className="w-full flex flex-col gap-2 pb-2">
        <div className="flex justify-between">
          <p className="text-[#718096] font-Mono">Length:</p>
          <p className="text-gray-900 font-Mono">
            {item?.length ? `${item.length} cm` : "-"}
          </p>
        </div>
        <div className="flex justify-between">
          <p className="text-[#718096] font-Mono">Width:</p>
          <p className="text-gray-900 font-Mono">
            {item?.width ? `${item.width} cm` : "-"}
          </p>
        </div>
        <div className="flex justify-between">
          <p className="text-[#718096] font-Mono">Height:</p>
          <p className="text-gray-900 font-Mono">
            {item?.height ? `${item.height} cm` : "-"}
          </p>
        </div>
        <div className="flex justify-between">
          <p className="text-[#718096] font-Mono">Weight:</p>
          <p className="text-gray-900 font-Mono">
            {item?.weight ? `${item.weight} kg` : "-"}
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
              onClick={handleFinalSubmit}
              disabled={isLoading}
            >
              {isLoading ? "Processing..." : "Proceed"}
            </button>
          </div>
        </>
      )}
    </div>
  );
};

export default BookingReviewPage;