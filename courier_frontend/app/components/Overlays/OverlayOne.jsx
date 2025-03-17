// version of customer id hardcoded
import React, { useState, useEffect } from 'react';
import { FaTimesCircle, FaCaretDown } from 'react-icons/fa';
import ProgressBar from './ProgressBar';

function OverlayOne({ onClose, setCurrentStep, formData, setFormData }) {
  const [savedAddresses, setSavedAddresses] = useState([]);
  const initialAddressState = {
    Name: "",
    Mobile: "",
    Email: "",
    Address: "",
    City: "",
    StateProvinceCode: "",
    CountryCode: "",
    PostalCode: ""
  };

  useEffect(() => {
    const customerId = formData?.customer_id || 151;
    fetch(`http://127.0.0.1:8000/thisaiapi/addressbook/${customerId}/viewaddressbook/`)
      .then(response => response.json())
      .then(data => {
        if (Array.isArray(data)) {
          setSavedAddresses(data);
        } else {
          console.error("API response is not an array:", data);
        }
      })
      .catch(error => console.error("Error fetching addresses:", error.message));
  }, [formData.customer_id]);

  const handleSavedAddressChange = (e, type) => {
    const selectedId = parseInt(e.target.value, 10);
    if (!selectedId) {
      setFormData(prev => ({
        ...prev,
        [type]: initialAddressState,
        [`selected${type}Id`]: "",
        from_pincode: type === "ship_from_address" ? "" : prev.from_pincode,
      to_pincode: type === "ship_to_address" ? "" : prev.to_pincode,
      }));
      return;
    }

    const selectedAddress = savedAddresses.find(addr => addr.address_id === selectedId);
    if (!selectedAddress) {
      console.error("Selected address not found.");
      return;
    }

    setFormData(prev => ({
      ...prev,
      [type]: {
        Name: selectedAddress.name,
        Mobile: selectedAddress.mobile,
        Email: selectedAddress.email_id,
        Address: selectedAddress.address,
        City: selectedAddress.city,
        StateProvinceCode: selectedAddress.state,
        CountryCode: selectedAddress.country,
        PostalCode: selectedAddress.pincode
      },
      [`selected${type}Id`]: selectedId,
      from_pincode: type === "ship_from_address" ? selectedAddress.pincode : prev.from_pincode,
    to_pincode: type === "ship_to_address" ? selectedAddress.pincode : prev.to_pincode,
    }));
  };

  const handleChange = (e, type) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [type]: {
        ...prev[type],
        [name]: value,
      }
    }));
  };

  return (
    <div className="overlay">
      <div className="flex justify-between items-center">
        <h1 className="CC">Address Details</h1>
        <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73]" />
      </div>

      <div className="p-6">
        <ProgressBar steps={["Address", "Package", "Carrier"]} currentStep={0} />
      </div>

      <form>
        {["ship_from_address", "ship_to_address"].map((type, index) => (
          <div key={type} className="mb-6">
            <h1 className="formTitle text-xl font-semibold">{index === 0 ? "From" : "To"}</h1>
              <div className="dropdown">
                <select
                  className="outline-none w-full appearance-none text-gray-500 text-sm px-0 py-0 bg-[#fafafa]"
                  value={formData[`selected${type}Id`] || ""}
                  onChange={(e) => handleSavedAddressChange(e, type)}
                >
                  <option value="">Select Saved Address</option>
                  {savedAddresses.map(addr => (
                    <option key={addr.address_id} value={addr.address_id}>
                      {addr.name}
                    </option>
                  ))}
                </select>
                <div className="pointer-events-none">
                  <FaCaretDown />
                </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              {["Name", "Mobile"].map(field => (
                <input
                  key={field}
                  type="text"
                  name={field}
                  placeholder={field}
                  value={formData[type][field] || ""}
                  onChange={(e) => handleChange(e, type)}
                  className="formContent"
                />
              ))}
            </div>
            
            <div className="grid grid-cols-2 gap-4 mt-4">
              {["Email", "Address"].map(field => (
                <input
                  key={field}
                  type="text"
                  name={field}
                  placeholder={field}
                  value={formData[type][field] || ""}
                  onChange={(e) => handleChange(e, type)}
                  className="formContent"
                />
              ))}
            </div>

            <div className="grid grid-cols-2 gap-4 mt-4">
              {["City", "StateProvinceCode"].map(field => (
                <input
                  key={field}
                  type="text"
                  name={field}
                  placeholder={field}
                  value={formData[type][field] || ""}
                  onChange={(e) => handleChange(e, type)}
                  className="formContent"
                />
              ))}
            </div>

            <div className="grid grid-cols-2 gap-4 mt-4">
              {["CountryCode", "PostalCode"].map(field => (
                <input
                  key={field}
                  type="text"
                  name={field}
                  placeholder={field}
                  value={formData[type][field] || ""}
                  onChange={(e) => handleChange(e, type)}
                  className="formContent"
                />
              ))}
            </div>
          </div>
        ))}

        <div className="flex justify-end">
          <button type="button" className="btn" onClick={() => setCurrentStep(1)}>Next</button>
        </div>
      </form>
    </div>
  );
}

export default OverlayOne;