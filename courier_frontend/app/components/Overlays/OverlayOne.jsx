// Hari's overlay one

// import React, { useState } from 'react';
// import ProgressBar from './ProgressBar';
// import OverlayTwo from './OverlayTwo';
// import { FaTimesCircle } from 'react-icons/fa';

// function OverlayOne({ onClose }) {
//   const [formData, setFormData] = useState({
//     nameFrom: '',
//     phoneFrom: '',
//     companyFrom: '',
//     emailFrom: '',
//     addressFrom: '',
//     cityFrom: '',
//     stateFrom: '',
//     countryFrom: 'In',
//     pincodeFrom: '',
//     nameTo: '',
//     phoneTo: '',
//     companyTo: '',
//     emailTo: '',
//     addressTo: '',
//     cityTo: '',
//     stateTo: '',
//     countryTo: '',
//     pincodeTo: '',
//   });

//   const [currentStep, setCurrentStep] = useState(0);
//   const steps = ['Address', 'Package', 'Carrier'];
//   const [errors, setErrors] = useState({});

//   const handleNext = () => {
//     if (validate()) {
//       setCurrentStep(1);
//     }
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
//       const value = formData[key].trim();

//       // Required field validation
//       if (!value) {
//         newErrors[key] = 'This field is required';
//       }

//       // Phone number validation (exactly 10 digits)
//       if (key.includes('phone') && value && (value.length < 10 || value.length > 15 || isNaN(value))) {
//         newErrors[key] = 'Phone number must be between 10 to 15 digits';
//       }
      
//       // Email validation (basic check for @ and .)
//       if (key.includes('email') && value && (!value.includes('@') || !value.includes('.'))) {
//         newErrors[key] = 'Enter a valid email address';
//       }

//     });

