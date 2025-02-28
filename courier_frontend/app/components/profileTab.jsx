// import React,{useState} from "react";
// import PropTypes from "prop-types";
// import { FaFileAlt, FaEdit } from "react-icons/fa";
// // import EntityForm from "./EditForm/Edit";
// import EditEntityForm from "./EditForm/Edit";

// const ProfileTab = ({ selectedEntity, entityType }) => {
//   const [isEditing, setIsEditing] = useState(false);
//   if (!selectedEntity) {
//     return <div>Loading profile...</div>;
//   }

//   // Define dynamic fields for different entity types
//   const entityLabels = {
//     customer: { name: "customer_name", mobile: "customer_mobile", email: "customer_email", city: "customer_city", state: "customer_state", country: "customer_country", pincode: "customer_pincode", address: "customer_address" },
//     agent: { name: "agent_name", mobile: "agent_mobile", email: "agent_email", city: "agent_city", state: "agent_state", country: "agent_country", pincode: "agent_pincode", address: "agent_address" },
//     carrier: { name: "carrier_name", mobile: "carrier_mobile", email: "carrier_email", city: "carrier_city", state: "carrier_state", country: "carrier_country", pincode: "carrier_pincode", address: "carrier_address" }
//   };

//   const labels = entityLabels[entityType] || {};
//   // const entityName = selectedEntity[labels.name] || "Unknown Name";

//   return (
//     <div className="w-[522px] h-[340px] rounded-[10px] p-4 bg-[#F1F4F7]">
//       <div className="flex flex-col w-[100%] rounded-xl h-[100%] p-5 gap-[30px] bg-white">
//         {/* FIRST ROW */}
//         <div className="flex gap-12">
//           {/* <h1 className="font-bold text-xl text-gray-800">{entityName}</h1> */}

//           <div className="flex flex-col gap-1.2">
//           <p className="text-[#718096] text-[12px] font-normal font-Inria">Mobile</p>
//             <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.mobile]}</h1>
//           </div>

//           <div className="flex flex-col gap-1.2">
//           <p className="text-[#718096] text-xs font-normal font-Inria">Email</p>
//           <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.email]}</h1>
//           </div>

//           <div className="flex flex-col gap-1.2">
//           <p className="text-[#718096] text-xs font-normal font-Inria">City</p>
//             <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.city]}</h1>
//           </div>

//           <div className="flex flex-col gap-1.2">
//           <p className="text-[#718096] text-xs font-normal font-Inria">State</p>
//             <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.state]}</h1>
//           </div>
//         </div>

//         {/* SECOND ROW */}
//         <div className="flex gap-[75px]">
//           <div className="flex flex-col gap-1.2">
//           <p className="text-[#718096] text-xs font-normal font-Inria">Country</p>
//           <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.country]}</h1>
//           </div>

//           <div className="flex flex-col gap-1.2">
//           <p className="text-[#718096] text-xs font-normal font-Inria">Pincode</p>
//             <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.pincode]}</h1>
//           </div>

//           <div className="flex flex-col gap-1.2">
//           <p className="text-[#718096] text-xs font-normal font-Inria">Address</p>
//             <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.address]}</h1>
//           </div>
//         </div>
      

//       {/* THIRD ROW */}
//       <div className="flex items-center gap-28">
//           <div className='flex flex-col gap-2'>
//             <p className="text-[#718096] text-xs font-normal font-Inria">Contract Document</p>
//             <div className="w-[120px] h-[100px] rounded-xl border-4 border-gray-300"><FaFileAlt className="relative text-[40px] text-[#4972b4] top-[24px] left-[40px]"/></div>
//           </div>
//           <button className="h-[34px] px-4 py-[9px] text-white bg-[#902f01] rounded-lg justify-start items-center gap-1.5 inline-flex text-sm font-medium font-Roboto" onClick={() => setIsEditing(true)}><FaEdit className="text-white" />Edit</button>
//           </div>
//       </div>
//       {isEditing && (
//         // <EntityForm 
//         //   entityType="customer" 
//         //   onClose={() => setIsEditing(false)} 
//         //   initialData={selectedEntity}
//         // />

//         <EditEntityForm 
//           entityType={entityType}  
//           onClose={() => setIsEditing(false)} 
//           initialData={selectedEntity}
//         />
//       )}
//       </div>
  
//   );
// };

// ProfileTab.propTypes = {
//   selectedEntity: PropTypes.object,
//   entityType: PropTypes.string.isRequired, 
// };

// export default ProfileTab;


// updated code:

import React from "react";
import PropTypes from "prop-types";
import { FaFileAlt, FaEdit } from "react-icons/fa";

const ProfileTab = ({ selectedEntity, entityType, handleEdit }) => {
  // const [isEditing, setIsEditing] = useState(false); // Remove isEditing state
  if (!selectedEntity) {
    return <div>Loading profile...</div>;
  }

  const entityLabels = {
    customer: { name: "customer_name", mobile: "customer_mobile", email: "customer_email", city: "customer_city", state: "customer_state", country: "customer_country", pincode: "customer_pincode", address: "customer_address" },
    agent: { name: "agent_name", mobile: "agent_mobile", email: "agent_email", city: "agent_city", state: "agent_state", country: "agent_country", pincode: "agent_pincode", address: "agent_address" },
    carrier: { name: "carrier_name", mobile: "carrier_mobile", email: "carrier_email", city: "carrier_city", state: "carrier_state", country: "carrier_country", pincode: "carrier_pincode", address: "carrier_address" },
  };

  const labels = entityLabels[entityType] || {};

  const handleEditClick = () => {
    // setIsEditing(true) // Remove setIsEditing
    handleEdit(true, selectedEntity)
  }

  return (
    <div className="w-[522px] h-[340px] rounded-[10px] p-4 bg-[#F1F4F7]">
      <div className="flex flex-col w-[100%] rounded-xl h-[100%] p-5 gap-[30px] bg-white">
        <div className="flex gap-12">
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-[12px] font-normal font-Inria">Mobile</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.mobile]}</h1>
          </div>
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Email</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.email]}</h1>
          </div>
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">City</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.city]}</h1>
          </div>
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">State</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.state]}</h1>
          </div>
        </div>

        <div className="flex gap-[75px]">
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Country</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.country]}</h1>
          </div>
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Pincode</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.pincode]}</h1>
          </div>
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Address</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.address]}</h1>
          </div>
        </div>

        <div className="flex items-center gap-28">
          <div className="flex flex-col gap-2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Contract Document</p>
            <div className="w-[120px] h-[100px] rounded-xl border-4 border-gray-300">
              <FaFileAlt className="relative text-[40px] text-[#4972b4] top-[24px] left-[40px]" />
            </div>
          </div>
          <button
            className="h-[34px] px-4 py-[9px] text-white bg-[#902f01] rounded-lg justify-start items-center gap-1.5 inline-flex text-sm font-medium font-Roboto"
            onClick={handleEditClick}
          >
            <FaEdit className="text-white" />
            Edit
          </button>
        </div>
      </div>
    </div>
  );
};

ProfileTab.propTypes = {
  selectedEntity: PropTypes.object,
  entityType: PropTypes.string.isRequired,
  handleEdit: PropTypes.func.isRequired, // Add the new prop
};

export default ProfileTab;

