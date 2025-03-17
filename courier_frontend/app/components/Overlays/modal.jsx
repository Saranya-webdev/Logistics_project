"use client";

import React from "react";
import CreateForm from "../CreateForm/Create";
import EditForm from "../EditForm/Edit";
import CreateBooking from "../CreateBookings/CreateBooking";
import CreateQuotation from "../CreateQuotation/CreateQuotation"; // Import Quotation Form

const Modal = ({ isVisible, onClose, entityType, isEditing, formData }) => {
  if (!isVisible) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        {entityType === "booking" ? (
          <CreateBooking onClose={onClose} />
        ) : entityType === "quotation" ? (
          <CreateQuotation onClose={onClose} /> // Render Quotation Form
        ) : isEditing ? (
          <EditForm entityType={entityType} formData={formData} onClose={onClose} />
        ) : (
          <CreateForm entityType={entityType} onClose={onClose} />
        )}
      </div>
    </div>
  );
};

export default Modal;