//     setErrors(newErrors);
//     return Object.keys(newErrors).length === 0;
//   };

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     if (validate()) {
//       console.log('Form submitted:', formData);
//     }
//   };

//   function nextform() {
//     return <OverlayTwo onClose={onClose} formData={formData} setFormData={setFormData} setCurrentStep={setCurrentStep} />;
//   }

//   return (
//     <div className='overlay' id='mainoverlay'>
//       <div className='flex justify-between items-center'>
//         <h1 className="CC">Create Quotation</h1>
//         <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73]" />
//       </div>
//       <div className="p-6">
//         <ProgressBar steps={steps} currentStep={currentStep} />
//       </div>
      
//       <form onSubmit={handleSubmit}>
//         {['From', 'To'].map((section) => (
//           <div key={section} className='flex flex-col mb-7'>
//             <h1 className="formTitle text-xl font-semibold font-['Roboto Condensed']">{section}</h1>
            
//             {[
//               [
//                 { name: 'name', placeholder: 'Name' },
//                 { name: 'phone', placeholder: 'Phone Number' }
//               ],
//               [
//                 { name: 'company', placeholder: 'Company Name' },
//                 { name: 'email', placeholder: 'Email' }
//               ],
//               [
//                 { name: 'address', placeholder: 'Address (Area and Street)', fullWidth: true }
//               ],
//               [
//                 { name: 'city', placeholder: 'City' },
//                 { name: 'state', placeholder: 'State' }
//               ],
//               [
//                 { name: 'country', placeholder: 'Country' },
//                 { name: 'pincode', placeholder: 'Pincode' }
//               ]
//             ].map((fieldGroup, groupIndex) => (
//               <div key={groupIndex} className={`flex justify-between gap-5 mb-4 ${fieldGroup[0].fullWidth ? 'w-full' : ''}`}>
//                 {fieldGroup.map((field) => (
//                   <div key={field.name} className={field.fullWidth ? 'w-full' : ''}>
//                     <input
//                       className={field.fullWidth ? 'formContent2 w-full' : 'formContent'}
//                       type="text"
//                       name={`${field.name}${section}`}
//                       placeholder={field.placeholder}
//                       value={formData[`${field.name}${section}`] || ""}
//                       onChange={handleChange}
//                     />
//                     {errors[`${field.name}${section}`] && (
//                       <p className="text-red-500 text-sm">{errors[`${field.name}${section}`]}</p>
//                     )}
//                   </div>
//                 ))}
//               </div>
//             ))}
//           </div>
//         ))}

//         <div className='flex justify-end gap-[32px]'>
//           <button type="submit" className="btn" id='nextButton' onClick={handleNext}>Next</button>
//           <button className="btn1" id='addAddressButton'>Add Address Book</button>
//         </div>
//       </form>

//       {currentStep === 1 && nextform()}
//     </div>
//   );
// }

// export default OverlayOne;

// updated code with single page(address,package overlay)
// import React, { useState } from 'react';
// import ProgressBar from './ProgressBar';
// import OverlayTwo from './OverlayTwo';
// import { FaTimesCircle } from 'react-icons/fa';

// function OverlayOne({ onClose }) {
//   const [formData, setFormData] = useState({
//     ship_to_address: {
//       Name: '',
//       Mobile: '',
//       Email: '',
//       Address: '',
//       City: '',
//       StateProvinceCode: '',
//       PostalCode: '',
//       CountryCode: '',
//     },
//     ship_from_address: {
//       Name: '',
//       Mobile: '',
//       Email: '',
//       Address: '',
//       City: '',
//       StateProvinceCode: '',
//       PostalCode: '',
//       CountryCode: '',
//     },
//     package_details: {
//       weight: '',
//       length: '',
//       width: '',
//       height: '',
//       package_type: '',
//       pickup_date: '',
//       package_count: 0,
//     },
//   });
//   const [currentStep, setCurrentStep] = useState(0);
//   const steps = ['Address', 'Package', 'Carrier'];
//   const [errors, setErrors] = useState({});
//   const [loading, setLoading] = useState(false);

//   const handleChange = (e) => {
//     const { name, value } = e.target;
//     const section = name.includes('To') ? 'ship_to_address' : name.includes('From') ? 'ship_from_address' : 'package_details';
//     const key = name.replace('To', '').replace('From', '');

//     setFormData({
//       ...formData,
//       [section]: {
//         ...formData[section],
//         [key]: value,
//       },
//     });
//   };

//   const validate = () => {
//     const newErrors = {};
//     const fieldsToValidate = {
//       ...formData.ship_to_address,
//       ...formData.ship_from_address,
//       ...formData.package_details,
//     };

//     Object.keys(fieldsToValidate).forEach((key) => {
//       const value = fieldsToValidate[key];
//       if (typeof value === 'string' && !value.trim()) {
//         newErrors[key] = 'This field is required';
//       }
//       if (key.includes('Mobile') && value && (value.length < 10 || value.length > 15 || isNaN(value))) {
//         newErrors[key] = 'Phone number must be between 10 to 15 digits';
//       }
//       if (key.includes('Email') && value && (!value.includes('@') || !value.includes('.'))) {
//         newErrors[key] = 'Enter a valid email address';
//       }
//     });
//     setErrors(newErrors);
//     return Object.keys(newErrors).length === 0;
//   };

//   const handleNext = async () => {
//     if (validate()) {
//       setLoading(true);
//       try {
//         const response = await fetch('http://127.0.0.1:8000/thisaiapi/bookings/fetch-ups-rates', {
//           method: 'POST',
//           headers: {
//             'Content-Type': 'application/json',
//           },
//           body: JSON.stringify(formData),
//         });
//         const result = await response.json();
//         setLoading(false);

//         if (response.ok) {
//           setCurrentStep(1);
//         } else {
//           let errorMessages = '';
//           result.detail.forEach((error) => {
//             errorMessages += `${error.loc[1]}: ${error.msg}\n`;
//           });
//           alert(`Error: \n${errorMessages}`);
//         }
//       } catch (error) {
//         setLoading(false);
//         alert('An error occurred while validating the data. Please try again.');
//       }
//     }
//   };

//   const handleSubmit = (e) => {
//     e.preventDefault();
//     handleNext();
//   };

//   function nextform() {
//     return <OverlayTwo onClose={onClose} formData={formData} setFormData={setFormData} setCurrentStep={setCurrentStep} />;
//   }

//   return (
//     <div className='overlay' id='mainoverlay'>
//       <div className='flex justify-between items-center'>
//         <h1 className="CC">Create Quotation</h1>
//         <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73]" />
//       </div>
//       <div className="p-6">
//         <ProgressBar steps={steps} currentStep={currentStep} />
//       </div>
//       <form onSubmit={handleSubmit}>
//         {['From', 'To'].map((section) => (
//           <div key={section} className='flex flex-col mb-7'>
//             <h1 className="formTitle text-xl font-semibold font-['Roboto Condensed']">{section}</h1>
//             {[
//               [{ name: `Name${section}`, placeholder: 'Name' }, { name: `Mobile${section}`, placeholder: 'Phone Number' }],
//               [{ name: `Email${section}`, placeholder: 'Email' }],
//               [{ name: `Address${section}`, placeholder: 'Address', fullWidth: true }],
//               [{ name: `City${section}`, placeholder: 'City' }, { name: `StateProvinceCode${section}`, placeholder: 'State' }],
//               [{ name: `CountryCode${section}`, placeholder: 'Country' }, { name: `PostalCode${section}`, placeholder: 'Pincode' }],
//             ].map((fieldGroup, groupIndex) => (
//               <div key={groupIndex} className={`flex justify-between gap-5 mb-4 ${fieldGroup[0].fullWidth ? 'w-full' : ''}`}>
//                 {fieldGroup.map((field) => (
//                   <div key={field.name} className={field.fullWidth ? 'w-full' : ''}>
//                     <input className={field.fullWidth ? 'formContent2 w-full' : 'formContent'} type="text" name={field.name} placeholder={field.placeholder} value={formData[section === 'From' ? 'ship_from_address' : 'ship_to_address'][field.name.replace(section, '')] || ""} onChange={handleChange} />
//                     {errors[field.name.replace(section, '')] && (
//                       <p className="text-red-500 text-sm">{errors[field.name.replace(section, '')]}</p>
//                     )}
//                   </div>
//                 ))}
//               </div>
//             ))}
//           </div>
//         ))}
//         <h1 className="formTitle text-xl font-semibold font-['Roboto Condensed']">Package Details</h1>
//         <div className='flex flex-col mb-7'>
//           {[
//             [{ name: 'weight', placeholder: 'Weight' }, { name: 'length', placeholder: 'Length' }],
//             [{ name: 'width', placeholder: 'Width' }, { name: 'height', placeholder: 'Height' }],
//             [{ name: 'package_type', placeholder: 'Package Type' }, { name: 'pickup_date', placeholder: 'Pickup Date' }],
//             [{ name: 'package_count', placeholder: 'Package Count', type: 'number' }],
//           ].map((fieldGroup, groupIndex) => (
//             <div key={groupIndex} className={`flex justify-between gap-5 mb-4 ${fieldGroup[0].fullWidth ? 'w-full' : ''}`}>
//               {fieldGroup.map((field) => (
//                 <div key={field.name} className={field.fullWidth ? 'w-full' : ''}>
//                   <input className={field.fullWidth ? 'formContent2 w-full' : 'formContent'} type={field.type || "text"} name={field.name} placeholder={field.placeholder} value={formData.package_details[field.name] || ""} onChange={handleChange} />
//                   {errors[field.name] && (
//                     <p className="text-red-500 text-sm">{errors[field.name]}</p>
//                   )}
//                 </div>
//               ))}
//             </div>
//           ))}
//         </div>
//         <div className='flex justify-end gap-[32px]'>
//           <button type="submit" className="btn" id='nextButton' disabled={loading}>
//             {loading ? 'Loading...' : 'Next'}
//           </button>
//           <button className="btn1" id='addAddressButton'>Add Address Book</button>
//         </div>
//       </form>
//       {currentStep === 1 && nextform()}
//     </div>
//   );
// }

// export default OverlayOne;


import React, { useState } from 'react';
import { FaTimesCircle } from 'react-icons/fa';
import ProgressBar from './ProgressBar';

function OverlayOne({ onClose, setCurrentStep, formData, setFormData }) {
  const [errors, setErrors] = useState({});
  const steps = ['Address', 'Package', 'Carrier'];

  const handleChange = (e) => {
    const { name, value } = e.target;
    const section = name.includes('To') ? 'ship_to_address' : 'ship_from_address';
    const key = name.replace('To', '').replace('From', '');

    setFormData({
      ...formData,
      [section]: {
        ...formData[section],
        [key]: value,
      },
    });
  };

  const validate = () => {
    const newErrors = {};
    const fieldsToValidate = {
      ...formData.ship_to_address,
      ...formData.ship_from_address,
    };

    Object.keys(fieldsToValidate).forEach((key) => {
      const value = fieldsToValidate[key];
      if (typeof value === 'string' && !value.trim()) {
        newErrors[key] = 'This field is required';
      }
      if (key.includes('Mobile') && value && (value.length < 10 || value.length > 15 || isNaN(value))) {
        newErrors[key] = 'Phone number must be between 10 to 15 digits';
      }
      if (key.includes('Email') && value && (!value.includes('@') || !value.includes('.'))) {
        newErrors[key] = 'Enter a valid email address';
      }
    });

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleNext = () => {
    if (validate()) {
      setCurrentStep(1); // Navigate to OverlayTwo
    }
  };

  return (
    <div className="overlay" id="addressOverlay">
      <div className="flex justify-between items-center">
        <h1 className="CC">Enter Address Details</h1>
        <FaTimesCircle onClick={onClose} className="text-xl text-[#074E73]" />
      </div>
      <div className="p-6">
        <ProgressBar steps={steps} currentStep={0} />
      </div>
      <form>
        {['From', 'To'].map((section) => (
          <div key={section} className="flex flex-col mb-7">
            <h1 className="formTitle text-xl font-semibold">{section}</h1>
            {[
              [{ name: `Name${section}`, placeholder: 'Name' }, { name: `Mobile${section}`, placeholder: 'Phone Number' }],
              [{ name: `Email${section}`, placeholder: 'Email' }],
              [{ name: `Address${section}`, placeholder: 'Address', fullWidth: true }],
              [{ name: `City${section}`, placeholder: 'City' }, { name: `StateProvinceCode${section}`, placeholder: 'State' }],
              [{ name: `CountryCode${section}`, placeholder: 'Country' }, { name: `PostalCode${section}`, placeholder: 'Pincode' }],
            ].map((fieldGroup, groupIndex) => (
              <div key={groupIndex} className="flex justify-between gap-5 mb-4">
                {fieldGroup.map((field) => (
                  <div key={field.name} className={field.fullWidth ? 'w-full' : ''}>
                    <input
                      type="text"
                      name={field.name}
                      placeholder={field.placeholder}
                      value={formData[section === 'From' ? 'ship_from_address' : 'ship_to_address'][field.name.replace(section, '')] || ''}
                      onChange={handleChange}
                      className="formContent"
                    />
                    {errors[field.name.replace(section, '')] && (
                      <p className="text-red-500 text-sm">{errors[field.name.replace(section, '')]}</p>
                    )}
                  </div>
                ))}
              </div>
            ))}
          </div>
        ))}
        <div className="flex justify-end">
          <button type="button" className="btn" onClick={handleNext}>
            Next
          </button>
        </div>
      </form>
    </div>
  );
}

export default OverlayOne;
