import React, { useState, useEffect } from "react";
import { FaTimesCircle, FaCaretDown } from "react-icons/fa";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

const fieldLabels = {
  customer_name: "Name",
  agent_name: "Name",
  carrier_name: "Name",
  customer_email: "Email",
  agent_email: "Email",
  carrier_email: "Email",
  customer_mobile: "Mobile",
  agent_mobile: "Mobile",
  carrier_mobile: "Mobile",
  customer_address: "Address",
  agent_address: "Address",
  carrier_address: "Address",
  customer_city: "City",
  agent_city: "City",
  carrier_city: "City",
  customer_state: "State",
  agent_state: "State",
  carrier_state: "State",
  customer_pincode: "Pincode",
  agent_pincode: "Pincode",
  carrier_pincode: "Pincode",
  customer_country: "Country",
  agent_country: "Country",
  carrier_country: "Country",
  customer_geolocation: "Geolocation",
  agent_geolocation: "Geolocation",
  customer_category: "Category",
  agent_category: "Category",
  agent_businessname: "Business Name",
  tax_id: "Tax ID",
  license_number: "License Number",
  designation: "Designation",
  company_name: "Company Name",
};

export default function EntityForm({ entityType, onClose, initialData }) {
    const config = {
        customer: {
          title:  "Edit Customer" ,
          endpoint:  "/thisaiapi/customers/updatecustomer/",
          fields: {
            firstSet: [
              "customer_name", "customer_email", "customer_mobile", 
              "customer_address", "customer_city", "customer_state", 
              "customer_pincode", "customer_country", "customer_category","customer_geolocation"
            ],
            thirdSet: ["tax_id", "license_number", "designation", "company_name"],
          },
        },
        agent: {
          title: "Edit Agent" ,
          endpoint:  "/thisaiapi/agents/updateagent/",
          fields: [
            "agent_name", "agent_email", "agent_mobile", "agent_address",
            "agent_city", "agent_state", "agent_country", "agent_pincode",
            "agent_geolocation", "agent_category", "agent_businessname", "tax_id"
          ],
        },
        carrier: {
          title:  "Edit Carrier",
          endpoint: "/thisaiapi/carriers/updatecarrier/" ,
          fields: [
            "carrier_name", "carrier_email", "carrier_mobile", "carrier_address",
            "carrier_city", "carrier_state", "carrier_country", "carrier_pincode",
            "carrier_geolocation"
          ],
        },
      }[entityType];
  
  const [formData, setFormData] = useState({});

  useEffect(() => {
    if (initialData) {
      setFormData({
        ...initialData,
        customer_personal: initialData.designation || initialData.tax_id || initialData.company_name ? "business" : "personal"
      });
    } else {
      setFormData(
        Object.fromEntries(
          (Array.isArray(config.fields)
            ? config.fields
            : [...(config.fields?.firstSet || []), ...(config.fields?.thirdSet || [])]
          ).map((field) => [field, ""])
        )
      );
    }
  }, [initialData, JSON.stringify(config.fields)]);
  
  const [successMessage, setSuccessMessage] = useState("");

  // Validate geolocation format for all relevant fields
  const geoFields = {
    customer_geolocation: formData.customer_geolocation,
    agent_geolocation: formData.agent_geolocation,
    carrier_geolocation: formData.carrier_geolocation
  };
  
  for (const [field, value] of Object.entries(geoFields)) {
    if (value) {
      const [lat, long] = value.split(",").map(coord => parseFloat(coord.trim()));
  
      if (isNaN(lat) || isNaN(long)) {
        alert(`Invalid geolocation format in ${field}. Please use 'latitude,longitude' format.`);
        return;
      }
  
      // Check if within US boundaries
      if (lat < 24.396308 || lat > 49.384358 || long < -125.000000 || long > -66.934570) {
        alert(`Invalid geolocation range in ${field}. Please enter a valid US location.`);
        return;
      }
    }
  }

  const defaultFieldLabels = {
    tax_id: "Tax ID",
    designation: "Designation",
    license_number: "License Number",
    company_name: "Company Name",
  };
  
  const updatedFieldLabels = { ...defaultFieldLabels, ...fieldLabels };
  
  
  console.log("Updated Field Labels:", updatedFieldLabels);
  console.log("Third Set Fields:", config.fields?.thirdSet);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleTypeSelection = (type) => {
    setFormData((prevData) => {
      if (type === "business") {
        return {
          ...prevData,
          customer_personal: "business",
          tax_id: prevData.tax_id || "", // Ensure business fields exist
          license_number: prevData.license_number || "",
          designation: prevData.designation || "",
          company_name: prevData.company_name || "",
        };
      } else {
        const { tax_id, license_number, designation, company_name, ...updatedData } = prevData;
        return {
          ...updatedData,
          customer_personal: "personal",
        };
      }
    });
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Submitting Data:", formData);
  
    const updatedData = { ...formData };
  
    // Remove business fields if the type is personal
    if (updatedData.customer_personal === "personal") {
      delete updatedData.tax_id;
      delete updatedData.license_number;
      delete updatedData.designation;
      delete updatedData.company_name;
    }

    // If customer_personal is "personal", remove business-related fields
  if (updatedData.customer_personal === "personal") {
    delete updatedData.tax_id;
    delete updatedData.designation;
    delete updatedData.company_name;
    delete updatedData.license_number;
  }

    try {
      const response = await fetch(`${API_BASE_URL}${config.endpoint}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        const errorMessage = errorData.detail || JSON.stringify(errorData);
        alert(`Error: ${errorMessage}`);
        throw new Error(errorMessage);
      }

      const responseData = await response.json();
    console.log("Response Data:", responseData);

    setFormData(responseData);
      
      setSuccessMessage(`Successfully updated ${entityType}`);

    } catch (error) {
      alert(`Error ${ "updating" } ${entityType}: ${error.message}`);
    }
  };

  return (
    <div className="modal-overlay">
    <div className="overlay p-6 bg-white rounded-lg shadow-lg">
      <div className="flex justify-between items-center mb-8">
        <h1 className="CC">{config.title}</h1>
        <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73] cursor-pointer" />
      </div>
  
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-2 gap-4 mb-6">
          {Array.isArray(config.fields)
            ? config.fields.map((field, index) => (
              <div key={index} className="flex flex-col relative">
                 {field.includes("category") ? (
                   <div className="dropdown">
            <select
              name={field}
              value={formData[field] || ""}
              onChange={handleChange}
              className="outline-none w-[310px] appearance-none bg-[#fafafa] text-[#AABOBA] text-sm px-0 py-0"
            >
              <option value="">Select Category</option>
              <option value="tier_1">Tier 1</option>
              <option value="tier_2">Tier 2</option>
              <option value="tier_3">Tier 3</option>
            </select>
            <div className="absolute right-4 pointer-events-none">
                                      <FaCaretDown />
                                    </div>
                                    </div>
          ) : (
            <input
              type="text"
              name={field}
              placeholder={fieldLabels[field] || field.replace(/_/g, " ").replace(/\b\w/g, char => char.toUpperCase())}
              className="w-full px-4 py-3 bg-neutral-50 placeholder-[#AABOBA] focus:ring-0 rounded-xl border-transparent focus:border-transparent font-Mono text-xs"
              value={formData[field] || ""}
              onChange={handleChange}
            />
          )}
        </div>
      ))
            : (config.fields?.firstSet || []).map((field, index) => (
              <div key={index} className="flex flex-col relative">
                  {field.includes("category") ? (
                    <div className="dropdown">
            <select
              name={field}
              value={formData[field] || ""}
              onChange={handleChange}
              className="outline-none w-[310px] appearance-none font-Mono bg-[#fafafa] text-[#AABOBA] text-xs px-0 py-0"
            >
              <option value="">Category</option>
              <option value="tier_1">Tier 1</option>
              <option value="tier_2">Tier 2</option>
              <option value="tier_3">Tier 3</option>
            </select>
            <div className="absolute right-6 pointer-events-none">
                                      <FaCaretDown />
                                    </div>
                                    </div>
          ) : (
            <input
              type="text"
              name={field}
              placeholder={fieldLabels[field]}
              className="w-full px-4 py-3 bg-neutral-50 placeholder-[#AABOBA] focus:ring-0 rounded-xl border-transparent focus:border-transparent font-Mono text-xs"
              value={formData[field] || ""}
              onChange={handleChange}
            />
          )}
        </div>
      ))}
</div>
  
        {!Array.isArray(config.fields) && (
          <div className="mb-6">
            <h1 className="text-[#4972b4] text-base font-semibold font-Roboto mb-4">Type</h1>
            <div className="flex gap-4">
              {["personal", "business"].map((type) => (
                <button
                  key={type}
                  type="button"
                  className={`px-6 py-2 rounded-xl transition-all bg-neutral-50 text-gray-700 border-2 font-mono text-xs ${
                    formData.customer_personal === type ? "border-blue-500 text-[#AABOBA] font-mono text-xs" : "border-transparent"
                  }`}
                  onClick={() => handleTypeSelection(type)}
                >
                  {type.charAt(0).toUpperCase() + type.slice(1)}
                </button>
              ))}
            </div>
          </div>
        )}
  
  {formData.customer_personal === "business" && Array.isArray(config.fields?.thirdSet) && (
  <div className="grid grid-cols-2 gap-4 mb-6">
    {config.fields.thirdSet.map((field, index) => (
      <div key={index} className="flex flex-col col-span-1">
        <input
  key={field} // This forces re-render on field updates
  type="text"
  name={field}
  placeholder={
    fieldLabels[field] ||
    field.replace(/_/g, " ").replace(/\b\w/g, (char) => char.toUpperCase())
  }
  className="w-full px-4 py-3 bg-neutral-50 placeholder-[#AABOBA] focus:ring-0 rounded-xl border-transparent focus:border-transparent font-Mono text-xs"
  value={formData[field] || ""}
  onChange={handleChange}
/>

      </div>
    ))}
  </div>
)}

  
        <div className="flex justify-center">
          <button 
            type="submit" 
            className="btn mt-6 rounded-xl px-8 py-3 text-lg text-center bg-blue-500 text-white"
          >
            Update
          </button>
        </div>
        {successMessage && (
          <p className="mt-10 text-green-600 text-center font-Roboto text-[20px]">{successMessage}</p>
        )}
      </form>
    </div>
    </div>
  ); 
}

