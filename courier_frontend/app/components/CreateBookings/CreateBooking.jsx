import React, { useState, useEffect } from 'react';
import OverlayOne from "../Overlays/OverlayOne";
import OverlayTwo from '../Overlays/OverlayTwo';
import OverlayThree from '../Overlays/OverlayThree';
import BookingReview from '@/app/bookings/bookingdetails/page';

function ParentOverlayManager({ onClose, startFromQuotation = false, quotationData = null }) {
  // Determine initial step based on whether coming from quotation
  const [currentStep, setCurrentStep] = useState(startFromQuotation ? 0 : 0);

  const [formData, setFormData] = useState(() => {
    if (startFromQuotation && quotationData) {
      // Prefill formData with quotation details
      return {
        ...quotationData,
        package_details: quotationData?.package_details?.length > 0 
  ? quotationData.package_details 
  : [{
      weight: '',
      length: '',
      width: '',
      height: '',
      package_type: '',
      pickup_date: '',
    }]
    ,
        booking_items: [],
      };
    }

    // Default formData for new booking
    const initialPackageDetails = Array.from({ length: 1 }, () => ({
      weight: '',
      length: '',
      width: '',
      height: '',
      package_type: '',
      pickup_date: '',
    }));
    return {
      ship_to_address: { Name: '', Mobile: '', Email: '', Address: '', City: '', StateProvinceCode: '', PostalCode: '', CountryCode: '' },
      ship_from_address: { Name: '', Mobile: '', Email: '', Address: '', City: '', StateProvinceCode: '', PostalCode: '', CountryCode: '' },
      package_details: initialPackageDetails,
      package_count: 1,
      booking_items: [],
    };
  });

  const [shippingRates, setShippingRates] = useState([]);

  useEffect(() => {
    console.log("Updated shippingRates in ParentOverlayManager:", shippingRates);
  }, [shippingRates]);

  useEffect(() => {
    if (formData.package_count > 0) {
      setFormData((prevFormData) => {
        const newPackageDetails = Array.from({ length: prevFormData.package_count }, (_, index) => ({
          weight: prevFormData.package_details[index]?.weight || '',
          length: prevFormData.package_details[index]?.length || '',
          width: prevFormData.package_details[index]?.width || '',
          height: prevFormData.package_details[index]?.height || '',
          package_type: prevFormData.package_details[index]?.package_type || '',
          pickup_date: prevFormData.package_details[index]?.pickup_date || '',
        }));

        return {
          ...prevFormData,
          package_details: newPackageDetails,
        };
      });
    }
  }, [formData.package_count]);

  // Function to create booking and shipment label
  const handleFinalSubmission = () => {
    console.log(" Booking Confirmed! Creating shipment label...");
    alert("Booking & Shipment Label Created Successfully!");
    onClose(); // Close the overlay manager
  };

  useEffect(() => {
    console.log("Received quotationData in ParentOverlayManager:", quotationData);
  }, [quotationData]);
  

  // Dynamically render steps
  const renderStep = () => {
    switch (currentStep) {
      case 0:
        return <OverlayOne onClose={onClose} setCurrentStep={setCurrentStep} formData={formData} setFormData={setFormData} />;
      case 1:
        return <OverlayTwo onClose={onClose} setCurrentStep={setCurrentStep} formData={formData} setFormData={setFormData} setShippingRates={setShippingRates} />;
      case 2:
        return <OverlayThree onClose={onClose} formData={formData} setFormData={setFormData} setCurrentStep={setCurrentStep} shippingRates={shippingRates} />;
      case 3:
        return <BookingReview formData={formData} setCurrentStep={setCurrentStep} onClose={onClose} onProceed={handleFinalSubmission} />;
      default:
        return null;
    }
  };

  return <div>{renderStep()}</div>;
}

export default ParentOverlayManager;


