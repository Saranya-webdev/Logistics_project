// Final code
import React, { useState, useEffect } from 'react';
import { FaTimesCircle, FaCaretDown } from 'react-icons/fa';
import ProgressBar from './ProgressBar';

// Define validatePayload outside of the OverlayTwo component
const validatePayload = (formData) => {
  const errors = [];
  const { package_details, package_count, package_type } = formData;

  if (!formData.ship_from_address?.CountryCode) {
    errors.push("Ship-from Country Code is missing.");
  }
  if (!formData.ship_to_address?.CountryCode) {
    errors.push("Ship-to Country Code is missing.");
  }
  if (!package_count) {
    errors.push("Package Count is required.");
  }
  if (!package_type) {
    errors.push("Package type is required.");
  }

  if (package_count === 1 && !Array.isArray(package_details)) {
    errors.push("Package details should be an array when count is 1.");
  } else if (package_count > 1 && (!Array.isArray(package_details) || package_details.length !== package_count)) {
    errors.push(`Package details array should have ${package_count} items.`);
  }

  if (Array.isArray(package_details)) {
    package_details.forEach((packageDetail, index) => {
      if (formData.package_type === "Document") {
        if (!packageDetail.weight) {
          errors.push(`Weight is required for package ${index + 1}.`);
        }
      } else if (formData.package_type === "Non-Document") {
        if (!packageDetail.weight) {
          errors.push(`Weight is required for package ${index + 1}.`);
        }
        if (!packageDetail.length) {
          errors.push(`Length is required for package ${index + 1}.`);
        }
        if (!packageDetail.width) {
          errors.push(`Width is required for package ${index + 1}.`);
        }
        if (!packageDetail.height) {
          errors.push(`Height is required for package ${index + 1}.`);
        }
      }
    });
  }


  return errors;
};

