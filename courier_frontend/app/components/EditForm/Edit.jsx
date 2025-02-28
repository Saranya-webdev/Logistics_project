import React, { useState, useEffect } from "react";
import { FaTimesCircle } from "react-icons/fa";

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
      setFormData(initialData);
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
  
  

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleTypeSelection = (type) => {
    setFormData((prev) => ({ ...prev, customer_personal: type }));
  };
  

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!config.endpoint) {
      alert("API endpoint is missing!");
      return;
    }

    const method =  "PUT";

    try {
      const response = await fetch(`${API_BASE_URL}${config.endpoint}`, {
        method: method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        const errorData = await response.json();
        const errorMessage = errorData.detail || JSON.stringify(errorData);
        alert(`Error: ${errorMessage}`);
        throw new Error(errorMessage);
      }
      

      alert(`Successfully ${ "updated" } ${entityType}`);
      onClose();
    } catch (error) {
      alert(`Error ${ "updating" } ${entityType}: ${error.message}`);
    }
  };

  return (
    <div className="overlay">
      <div className="flex justify-between items-center mb-8">
        <h1 className="CC">{config.title}</h1>
        <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73] cursor-pointer" />
      </div>
  
      <form onSubmit={handleSubmit}>
        <div className="grid grid-cols-2 gap-4 mb-6">
          {Array.isArray(config.fields)
            ? config.fields.map((field, index) => (
                <div key={index} className="flex flex-col col-span-1">
                  <input
                    type="text"
                    name={field}
                    placeholder={fieldLabels[field] || field.replace(/_/g, " ").replace(/\b\w/g, char => char.toUpperCase())}
                    className="w-full px-4 py-3 bg-neutral-50 placeholder-[#FAFAFA] focus:ring-0 rounded-xl border-transparent focus:border-transparent font-mono text-xs"
                    value={formData[field] || ""}
                    onChange={handleChange}
                  />
                </div>
              ))
            : (config.fields?.firstSet || []).map((field, index) => (
                <div key={index} className="flex flex-col col-span-1">
                  <input
                    type="text"
                    name={field}
                    placeholder={fieldLabels[field] || field.replace(/_/g, " ").replace(/\b\w/g, char => char.toUpperCase())}
                    className="w-full px-4 py-3 bg-neutral-50 placeholder-[#FAFAFA] focus:ring-0 rounded-xl border-transparent focus:border-transparent font-mono text-xs"
                    value={formData[field] || ""}
                    onChange={handleChange}
                  />
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
  
        {formData.customer_personal === "business" && !Array.isArray(config.fields) && (
          <div className="grid grid-cols-2 gap-4 mb-6">
            {(config.fields?.thirdSet || []).map((field, index) => (
              <div key={index} className="flex flex-col col-span-1">
                <input
                  type="text"
                  name={field}
                  placeholder={fieldLabels[field]}
                  className="w-full px-6 py-3 bg-neutral-50 placeholder-[#FAFAFA] focus:ring-0 rounded-xl border-transparent focus:border-transparent font-mono text-xs"
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
            className="btn mt-6 rounded-xl px-8 py-3 text-lg w-32 text-center bg-blue-500 text-white"
          >
            Update
          </button>
        </div>
      </form>
    </div>
  ); 
}

