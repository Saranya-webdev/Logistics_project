// "use client";

// import React from "react";
// import CreateForm from "../CreateForm/Create"; // Ensure correct path
// import EditForm from "../EditForm/Edit"; // Ensure correct path
// import OverlayOne from "./OverlayOne";

// const Modal = ({ isVisible, onClose, entityType, isEditing, formData }) => {
//   if (!isVisible) return null;

//   return (
//     <div className="modal-overlay" onClick={onClose}>
//       <div className="modal-content" onClick={(e) => e.stopPropagation()}>
//         {entityType === "booking" ? (
//           <OverlayOne onClose={onClose} />
//         ) : isEditing ? (
//           <EditForm entityType={entityType} formData={formData} onClose={onClose} />
//         ) : (
//           <CreateForm entityType={entityType} onClose={onClose} />
//         )}
//       </div>
//     </div>
//   );
// };

// export default Modal;

// updated code:

// "use client";

// import React from "react";
// import EntityForm from "../CreateForm/Create"; // Ensure correct path
// import OverlayOne from "./OverlayOne";

// const Modal = ({ isVisible, onClose, entityType, initialData }) => { // Receive initialData
//   if (!isVisible) return null;

//   return (
//     <div className="modal-overlay" onClick={onClose}>
//       <div className="modal-content" onClick={(e) => e.stopPropagation()}>
//         {entityType === "booking" ? (
//           <OverlayOne onClose={onClose} />
//         ) : (
//           <EntityForm entityType={entityType} onClose={onClose} initialData={initialData}/> // Pass initialData to Edit
//         )}
//       </div>
//     </div>
//   );
// };

// export default Modal;


"use client";

import React from "react";
import EntityForm from "../CreateForm/Create"; // Ensure correct path
// import OverlayOne from "./OverlayOne";
import CreateBooking from "../CreateBookings/CreateBooking";

const Modal = ({ isVisible, onClose, entityType, initialData, children }) => { // Receive initialData
  if (!isVisible) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {entityType === "booking" ? (
          <CreateBooking onClose={onClose} />
        ) : (
          <EntityForm entityType={entityType} onClose={onClose} initialData={initialData}/>
        )}
         {children}
      </div>
    </div>
  );
};

export default Modal;