function OverlayTwo({ onClose, setCurrentStep, formData, setFormData, setShippingRates }) {
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const steps = ['Address', 'Package', 'Carrier'];

  const handleChange = (e, index) => {
    const { name, value } = e.target;
    console.log("Updating:", name, value);


    setFormData((prevFormData) => {
      if (name === "package_type") {
        return {
          ...prevFormData,
          package_type: value,
          package_details: prevFormData.package_details.map((packageDetail) => ({
            ...packageDetail,
            package_type: value,
          })),
        };
      }

    if (name === "pickup_date") {
      const [date, time = "00:00"] = value.split("T"); // Ensure time is always set
      return {
        ...prevFormData,
        pickup_date: date,
        pickup_time: time,
      };
    }
    
    console.log("Pickup Date Updated:", value);

    

    const newDetails = prevFormData.package_details.map((packageDetail, i) =>
      i === index ? { ...packageDetail, [name]: value } : packageDetail
    );

      return {
        ...prevFormData,
        package_details: newDetails,
        [name]: value,
      };
    });
    console.log("Pickup Date Updated:", value);
  };

  const handlePackageCountChange = (e) => {
    if (!e || !e.target) return;
    const packageCount = Number(e.target.value);

    setFormData((prevFormData) => {
      const newPackageDetails = Array.from({ length: packageCount }, (_, index) => ({
        weight: prevFormData.package_details[index]?.weight || '',
        length: prevFormData.package_details[index]?.length || '',
        width: prevFormData.package_details[index]?.width || '',
        height: prevFormData.package_details[index]?.height || '',
        package_type: prevFormData.package_type || '',
      }));

      const newBookingItems = Array.from({ length: packageCount }, (_, index) => ({
        weight: prevFormData.booking_items[index]?.weight || 0,
        length: prevFormData.booking_items[index]?.length || 0,
        width: prevFormData.booking_items[index]?.width || 0,
        height: prevFormData.booking_items[index]?.height || 0,
        package_type: prevFormData.booking_items[index]?.package_type || '',
        package_cost: prevFormData.booking_items[index]?.package_cost || 0,
      }));

      return {
        ...prevFormData,
        package_count: packageCount,
        package_details: newPackageDetails,
        booking_items: newBookingItems,
      };
    });
  };

  const handlePrevious = () => {
    setCurrentStep(0);
  };

  const handleNext = async () => {
    const validationErrors = validatePayload(formData);
    setErrors({});
    if (validationErrors.length > 0) {
      const formattedErrors = validationErrors.reduce((acc, err) => ({ ...acc, [err]: err }), {});
      setErrors(formattedErrors);
      return;
    }
  
    const formattedFormData = {
      ship_to_address: formData.ship_to_address,
      ship_from_address: formData.ship_from_address,
      package_count: formData.package_count,
      pickup_date: formData.pickup_date ? formData.pickup_date.replace(/[-T:]/g, "").substring(0, 8) : "",
      pickup_time: formData.pickup_time ? formData.pickup_time.replace(/[:]/g, "") : "000000",
      package_details: formData.package_details.length > 0 ? formData.package_details : [],
      status: "Unsaved",
    };
  
    console.log('Final Form Data:', formattedFormData);
    setLoading(true);
  
    try {
      const response = await fetch("http://127.0.0.1:8000/thisaiapi/bookings/fetch-ups-rates/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formattedFormData),
      });
  
      const result = await response.json();
      console.log("API Response Type:", typeof result);
      console.log("Full API Response:", JSON.stringify(result, null, 2));
  
      setLoading(false);
  
      let quotationIdString = null;

  
      if (Array.isArray(result) && result.length > 0) {
        quotationIdString = result[0].quotation_id?.toString() || null;
      }
      

      if (quotationIdString) {
        console.log("Stored Quotation ID:", quotationIdString);

        setFormData((prev) => ({
          ...prev,
          quotation_id: quotationIdString,
        }));
        console.log("OverlayTwo FormData:", formData);
        setShippingRates(result);

        setCurrentStep(2);
      } else {
        console.error("quotation_id is missing from API response!", result);
      }
    } catch (error) {
      console.error("Network error:", error);
      alert("An error occurred while fetching carrier plans.");
      setLoading(false);
    }
  };

  

  return (
    <div className="overlay no-scrollbar" id="packageOverlay">
      {/* ... (rest of your OverlayTwo code) */}
      <div className="flex justify-between items-center">
        <h1 className="CC">Package Details</h1>
        <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73]" />
      </div>
      <div className="p-6">
        <ProgressBar steps={steps} currentStep={1} />
      </div>
      <form>
        <div className="flex flex-col">
          <h1 className="formTitle mt-[26px] text-xl font-semibold font-['Roboto Condensed']">
            Package Details
          </h1>
          <div className="flex justify-between items-top">

          <div className="flex flex-col relative ">
          <div className="dropdown">
            <select
              className="outline-none w-[290px] appearance-none bg-[#fafafa] text-gray-500 text-sm px-0 py-0"
              name="package_type"
              value={formData.package_type || ""}
              onChange={handleChange}
            >
              <option value="" disabled>
                Package Type
              </option>
              <option  value="Document">Document</option>
              <option value="Non-Document">Non-Document</option>
            </select>
            <div className="absolute right-4 pointer-events-none">
              <FaCaretDown />
            </div>
          </div>
          {errors['Package type is required'] && (
            <p className="text-red-500 text-sm">
              {errors['Package type is required']}
            </p>
          )}
        </div>

        <input
            type="number"
            name="package_count"
            placeholder="Package Count"
            value={formData.package_count || 1}
            onChange={handlePackageCountChange}
            className="formContent w-[180px]"
            min="1"
          />
          
          </div>
{errors['Package Count is required.'] && (
            <p className="text-red-500 text-sm">
              {errors['Package Count is required.']}
            </p>
          )}
        </div>

        {/* Common Pickup Date Field */}
        <div className="mb-5">
          <h1 className="formTitle mt-15 mb-[15px] text-xl font-semibold font-['Roboto Condensed']">
            Pickup Date
          </h1>
          <input
  type="datetime-local"
  name="pickup_date"
  value={formData.pickup_date ? `${formData.pickup_date}T${formData.pickup_time || "00:00"}` : ""}
  onChange={handleChange}
  className="formContent w-full max-w-[280px]"
