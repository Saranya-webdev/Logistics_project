// "use client";

// import React, { useState } from 'react';
// import Barchart from './Barchart';
// import Doughnut from './Doughnut';
// import Modal from "../Overlays/modal";
// import ProfileTab from '../profileTab';
// import { FaEye, FaDollarSign, FaPlus } from 'react-icons/fa';

// function CombinedCharts({ entityType, entityName, selectedEntity }) {
//   const [showProfile, setShowProfile] = useState(false);
//   const [showCharts, setShowCharts] = useState(true);
//   const [showModal, setShowModal] = useState(false);
//   // const [entityType, setEntityType] = useState(null);

//   const handleEyeIconClick = () => {
//     setShowProfile((prev) => !prev);
//     setShowCharts(true);
//   };

//   // Enable profile only for customer, agent, and carrier
//   const isProfileEnabled = ['customer', 'agent', 'carrier'].includes(entityType);

//   return (
//     <div className="w-[600px] flex gap-5 md:w-[100%]">
//       <div className='flex flex-col items-center gap-2 w-full'>
//         {/* HEADER */}
//         <div className='w-full h-full flex justify-between mb-4 gap-4'>
//           <div className='flex items-center gap-4'>
//             <h1 className="text-gray-900 text-xl font-bold font-Mono">{entityName}</h1>

//             {isProfileEnabled && (
//               <div className="flex gap-4">
//                 <FaEye className="text-xl text-[#074E73]" onClick={handleEyeIconClick} />
//                 <FaDollarSign className="text-xl text-[#074E73]" />
//               </div>
//             )}
//           </div>
//           <button onClick={() => setShowModal(true)} className="flex items-center gap-2 h-12 text-white px-[22px] py-4 bg-[#074E73] rounded-xl">
//             <FaPlus style={{ fontSize: '18px', color: 'white' }} /> Create
//           </button>
//         </div>

//         {/* CHARTS & PROFILE */}
//         {/* <div className='grid lg:flex md:grid-cols w-[100%] md:w-[100%] gap-10'>
//           {showProfile && isProfileEnabled && <ProfileTab selectedEntity={selectedEntity} entityType={entityType} />}
//           {showCharts && (
//             <>
//               <Doughnut />
//               <Barchart />
//             </>
//           )}
//         </div> */}

// <div className={`flex ${showProfile ? 'flex-col' : 'flex-row'} w-full gap-10`}>
//   {/* PROFILE TAB - First Row When Visible */}
//   {showProfile && isProfileEnabled && (
//     <div className="w-full">
//       <ProfileTab selectedEntity={selectedEntity} entityType={entityType} />
//     </div>
//   )}
  
//   {/* CHARTS - Stays in 2nd Row if Profile is Open, Otherwise in 1st Row */}
//   <div className="w-full flex gap-5">
//     {showCharts && (
//       <>
//         <Doughnut />
//         <Barchart />
//       </>
//     )}
//   </div>
// </div>

//         {/* MODAL */}
//         <Modal isVisible={showModal} onClose={() => setShowModal(false)} entityType={entityType} />
//       </div>
//     </div>
//   );
// }

// export default CombinedCharts;


// updated code:
"use client";

import React, { useState, useEffect } from 'react';
import Barchart from './Barchart';
import Doughnut from './Doughnut';
import Modal from "../Overlays/modal";
import ProfileTab from '../profileTab';
import { FaEye, FaDollarSign, FaPlus } from 'react-icons/fa';

function CombinedCharts({ entityType, entityName, selectedEntity: initialSelectedEntity }) {
  const [showProfile, setShowProfile] = useState(false);
  const [showCharts, setShowCharts] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [editData, setEditData] = useState(null);
  const [selectedEntity, setSelectedEntity] = useState(initialSelectedEntity || {}); // Initialize with prop or empty object
  // const [entityType, setEntityType] = useState(null); // No longer needed
  // const [entityName, setEntityName] = useState(null);  // No longer needed

  useEffect(() => {
    setSelectedEntity(initialSelectedEntity || {}); // Update selectedEntity when prop changes
  }, [initialSelectedEntity]);

  const handleEyeIconClick = () => {
    setShowProfile((prev) => !prev);
    setShowCharts(true);
  };

  const handleEdit = (isEditing, editData) => {
    setIsEditing(isEditing);
    setEditData(editData);
  };

  const closeModal = () => {
    setIsEditing(false);
    setEditData(null);
  };

  // Enable profile only for customer, agent, and carrier
  const isProfileEnabled = ['customer', 'agent', 'carrier'].includes(entityType);

  const handleCreateClick = () => {
    setShowModal(true);
    // Reset the edit data
    setEditData(null);
  }

  return (
    <div className="w-[600px] flex gap-5 md:w-[100%]">
      <div className='flex flex-col items-center gap-2 w-full'>
        {/* HEADER */}
        <div className='w-full h-full flex justify-between mb-4 gap-4'>
          <div className='flex items-center gap-4'>
            <h1 className="text-gray-900 text-xl font-bold font-Mono">{entityName}</h1>

            {isProfileEnabled && (
              <div className="flex gap-4">
                <FaEye className="text-xl text-[#074E73]" onClick={handleEyeIconClick} />
                <FaDollarSign className="text-xl text-[#074E73]" />
              </div>
            )}
          </div>
          <button onClick={handleCreateClick} className="flex items-center gap-2 h-12 text-white px-[22px] py-4 bg-[#074E73] rounded-xl">
            <FaPlus style={{ fontSize: '18px', color: 'white' }} /> Create
          </button>
        </div>

        {/* CHARTS & PROFILE */}
        <div className={`flex ${showProfile ? 'flex-col' : 'flex-row'} w-full gap-10`}>
          {/* PROFILE TAB - First Row When Visible */}
          {showProfile && isProfileEnabled && (
            <div className="w-full">
              <ProfileTab selectedEntity={selectedEntity} entityType={entityType} handleEdit={handleEdit} />
            </div>
          )}

          {/* CHARTS - Stays in 2nd Row if Profile is Open, Otherwise in 1st Row */}
          <div className="w-full flex gap-5">
            {showCharts && (
              <>
                <Doughnut />
                <Barchart />
              </>
            )}
          </div>
        </div>

        {/* MODAL */}
        <Modal
          isVisible={isEditing || showModal}
          onClose={closeModal}
          entityType={entityType}
          initialData={editData}
        />
         {/* Create Modal */}
         <Modal
          isVisible={showModal && !isEditing}
          onClose={() => setShowModal(false)}
          entityType={entityType}
          initialData={null}
        />
      </div>
    </div>
  );
}

export default CombinedCharts;
