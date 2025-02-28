// // OverlayThree.jsx

// // !ShippingTable
// import React, { useState } from 'react';
// import { FaTimesCircle, } from 'react-icons/fa';
// import ProgressBar from './ProgressBar';
// import ShippingTable from './ShippingTable';
// import OverlayTwo from './OverlayTwo';
  
// // !CreateCustomer2

//   function OverlayThree({onClose, setCurrentStep, currentStep}){
//     const [formData, setFormData] = useState({});
//   // const [currentStep, setCurrentStep] = useState(1); // Track current step
//   const steps = ['Address', 'Package', 'Carrier'];
//   const [errors, setErrors] = useState({});

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     if (validate()) {
//       console.log('Form submitted:', formData);
//       handleNext();
//     }
//   };

//   const handlePrevious = () => {
//     setCurrentStep(1); // Go back to OverlayTwo
//   };

//   const handleChange = (e) => {
//     setFormData({
//       ...formData,
//       [e.target.name]: e.target.value,
//     });
//   };

//   const validate = () => {
//     const newErrors = {};
//     Object.keys(formData).forEach((key) => {
//       if (!formData[key]) {
//         newErrors[key] = 'This field is required';
//       }
//     });
//     setErrors(newErrors);
//     return Object.keys(newErrors).length === 0;
//   };


//     return (
//       <>
//       <div className='overlay'>
//         <div className='flex justify-between items-center'>
//           <h1 className="CC">Create Quotation</h1>
//           <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73]"/>
//         </div>
//         <div className="p-6">
//           <ProgressBar steps={steps} currentStep={currentStep} />
//         </div>
  
//         <ShippingTable/>
//         <div className='three'>
//         <button type="button" className="btn1" onClick={handlePrevious}>Previous</button>
//         <button type="submit" className="submit" onClick={()=>setCurrentStep(3)}>Proceed</button>
//         <button className='save'>Save</button>
//         </div>
//       </div>
//       </>
//     )
//   }

//   export default OverlayThree


import React, { useState,useEffect } from 'react';
import ProgressBar from './ProgressBar';
import { FaTimesCircle } from 'react-icons/fa';
import ShippingTable from './ShippingTable';

function OverlayThree({ onClose, formData, setFormData, setCurrentStep, shippingRates }) {
  const steps = ['Address', 'Package', 'Carrier'];
  const [selectedRate, setSelectedRate] = useState(null);

  const handlePrevious = () => {
    setCurrentStep(1); // Navigate back to OverlayTwo
  };

  const handleRateSelect = (rate) => {
    setSelectedRate(rate); // Update the selected rate
  };

  const handleSave = () => {
    if (!selectedRate) {
      alert("Please select a shipping rate before saving.");
      return;
    }
    alert("Quotation saved successfully!");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!selectedRate) {
      alert("Please select a shipping rate before proceeding.");
      return;
    }
  
    // Construct the `booking_items` array from formData
    const bookingItems = [
      {
        weight: formData.package_details.weight || 0,
        length: formData.package_details.length || 0,
        width: formData.package_details.width || 0,
        height: formData.package_details.height || 0,
        package_type: formData.package_details.package_type || "Unknown",
        package_cost: formData.package_details.package_cost || 0,
      },
    ];
  
    // Build the complete request body as per FastAPI's schema
    const bookingData = {
      customer_id: 0, // Replace with the actual customer ID if available
      ship_to_address: {
        to_name: formData.ship_to_address.Name,
        to_mobile: formData.ship_to_address.Mobile,
        to_email: formData.ship_to_address.Email,
        to_address: formData.ship_to_address.Address,
        to_city: formData.ship_to_address.City,
        to_state: formData.ship_to_address.StateProvinceCode,
        to_pincode: formData.ship_to_address.PostalCode,
        to_country: formData.ship_to_address.CountryCode,
      },
      ship_from_address: {
        from_name: formData.ship_from_address.Name,
        from_mobile: formData.ship_from_address.Mobile,
        from_email: formData.ship_from_address.Email,
        from_address: formData.ship_from_address.Address,
        from_city: formData.ship_from_address.City,
        from_state: formData.ship_from_address.StateProvinceCode,
        from_pincode: formData.ship_from_address.PostalCode,
        from_country: formData.ship_from_address.CountryCode,
      },
      package_details: {
        carrier_plan: selectedRate.carrier_plan,
        carrier_name: selectedRate.carrier_name,
        service_code: selectedRate.service_code,
        pickup_date: selectedRate.pickup_date || new Date().toISOString().split("T")[0], // Fallback to today's date
        package_count: formData.package_details.package_count || 1,
        est_cost: selectedRate.est_cost || 0,
        total_cost: selectedRate.total_cost || 0,
        est_delivery_date: selectedRate.est_delivery_date || "Unknown",
        booking_date: new Date().toISOString().split("T")[0], // Today's date
        booking_by: "user", // Replace with authenticated user info if applicable
      },
      booking_items: bookingItems, // Add constructed `booking_items` array here
    };
  
    try {
      const response = await fetch("http://127.0.0.1:8000/thisaiapi/bookings/create_booking", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(bookingData),
      });
  
      if (response.ok) {
        alert("Booking created successfully!");
        onClose(); // Close overlay on success
      } else {
        const errorResponse = await response.json();
        alert("Error creating booking: " + (errorResponse.detail || "Unknown error"));
      }
    } catch (error) {
      console.error("Network error:", error);
      alert("An error occurred while submitting the booking. Please try again.");
    }
  };
  
  useEffect(() => {
    console.log("Shipping Rates:", shippingRates);
  }, [shippingRates]);
  

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

        {/* Display shipping rates */}
        {shippingRates?.length > 0 ? (
          <ShippingTable
            shippingRates={shippingRates}
            selectedRate={selectedRate}
            handleRateSelect={handleRateSelect}
          />
        ) : (
          <p>No shipping rates available. Please try again later.</p>
        )}

        {/* Action buttons */}
        <div className="three">
          <button type="button" className="btn1" onClick={handlePrevious}>
            Previous
          </button>
          <button type="submit" className="submit" onClick={handleSubmit}>
            Proceed
          </button>
          <button type="button" className="save" onClick={handleSave}>
            Save
          </button>
        </div>
      </div>
    </div>
  );
}

export default OverlayThree;
