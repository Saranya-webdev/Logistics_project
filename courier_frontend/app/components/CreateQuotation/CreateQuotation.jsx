"use client";

import React, { useState, useEffect } from "react";
import { FaTimesCircle, FaCaretDown } from "react-icons/fa";
import ShippingTable from "../Overlays/ShippingTable";
const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

// Validation function
const validatePayload = (formData) => {
  const errors = {};
  const { package_details, package_count, package_type } = formData;

  if (!formData.from_pincode) {
    errors["from_pincode"] = "Ship-from Pincode is missing.";
  }
  if (!formData.to_pincode) {
    errors["to_pincode"] = "Ship-to Pincode is missing.";
  }
  if (!package_count) {
    errors["package_count"] = "Package Count is required.";
  }
  if (!package_type) {
    errors["package_type"] = "Package type is required.";
  }

  return Object.keys(errors).length > 0 ? errors : {};
};

export default function QuotationForm({ onClose }) {
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [carrierPlans, setCarrierPlans] = useState([]);
  const [selectedRate, setSelectedRate] = useState(null);
  const [showCarrierPlans, setShowCarrierPlans] = useState(false);

  const [formData, setFormData] = useState({
    quotation_id: "",  // Ensure it's a string or valid ID type
    ship_to_name: "",
    ship_to_mobile: "",
    ship_to_email: "",
    ship_to_address: "",
    ship_to_city: "",
    ship_to_state: "",
    ship_from_name: "",
    ship_from_mobile: "",
    ship_from_email: "",
    ship_from_address: "",
    ship_from_city: "",
    ship_from_state: "",
    pickup_date: "",
    pickup_time: "",
    from_pincode: "",
  to_pincode: "",
  package_type: "",
    package_count: 1, // Ensure package count has a default value
    package_details: [
      {
        weight: "", length: "", width: "", height: "", 
        pickup_date: "", package_type: "", status: "Saved"
      }
    ]
  });
  


  const handlePackageChange = (index, e) => {
    const { name, value } = e.target;
    console.log(`Updating ${name} at index ${index}:`, value);  // Debugging

    setFormData((prevFormData) => {
      const newPackageDetails = [...prevFormData.package_details];
      newPackageDetails[index][name] = value || "";
      newPackageDetails[index]["package_type"] = prevFormData.package_type; // Add package_type to each package detail
      return {
        ...prevFormData,
        package_details: newPackageDetails,
      };
    });
  };

  const handlePackageCountChange = (e) => {
    const count = parseInt(e.target.value, 10) || 1;

    setFormData((prevState) => {
        if (prevState.package_count === count) return prevState; //  Prevent unnecessary updates

        return {
            ...prevState,
            package_count: count,
            package_details: prevState.package_details.length === count 
                ? prevState.package_details 
                : Array.from({ length: count }, (_, i) => prevState.package_details[i] || {
                    weight: "", length: "", width: "", height: "", pickup_date: "", package_type: prevState.package_type || "", status: "Saved"
                }),
        };
    });
};


useEffect(() => {
  if (formData.package_details.length === 0) {
      setErrors((prevErrors) => ({ ...prevErrors, package: "Package details are required." }));
  }
}, [formData.package_details]);




  const handleRateSelect = (rate) => {
    const updatedRate = {
      ...rate,
      carrier_name: rate.carrier_name || "UPS",
      carrier_plan: rate.carrier_plan || rate.service_name || "N/A",
      service_code: rate.service_code || "N/A",
      total_charges: parseFloat(rate.total_charges || 0),
    };
    setSelectedRate(updatedRate);
  };

  useEffect(() => {
    if (selectedRate) {
        console.log("Updated Selected Rate:", selectedRate);
    }
}, [selectedRate]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({ ...prevState, [name]: value,
     }));
  };

  const handleNext = async () => {
    console.log("handleNext triggered");
    setLoading(true);

    const validationErrors = validatePayload(formData);
    if (Object.keys(validationErrors).length > 0) {
      setErrors(validationErrors);
      setLoading(false);
      return;
    }
    setShowCarrierPlans(true);

    try {
      const originalPickupDate = formData.package_details[0]?.pickup_date;
        const formattedPickupDate = originalPickupDate?.replace(/[-:]/g, "").slice(0, 8) || ""; // Correctly format the date to YYYYMMDD
        const pickupTime = formData.pickup_time
      const payload = {
        ship_to_address: {
          Name: formData.ship_to_name || "",
          Mobile: formData.ship_to_mobile || "",
          Email: formData.ship_to_email || "",
          Address: formData.ship_to_address || "",
          City: formData.ship_to_city || "",
          StateProvinceCode: formData.ship_to_state || "",
          PostalCode: formData.to_pincode || "",
          CountryCode: "US",
        },
        ship_from_address: {
          Name: formData.ship_from_name || "",
          Mobile: formData.ship_from_mobile || "",
          Email: formData.ship_from_email || "",
          Address: formData.ship_from_address || "",
          City: formData.ship_from_city || "",
          StateProvinceCode: formData.ship_from_state || "",
          PostalCode: formData.from_pincode || "",
          CountryCode: "US",
        },
        from_pincode: formData.from_pincode || formData.ship_from_address?.PostalCode || "",
        to_pincode: formData.to_pincode || formData.ship_to_address?.PostalCode || "",
        package_count: formData.package_count || 0,
        pickup_date: formattedPickupDate, //send the correct format
        pickup_time: pickupTime || "", // Default pickup time
        package_details: formData.package_details.map(pkg => ({
          weight: pkg.weight || "",
          length: pkg.length || "",
          width: pkg.width || "",
          height: pkg.height || "",
          package_type: pkg.package_type || formData.package_type || "",
        })),
      };

      console.log("Sending Request Payload:", payload);

      const response = await fetch(`${API_BASE_URL}/thisaiapi/bookings/fetch-ups-rates/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("Failed to fetch UPS shipping rates");

      const data = await response.json();
      console.log("UPS Shipping Rates Response:", data);
      setCarrierPlans(data || []);
      if (data.length > 0 && data[0].quotation_id && formData.quotation_id !== data[0].quotation_id) {
        setFormData((prevFormData) => ({
          ...prevFormData,
          from_pincode: data[0].ship_from_postalcode || prevFormData.from_pincode || "",
          to_pincode: data[0].ship_to_postalcode || prevFormData.to_pincode || "",
          package_type: data[0].package_details?.length > 0 
              ? data[0].package_details[0].package_type 
              : prevFormData.package_type || "N/A",
          quotation_id: data[0].quotation_id,
          pickup_time: payload.pickup_time,
          pickup_date: originalPickupDate
      }));
      
    }
    

    } catch (error) {
      console.error("Error fetching UPS rates:", error);
      setErrors({ fetch: "Failed to fetch UPS rates" });
    } finally {
      setLoading(false);
    }
  };

  const handleSaveQuotation = async () => {
    if (!selectedRate) {
        setErrors({ carrier: "Please select a carrier plan first." });
        return;
    }
    if (!formData.quotation_id) {
        setErrors({ quotation: "No quotation ID found, please fetch rates again." });
        return;
    }

    setLoading(true);
    try {
      const updatePayload = {
        quotation_id: formData.quotation_id,
        status: "Saved",
        package_count: formData.package_count || formData.package_details.length || 0,
        ship_to_address: {
            ...formData.ship_to_address,
                PostalCode: formData.to_pincode || "", // Assign the correct value
                CountryCode: "US",
        },
        ship_from_address: {
            ...formData.ship_from_address,
                PostalCode: formData.from_pincode || "", // Assign the correct value
                CountryCode: "US",
        },
        from_pincode: formData.from_pincode || "",
        to_pincode: formData.to_pincode || "",
        pickup_date: formData.pickup_date || "",
        pickup_time: formData.pickup_time || "",
        package_details: formData.package_details.map(pkg => ({
            weight: pkg.weight || "",
            length: pkg.length || "",
            width: pkg.width || "",
            height: pkg.height || "",
            package_type: formData.package_type || "",
            status: "Saved"
        })),
        selectedRate 
    };
    

        console.log("Updating Quotation:", updatePayload);

        const response = await fetch(`${API_BASE_URL}/thisaiapi/quotations/${formData.quotation_id}/updatequotation/`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(updatePayload),
        });

        const responseData = await response.json(); //  Get API response

        if (!response.ok) {
            console.error("Error saving quotation:", responseData);
            setErrors({ save: responseData.detail || "Failed to save quotation." });
            return;
        }

        console.log("Quotation Updated Response:", responseData); //  Log response to verify status

        //  Update formData to reflect Saved status in UI
        setFormData(prevFormData => ({
            ...prevFormData,
            status: "Saved" 
        }));

        alert("Quotation Saved successfully!");
        onClose();
    } catch (error) {
        console.error("Error saving quotation:", error);
        setErrors({ save: "Failed to save quotation" });
    } finally {
        setLoading(false);
    }
};
   
  return (
    <div className="overlay p-6 bg-white rounded-lg shadow-lg">
      <div className="flex justify-between items-center mb-4">
        <h1 className="CC">Create Quotation</h1>
        <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73] cursor-pointer" />
      </div>

      <form>
        {/* Row 1 - Labels */}
        <div className="grid grid-cols-2 gap-4">
          <h1 className="formTitle text-xl font-semibold">From</h1>
          <h1 className="formTitle text-xl font-semibold">To</h1>
        </div>

        {/* Row 2 - Inputs */}
        <div className="grid grid-cols-2 gap-4 mb-4">
          <input type="text" name="from_pincode" placeholder="From Pincode" className="formContent" value={formData.from_pincode ?? ""} onChange={handleChange} />

          {errors['from_pincode'] && <p className="text-red-500 text-sm">{errors['from_pincode']}</p>}

          <input type="text" name="to_pincode" placeholder="To Pincode" className="formContent" value={formData.to_pincode} onChange={handleChange} />
          {errors['to_pincode'] && <p className="text-red-500 text-sm">{errors['to_pincode']}</p>}
        </div>

        {/* Package Details */}
        <h2 className="text-lg font-semibold mb-2">Package Details</h2>
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div className="relative">
            <select className="formContent appearance-none w-full text-gray-500 text-sm" name="package_type" value={formData.package_type || ""} onChange={(e) => handleChange(e)}>
              <option value="" disabled>Package Type</option>
              <option value="Document">Document</option>
              <option value="Non-Document">Non-Document</option>
            </select>
            <div className="absolute right-4 top-1/2 transform -translate-y-1/2 pointer-events-none">
              <FaCaretDown />
            </div>
            {errors['package_type'] && <p className="text-red-500 text-sm">{errors['package_type']}</p>}
          </div>

          <input type="number" name="package_count" placeholder="Package Count" value={formData.package_count} onChange={handlePackageCountChange} className="formContent mb-4" min="1" />
          {errors['package_count'] && <p className="text-red-500 text-sm">{errors['package_count']}</p>}
        </div>

        {/* Pickup Date */}
        <div className="mt-4">
          <h3 className="text-lg font-semibold">Pickup Date</h3>
          <div className="mt-2">
            <input type="datetime-local" name="pickup_date" placeholder="Pickup Date" value={formData.package_details[0]?.pickup_date || ""} onChange={(e) => handlePackageChange(0, e)} className="formContent w-full max-w-[280px]" />
          </div>
          {errors["Pickup Date is required for package 1."] && <p className="text-red-500 text-sm">{errors["Pickup Date is required for package 1."]}</p>}
        </div>

        {/* Package Details (Loop) */}
        {formData.package_details.map((pkg, index) => (
          <div key={index} className="mb-5 mt-6">
            <h1 className="formTitle mt-15 mb-[15px] text-xl font-semibold font-['Roboto Condensed']">Item {index + 1}</h1>

            <div className="grid grid-cols-2 gap-4">
              {(formData.package_type === "Non-Document") && (
                <>
                  <input type="text" name="length" placeholder="Length" value={pkg.length ?? ""}
 onChange={(e) => handlePackageChange(index, e)} className="formContent w-full" />
                  <input type="text" name="width" placeholder="Width" value={pkg.width ?? ""} onChange={(e) => handlePackageChange(index, e)} className="formContent w-full" />
                  <input type="text" name="height" placeholder="Height" value={pkg.height ?? ""} onChange={(e) => handlePackageChange(index, e)} className="formContent w-full" />
                </>
              )}
              <input type="text" name="weight" placeholder="Weight" value={pkg.weight ?? ""} onChange={(e) => handlePackageChange(index, e)} className="formContent w-full" />
              {errors[`weight is required for package ${index + 1}.`] && <p className="text-red-500 text-sm">{errors[`weight is required for package ${index + 1}.`]}</p>}
            </div>
          </div>
        ))}

        {/* Carrier Plans Display */}
        {carrierPlans.length > 0 && showCarrierPlans && (
          <ShippingTable
            shippingRates={carrierPlans}
            selectedRate={selectedRate}
            handleRateSelect={handleRateSelect}
          />
        )}

        {/* Buttons */}
        <div className="flex justify-between mt-6">
          {!showCarrierPlans && (
            <button
              type="button"
              className="btn bg-blue-500 text-white px-6 py-2 rounded-lg"
              onClick={handleNext} disabled={loading}
            >
               {loading ? "Fetching rates..." : "Next"}
            </button>
          )}

          {showCarrierPlans && (
            <button type="button" onClick={handleSaveQuotation} className="btn bg-blue-500 text-white px-4 py-2 rounded">
              Save as Quotation
            </button>
          )}
        </div>
      </form>
    </div>
  );
}



