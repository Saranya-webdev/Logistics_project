// import React, { useState } from 'react';
// import OverlayOne from '../../components/Overlays/OverlayOne';
// import OverlayTwo from '../../components/Overlays/OverlayTwo';
// import OverlayThree from '../../components/Overlays/OverlayThree';

// const CreateBookingPage = () => {
//   const initialFormData = {
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
//   };

//   const [currentStep, setCurrentStep] = useState(0);
//   const [formData, setFormData] = useState(initialFormData);
//   const [shippingRates, setShippingRates] = useState(null);

//   const handleClose = () => {
//     setCurrentStep(0);
//     setFormData(initialFormData);
//     setShippingRates(null);
//   };

//   const renderOverlay = () => {
//     console.log('FormData before rendering overlay:', formData); // Debug log
//     switch (currentStep) {
//       case 0:
//         return (
//           <OverlayOne
//             onClose={handleClose}
//             formData={formData}
//             setFormData={setFormData}
//             setCurrentStep={setCurrentStep}
//           />
//         );
//       case 1:
//         return (
//           <OverlayTwo
//             onClose={handleClose}
//             formData={formData}
//             setFormData={setFormData}
//             setCurrentStep={setCurrentStep}
//             setShippingRates={setShippingRates}
//           />
//         );
//       case 2:
//         return (
//           <OverlayThree
//             onClose={handleClose}
//             formData={formData}
//             setFormData={setFormData}
//             setCurrentStep={setCurrentStep}
//             shippingRates={shippingRates}
//           />
//         );
//       default:
//         return null;
//     }
//   };

//   return (
//     <div className="p-6 max-w-md mx-auto">
//       <h2 className="text-xl font-bold mb-4">Create Booking</h2>
//       <button
//         className="bg-blue-500 text-white px-4 py-2 rounded"
//         onClick={() => setCurrentStep(0)}
//       >
//         Create Booking
//       </button>
//       {renderOverlay()}
//     </div>
//   );
// };

// export default CreateBookingPage;

// import React, { useState } from 'react';
// import OverlayOne from './OverlayOne';

// function CreateBooking() {
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

//   const handleClose = () => {
//     // Logic to close the overlay
//   };

//   return (
//     <OverlayOne
//       onClose={handleClose}
//       formData={formData}
//       setFormData={setFormData}
//       setCurrentStep={setCurrentStep}
//     />
//   );
// }
// export default CreateBooking;

import React, { useState } from 'react';
import OverlayOne from "../Overlays/OverlayOne";
import OverlayTwo from '../Overlays/OverlayTwo';
import OverlayThree from '../Overlays/OverlayThree';

function ParentOverlayManager({ onClose }) {
  const [currentStep, setCurrentStep] = useState(0);
  const [formData, setFormData] = useState({
    ship_to_address: { Name: '', Mobile: '', Email: '', Address: '', City: '', StateProvinceCode: '', PostalCode: '', CountryCode: '' },
    ship_from_address: { Name: '', Mobile: '', Email: '', Address: '', City: '', StateProvinceCode: '', PostalCode: '', CountryCode: '' },
    package_details: { weight: '', length: '', width: '', height: '', package_type: '', pickup_date: '', package_count: 0 },
  });
  const [shippingRates, setShippingRates] = useState([]);

  const renderCurrentStep = () => {
    switch (currentStep) {
      case 0:
        return (
          <OverlayOne
            onClose={onClose}
            setCurrentStep={setCurrentStep}
            formData={formData}
            setFormData={setFormData}
          />
        );
      case 1:
        return (
          <OverlayTwo
            onClose={onClose}
            setCurrentStep={setCurrentStep}
            formData={formData}
            setFormData={setFormData}
          />
        );
      case 2:
        return (
          <OverlayThree
            onClose={onClose}
            formData={formData}
            setFormData={setFormData}
            setCurrentStep={setCurrentStep}
            shippingRates={shippingRates}
          />
        );
      default:
        return null;
    }
  };

  return <div>{renderCurrentStep()}</div>;
}

export default ParentOverlayManager;
