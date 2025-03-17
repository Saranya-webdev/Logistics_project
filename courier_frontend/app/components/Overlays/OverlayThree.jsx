import React, { useState, useEffect } from 'react';
import ProgressBar from './ProgressBar';
import { FaTimesCircle } from 'react-icons/fa';
import ShippingTable from './ShippingTable';
import { useRouter } from "next/navigation";

function OverlayThree({ onClose, formData, setFormData, setCurrentStep, shippingRates, onProceed }) {
  const steps = ['Address', 'Package', 'Carrier'];
  const [selectedRate, setSelectedRate] = useState(null);
  const router = useRouter();

  const handlePrevious = () => setCurrentStep(1); // Navigate back to OverlayTwo

  const handleRateSelect = (rate) => {
    console.log("Selected Rate Before Setting:", rate);
    if (!rate) return;

    const updatedRate = {
      ...rate,
      carrier_name: rate.carrier_name || "UPS",
      carrier_plan: rate.carrier_plan || rate.service_name || "N/A",
      service_code: rate.service_code || "N/A",
      total_charges: parseFloat(rate.total_charges || 0),
    };
    setSelectedRate(updatedRate);
    setFormData((prev) => {
      const updatedFormData = {
        ...prev,
        selectedRate: updatedRate,
        package_details: prev.package_details.map((item) => ({
          ...item,
          carrier_name: updatedRate.carrier_name,
          carrier_plan: updatedRate.carrier_plan,
          service_code: updatedRate.service_code,
        })),
      };
      localStorage.setItem("formData", JSON.stringify(updatedFormData));
      return updatedFormData;
    });
  };

  useEffect(() => {
    console.log("Updated Selected Rate:", selectedRate);
  }, [selectedRate]);

  const formatBookingData = (type) => {
    if (!selectedRate) {
      alert("Please select a shipping rate before proceeding.");
      return null;
    }

    const packageDetails = formData.package_details?.[0] || {}; // Use formData here
    const formattedEstDeliveryDate = selectedRate.estimated_arrival_date
      ? new Date(selectedRate.estimated_arrival_date).toISOString().split("T")[0]
      : null;

    return {
      customer_id: formData.customer_id || 0, // Use formData here
      quotation_id: formData.quotation_id || "N/A", // Use formData here
      type, // "booking" or "quotation"
      status: type === "quotation" ? "Saved" : "Pending", // Corrected the status field to lowercase
      from_pincode: formData.ship_from_address?.PostalCode || formData.from_pincode || "N/A",
    to_pincode: formData.ship_to_address?.PostalCode || formData.to_pincode || "N/A",
      ship_to_address: {
        ...formData.ship_to_address,
        to_pincode: formData.ship_to_address?.PostalCode || "N/A", // Convert PostalCode to to_pincode
        PostalCode: undefined,
      },// Use formData here
      ship_from_address: {
        ...formData.ship_from_address,
        from_pincode: formData.ship_from_address?.PostalCode || "N/A", // Convert PostalCode to from_pincode
        PostalCode: undefined,
      },// Use formData here
      package_count: parseInt(formData.package_count || 1, 10), // Use formData here
      pickup_date: formData.pickup_date || new Date().toISOString().split("T")[0], // Use formData here
      package_details: [
        {
            ...packageDetails,
            carrier_name: selectedRate.carrier_name,
            carrier_plan: selectedRate.carrier_plan,
            service_code: selectedRate.service_code,
            est_cost: parseFloat(selectedRate.total_charges || 0),
            total_cost: parseFloat(selectedRate.total_charges || 0),
            est_delivery_date: formattedEstDeliveryDate,
            booking_date: new Date().toISOString().split("T")[0],
            booking_by: "user",
          }
      ],
      booking_items: formData.package_details.map((item) => ({ // Use formData here
        weight: parseFloat(item.weight || 0),
        length: parseFloat(item.length || 0),
        width: parseFloat(item.width || 0),
        height: parseFloat(item.height || 0),
        package_type: item.package_type || "Unknown",
        package_cost: parseFloat(selectedRate.total_charges || 0),
      })),
    };
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedRate) {
      alert("Please select a shipping rate before proceeding.");
      return;
    }
    onProceed();
    router.push("/bookings/reviewpage");
  };

  const handleSave = async () => {
    if (!formData || !formData.quotation_id) {
      alert("No quotation found to update. Please try again.");
      return;
    }

    const quotationData = formatBookingData("quotation");
    console.log("Final Quotation Data before Saving:", quotationData);

    if (!quotationData) return;

    try {
      const updateUrl = `http://127.0.0.1:8000/thisaiapi/bookings/quotations/${formData.quotation_id}/updatequotation`; 
      // Use formData here

      const response = await fetch(updateUrl, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(quotationData),
      });

      if (response.ok) {
        alert("Quotation updated successfully!");

        // Redirect to Booking Table after successful quotation update
        router.push(`/quotations?selectedEntity=${encodeURIComponent(JSON.stringify(quotationData))}&userType=quotation`);



        onClose();
      } else {
        const errorResponse = await response.json();
        console.error("Error Response from Backend:", errorResponse);
        alert("Error updating quotation: " + JSON.stringify(errorResponse));
      }
    } catch (error) {
      console.error("Network error:", error);
      alert("An error occurred while updating the quotation. Please try again.");
    }

    onProceed();
  };

  const handleProceed = () => {
    if (!formData || !formData.package_details || !formData.ship_to_address) {
      alert("Missing required booking details.");
      return;
    }

    const updatedFormData = {
      ...formData,
      selectedRate,
    };
    setFormData(updatedFormData)
    localStorage.setItem("formData", JSON.stringify(updatedFormData));

    console.log("Proceeding with FormData:", updatedFormData);

    router.push("/bookings/reviewpage");
  };

  return (
    <div className="overlay w-[1004px]">
      <div className="flex justify-between items-center">
        <h1 className="CC">Select Carrier Plan</h1>
        <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73]" />
      </div>
      <div className="flex flex-col justify-center items-center">
        <div className="p-6">
          <ProgressBar steps={steps} currentStep={2} />
        </div>

        {shippingRates?.length > 0 ? (
          <ShippingTable
            shippingRates={shippingRates}
            selectedRate={selectedRate}
            handleRateSelect={handleRateSelect}
          />
        ) : (
          <p>No shipping rates available. Please try again later.</p>
        )}

        <div className="three">
          <button type="button" className="btn1" onClick={handlePrevious}>
            Previous
          </button>
          <button type="button" className="save" onClick={handleSave}>
            Ship Later
          </button>
          <button type="button" className="btn" onClick={handleProceed}>
            Ship Now
          </button>
        </div>
      </div>
    </div>
  );
}

export default OverlayThree;

