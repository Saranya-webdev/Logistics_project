// import React, { useState } from 'react'; 
// import ProgressBar from './ProgressBar'; 
// import OverlayThree from './OverlayThree'; 
// import OverlayOne from './OverlayOne'; 
// import { FaTimesCircle, FaCaretDown } from 'react-icons/fa';

// function OverlayTwo({ onClose, formData, setFormData, setCurrentStep }) {
//   const [currentStep, setCurrentStepLocal] = useState(1); // Track current step
//   const steps = ['Address', 'Package', 'Carrier'];
//   const [errors, setErrors] = useState({});
//   const [selectedPackageType, setSelectedPackageType] = useState("");
//   const [numPackages, setNumPackages] = useState(1); // Default to 1 package

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     if (validate()) {
//       console.log('Form submitted:', formData);
//       handleNext();
//     }
//   };

//   const handleNext = () => {
//     if (validate()) {
//       setCurrentStepLocal((prevStep) => prevStep + 1); // Move to next step
//     }
//   };

//   const handlePrevious = () => {
//     if (currentStep > 1) {
//       setCurrentStepLocal((prevStep) => prevStep - 1);
//     } else {
//       setCurrentStep(0); // Move back to OverlayOne
//     }
//   };
  

//   const handleChange = (e) => {
//     const { name, value } = e.target;
    
//     setFormData((prevData) => ({
//       ...prevData,
//       [name]: value,
//     }));
//     // Update number of packages
//     if (name === "noOfPackages") {
//       const count = parseInt(value, 10) || 1;
//       setNumPackages(count);
//       setFormData((prevData) => ({
//         ...prevData,
//         noOfPackages: count, // Ensure formData updates with a default of 1
//       }));
//     }
    

//     // Update the package type selection
//     if (name === "packageType") {
//       setSelectedPackageType(value);
//     }
//   };
  
//   const validate = () => {
//     const newErrors = {};
  
//     // Validate dynamically generated fields for each package
//     for (let i = 0; i < numPackages; i++) {
//       if (!formData[`length_${i}`]) {
//         newErrors[`length_${i}`] = "Length is required";
//       }
//       if (!formData[`width_${i}`]) {
//         newErrors[`width_${i}`] = "Width is required";
//       }
//       if (!formData[`height_${i}`]) {
//         newErrors[`height_${i}`] = "Height is required";
//       }
//       if (!formData[`grossWeight_${i}`]) {
//         newErrors[`grossWeight_${i}`] = "Gross weight is required";
//       }
//       if (!formData[`packageType_${i}`]) {
//         newErrors[`packageType_${i}`] = "Package type is required";
//       }
//     }
  
//     setErrors(newErrors);
//     return Object.keys(newErrors).length === 0; // Return true if no errors
//   };
  
//   return (
//     <>  
//       <div className='overlay w-[1004px]'>
//         <div className='flex justify-between items-center'>
//           <h1 className="CC">Create Quotation</h1>
//           <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73]" />
//         </div>
//         <div className='flex flex-col justify-center items-center'>
//           <div className='p-6'>
//             <ProgressBar steps={steps} currentStep={currentStep} />
//           </div>

//           {currentStep === 0 && <OverlayOne onClose={onClose} />}
//           {currentStep === 1 && (
//             <form onSubmit={handleSubmit}>
//               <div className='flex flex-col'>
//                 <h1 className="formTitle text-xl font-semibold font-['Roboto Condensed']">Package Details</h1>
//                 <div className='flex justify-between gap-5'>
//                   <div>
//                     <input
//                       className="formContent1 bg-transparent"
//                       type="number"
//                       placeholder="No. of Packages"
//                       name="noOfPackages"
//                       min="1"
//                       value={formData.noOfPackages || "1"}
//                       onChange={handleChange}
//                     />
//                     {errors.noOfPackages && <p className="text-red-500 text-sm ml-3">{errors.noOfPackages}</p>}
//                   </div>
//                 </div>
//               </div>

//               {/* Generate item input fields dynamically */}
//               {[...Array(numPackages)].map((_, index) => (
//                 <div key={index}>
//                   <h1 className="formTitle mt-[26px] text-xl font-semibold font-['Roboto Condensed']">Item {index + 1}</h1>
//                   <div className='flex justify-between gap-[10px] mb-4'>
//                     <div>
//                       <input
//                         className="formContent1 bg-transparent"
//                         type="text"
//                         placeholder="Length"
//                         name={`length_${index}`}
//                         value={formData[`length_${index}`] || ""}
//                         onChange={handleChange}
//                       />
//                       {errors[`length_${index}`] && <p className="text-red-500 text-sm ml-3">{errors[`length_${index}`]}</p>}
//                     </div>
//                     <div>
//                       <input
//                         className="formContent1 bg-transparent"
//                         type="text"
//                         placeholder="Width"
//                         name={`width_${index}`}
//                         value={formData[`width_${index}`] || ""}
//                         onChange={handleChange}
//                       />
//                       {errors[`width_${index}`] && <p className="text-red-500 text-sm ml-3">{errors[`width_${index}`]}</p>}
//                     </div>
//                     <div>
//                       <input
//                         className="formContent1 bg-transparent"
//                         type="text"
//                         placeholder="Gross Weight"
//                         name={`grossWeight_${index}`}
//                         value={formData[`grossWeight_${index}`] || ""}
//                         onChange={handleChange}
//                       />
//                       {errors[`grossWeight_${index}`] && <p className="text-red-500 text-sm ml-3">{errors[`grossWeight_${index}`]}</p>}
//                     </div>
//                   </div>

//                   <div className='flex justify-between gap-[10px] mb-4'>
//                     <div>
//                       <input
//                         className="formContent1 bg-transparent"
//                         type="text"
//                         placeholder="Height"
//                         name={`height_${index}`}
//                         value={formData[`height_${index}`] || ""}
//                         onChange={handleChange}
//                       />
//                       {errors[`height_${index}`] && <p className="text-red-500 text-sm ml-3">{errors[`height_${index}`]}</p>}
//                     </div>
//                     <div>
//                       <input
//                         className="formContent1 bg-transparent"
//                         type="text"
//                         placeholder="Volumetric Weight"
//                         name={`volumetricWeight_${index}`}
//                         value={formData[`volumetricWeight_${index}`] || ""}
//                         onChange={handleChange}
//                       />
//                       {errors[`volumetricWeight_${index}`] && <p className="text-red-500 text-sm ml-3">{errors[`volumetricWeight_${index}`]}</p>}
//                     </div>

//                     <div className="flex flex-col w-[200px] relative">
//                       <div className="formContent1 w-full h-12 p-4 bg-transparent rounded-xl flex items-center">
//                         <select
//                           className="bg-[#FAFAFA] outline-none w-full appearance-none text-gray-500"
//                           name={`packageType_${index}`}
//                           value={formData[`packageType_${index}`] || ""}
//                           onChange={handleChange}
//                         >
//                           <option value="" disabled>Package Type</option>  
//                           <option value="Document">Document</option>
//                           <option value="Non-Document">Non-Document</option>
//                         </select>
//                         <div className="absolute right-4 pointer-events-none"><FaCaretDown /></div>
//                       </div>
//                       {errors[`packageType_${index}`] && (
//                         <p className="text-red-500 ml-3 text-sm mt-1">{errors[`packageType_${index}`]}</p>
//                       )}
//                     </div>
//                   </div>
//                 </div>
//               ))}

//               <div className="flex gap-40 mt-10">
//                 <button type="button" className="btn1" onClick={handlePrevious}>Previous</button>
//                 <button type="submit" className="btn2">Next</button>
//               </div>
//             </form>
//           )}

//           {currentStep=== 2 && (
//             <OverlayThree 
//               setCurrentStep={setCurrentStepLocal} 
//               currentStep={currentStep} 
//               onClose={onClose} 
//             />
//           )}
//         </div>
//       </div>
//     </>
//   );
// }

// export default OverlayTwo;


import React, { useState } from 'react';
import { FaTimesCircle } from 'react-icons/fa';
import ProgressBar from './ProgressBar';

// Define validatePayload outside of the OverlayTwo component
const validatePayload = (formData) => {
  const requiredFields = [
    'weight', 'length', 'width', 'height',
    'package_type', 'pickup_date', 'package_count',
  ];
  const errors = [];

  // Validate package_details fields
  requiredFields.forEach((field) => {
    if (!formData.package_details[field]) {
      errors.push(`${field} is required.`);
    }
  });

  // Validate ship_from_address and ship_to_address
  if (!formData.ship_from_address.CountryCode) {
    errors.push('Ship-from Country Code is missing.');
  }
  if (!formData.ship_to_address.CountryCode) {
    errors.push('Ship-to Country Code is missing.');
  }

  return errors;
};

function OverlayTwo({ onClose, setCurrentStep, formData, setFormData }) {
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const steps = ['Address', 'Package', 'Carrier'];

  const handleChange = (e) => {
    const { name, value } = e.target;

    setFormData({
      ...formData,
      package_details: {
        ...formData.package_details,
        [name]: value,
      },
    });
  };

  const validate = () => {
    const newErrors = {};
    const fieldsToValidate = { ...formData.package_details };

    Object.keys(fieldsToValidate).forEach((key) => {
      const value = fieldsToValidate[key];
      if (typeof value === 'string' && !value.trim()) {
        newErrors[key] = 'This field is required';
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = async () => {
    const errors = validatePayload(formData);
    if (errors.length > 0) {
      alert(`Validation Errors:\n${errors.join('\n')}`);
      return;
    }

    // Proceed with API request if no errors
    setLoading(true);
    try {
      console.log('Payload being sent:', formData);
      const response = await fetch('http://127.0.0.1:8000/thisaiapi/bookings/fetch-ups-rates/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      setLoading(false);

      if (response.ok) {
        setCurrentStep(2);
      } else {
        console.error('Backend validation errors:', result);
        let errorMessages = '';
        result.detail.forEach((error) => {
          errorMessages += `${error.loc[1]}: ${error.msg}\n`;
        });
        alert(`Error: \n${errorMessages}`);
      }
    } catch (error) {
      setLoading(false);
      alert('An error occurred while fetching carrier plans. Please try again.');
    }
  };

  return (
    <div className="overlay" id="packageOverlay">
      <div className="flex justify-between items-center">
        <h1 className="CC">Enter Package Details</h1>
        <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73]" />
      </div>
      <div className="p-6">
        <ProgressBar steps={steps} currentStep={1} />
      </div>
      <form>
        {[
          [{ name: 'weight', placeholder: 'Weight' }, { name: 'length', placeholder: 'Length' }],
          [{ name: 'width', placeholder: 'Width' }, { name: 'height', placeholder: 'Height' }],
          [{ name: 'package_type', placeholder: 'Package Type' }, { name: 'pickup_date', placeholder: 'Pickup Date' }],
          [{ name: 'package_count', placeholder: 'Package Count', type: 'number' }],
        ].map((fieldGroup, groupIndex) => (
          <div key={groupIndex} className="flex justify-between gap-5 mb-4">
            {fieldGroup.map((field) => (
              <div key={field.name}>
                <input
                  type={field.type || 'text'}
                  name={field.name}
                  placeholder={field.placeholder}
                  value={formData.package_details[field.name] || ''}
                  onChange={handleChange}
                  className="formContent"
                />
                {errors[field.name] && (
                  <p className="text-red-500 text-sm">{errors[field.name]}</p>
                )}
              </div>
            ))}
          </div>
        ))}
        <div className="flex justify-end">
          <button type="button" className="btn" onClick={handleNext} disabled={loading}>
            {loading ? 'Loading...' : 'Next'}
          </button>
        </div>
      </form>
    </div>
  );
}

export default OverlayTwo;