/>


          {errors["Pickup Date is required for package 1."] && (
            <p className="text-red-500 text-sm">{errors["Pickup Date is required for package 1."]}</p>
          )}
          
        </div>

        {Array.from({ length: formData.package_count || 1 }).map((_, index) => {
  const packageDetails = formData.package_details?.[index] || {};

  return (
    <div key={index} className="mb-5 mt-6">
      <h1 className="formTitle mt-15 mb-[15px] text-xl font-semibold font-['Roboto Condensed']">
        Item {index + 1}
      </h1>

      {/* Document Package: Only show Weight */}
      {formData.package_type === "Document" ? (
        <div className="flex flex-wrap justify-between gap-2 w-full">
          <div className="relative w-full sm:w-[48%] flex items-center border border-gray-300 rounded-md overflow-hidden bg-gray-100">
            <input
              type="text"
              name="weight"
              placeholder="Weight"
              value={packageDetails.weight || ""}
              onChange={(e) => handleChange(e, index)}
              className="formContent w-full px-3 py-2 outline-none bg-gray-100"
            />
            <select
              name="weight_unit"
              value={packageDetails.weight_unit || "lbs"}
              onChange={(e) => handleChange(e, index)}
              className="bg-gray-100 px-2 py-2 outline-none text-gray-700"
            >
              <option value="lbs">lbs</option>
              <option value="kg">kg</option>
            </select>
          </div>
          {errors?.[index]?.weight && (
            <p className="text-red-500 text-sm">{errors[index].weight}</p>
          )}
        </div>
      ) : (
        // Non-Document Package: Show Length, Width, Height, Weight in 2 per row
        <div>
          {/* First Row: Length & Width */}
          <div className="flex flex-wrap justify-between gap-4 mt-3 mb-4 w-full">
            {["length", "width"].map((field) => (
              <div key={field} className="relative w-full sm:w-[48%] flex items-center  rounded-md overflow-hidden bg-gray-100">
                <input
                  type="text"
                  name={field}
                  placeholder={field.charAt(0).toUpperCase() + field.slice(1)}
                  value={packageDetails[field] || ""}
                  onChange={(e) => handleChange(e, index)}
                  className="formContent w-full px-3 py-2 outline-none bg-gray-100"
                />
                <select
                  name={`${field}_unit`}
                  value={packageDetails[`${field}_unit`] || "in"}
                  onChange={(e) => handleChange(e, index)}
                  className="bg-gray-100 px-2 py-2 outline-none text-gray-700"
                >
                  <option value="in">in</option>
                  <option value="cm">cm</option>
                </select>
              </div>
            ))}
          </div>

          {/* Second Row: Height & Weight */}
          <div className="flex flex-wrap justify-between gap-4 mb-4 w-full">
            {["height", "weight"].map((field) => (
              <div key={field} className="relative w-full sm:w-[48%] flex items-center rounded-md overflow-hidden bg-gray-100">
                <input
                  type="text"
                  name={field}
                  placeholder={field.charAt(0).toUpperCase() + field.slice(1)}
                  value={packageDetails[field] || ""}
                  onChange={(e) => handleChange(e, index)}
                  className="formContent w-full px-3 py-2 outline-none bg-gray-100"
                />
                <select
                  name={`${field}_unit`}
                  value={packageDetails[`${field}_unit`] || (field === "weight" ? "lbs" : "in")}
                  onChange={(e) => handleChange(e, index)}
                  className="bg-gray-100 px-2 py-2 outline-none text-gray-700"
                >
                  {field === "weight" ? (
                    <>
                      <option value="lbs">lbs</option>
                      <option value="kg">kg</option>
                    </>
                  ) : (
                    <>
                      <option value="in">in</option>
                      <option value="cm">cm</option>
                    </>
                  )}
                </select>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
})}


        <div className="flex justify-evenly">
          <button type="button" className="btn1" onClick={handlePrevious}>
            Previous
          </button>
          <button type="button" className="btn" onClick={handleNext} >
            {loading ? 'Loading...' : 'Next'}
          </button>
        </div>
      </form>
      </div>
  );
}

export default OverlayTwo;