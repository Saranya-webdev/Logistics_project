// for seperate create form
import React, { useState } from "react";
import { FaTimesCircle, FaCaretDown } from "react-icons/fa";
import { isPointInPolygon, isValidCoordinate } from 'geolib';

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:8000";

const entityConfigs = {
  customer: {
    title: "Create Customer",
    endpoint: "/thisaiapi/customers/createcustomer/",
    fields: {
      firstSet: [
        "customer_name", "customer_email", "customer_mobile", 
        "customer_address", "customer_city", "customer_state", 
        "customer_pincode", "customer_country", "customer_category","customer_geolocation"
      ],
      thirdSet: ["tax_id", "license_number", "designation", "company_name"], // Shown only if Business is selected
    },
  },
  agent: {
    title: "Create Agent",
    endpoint: "/thisaiapi/agents/createagent/",
    fields: [
      "agent_name", "agent_email", "agent_mobile", "agent_address",
      "agent_city", "agent_state", "agent_country", "agent_pincode",
      "agent_geolocation", "agent_category", "agent_businessname", "tax_id"
    ],
  },
  carrier: {
    title: "Create Carrier",
    endpoint: "/thisaiapi/carriers/createcarrier/",
    fields: [
      "carrier_name", "carrier_email", "carrier_mobile", "carrier_address",
      "carrier_city", "carrier_state", "carrier_country", "carrier_pincode",
      "carrier_geolocation"
    ],
  },
};

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

export default function EntityForm({ entityType, onClose }) {
  const config = entityConfigs[entityType] || {};
  
  const [formData, setFormData] = useState(
    config.fields 
      ? Array.isArray(config.fields) // Handle agents and carriers
        ? Object.fromEntries(config.fields.map(field => [field, ""]))
        : {
            ...Object.fromEntries(
              [...(config.fields.firstSet || []), ...(config.fields.thirdSet || [])].map(field => [field, ""])
            ),
            customer_personal: "", // Type selection (Personal or Business)
          }
      : {}
  );

  const [successMessage, setSuccessMessage] = useState("");

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleTypeSelection = (type) => {
    setFormData({ ...formData, customer_personal: type });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    if (!config.endpoint) {
      alert("API endpoint is missing!");
      return;
    }

    // Validate customer-specific fields
  if (entityType === "customer") {
    if (!formData.customer_name?.trim()) {
      alert("Customer Name is required.");
      return;
    }
    if (!formData.customer_email?.trim()) {
      alert("Customer Email is required.");
      return;
    }
  }

  // const formData = {
  //   customer_geolocation: "37.7749,-122.4194",
  //   agent_geolocation: "34.0522,-118.2437",
  //   carrier_geolocation: "36.1699,-115.1398"
  // };
  
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
  
    // Ensure all required fields are filled
    const requiredFields = [...(config.fields?.firstSet || [])];
    if (formData.customer_personal === "business") {
      requiredFields.push(...(config.fields?.thirdSet || []));
    }
  
    const missingFields = requiredFields
  .filter(field => !(entityType === "customer" && field === "customer_mobile")) // Exclude mobile only for customers
  .some(field => !formData[field]?.trim());

    if (missingFields) {
      alert("Please fill in all fields before submitting.");
      return;
    }
  
    // Prepare payload
  const payload = { ...formData };
  if (entityType === "customer") {
    payload.customer_type = formData.customer_personal === "business" ? "corporate" : "individual";
    delete payload.customer_personal;
  }
  
    try {
      const response = await fetch(`${API_BASE_URL}${config.endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload), // Ensure only necessary data is sent
      });
  
      if (!response.ok) {
        const errorData = await response.json();
        alert(`Error: ${JSON.stringify(errorData.detail || errorData)}`);
        console.error("API Error Response:", errorData);
        
        
        let errorMessage = "Failed to create entity";
      
        if (errorData.detail) {
            alert(`Error: ${JSON.stringify(errorData.detail)}`);
          } else {
            alert(`Error: ${JSON.stringify(errorData)}`);
          }
      
        throw new Error(errorMessage);
      }
      
  
      const responseData = await response.json();
      console.log(`Successfully created ${entityType}:`, responseData);
      setSuccessMessage(`Successfully created ${entityType}`);

      setFormData(Object.fromEntries(Object.keys(formData).map(field => [field, ""])));
    } catch (error) {
        console.error(`Error creating ${entityType}:`, error);
      
        if (error instanceof Error) {
          alert(`Error creating ${entityType}: ${error.message}`);
        } else {
          alert(`Error creating ${entityType}: ${JSON.stringify(error)}`);
        }
      }
    };      
  

  return (
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
              className="outline-none w-[310px] appearance-none bg-[#fafafa] text-gray-500 text-sm px-0 py-0"
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
              className="outline-none w-[310px] appearance-none font-Mono bg-[#fafafa] text-gray-500 text-xs px-0 py-0"
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
                  className={`px-6 py-2 rounded-xl transition-all bg-neutral-50 text-gray-700 border-2 placeholder-[#AABOBA] font-Mono text-xs ${
                    formData.customer_personal === type ? "border-blue-500 text-[#AABOBA] font-Mono text-xs" : "border-transparent font-Mono text-xs"
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
                  className="w-full px-6 py-3 bg-neutral-50 placeholder-[#AABOBA] focus:ring-0 rounded-xl border-transparent focus:border-transparent font-Mono text-xs" 
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
            Create
          </button>
        </div>
        {successMessage && (
          <p className="mt-10 text-green-600 text-center font-Roboto text-[20px]">{successMessage}</p>
        )}
      </form>
    </div>
  );
}
