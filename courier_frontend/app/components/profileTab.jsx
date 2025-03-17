// for seperate edit form

import React,{useState} from "react";
import PropTypes from "prop-types";
import { FaFileAlt, FaEdit } from "react-icons/fa";
// import EntityForm from "./EditForm/Edit";
import EditEntityForm from "./EditForm/Edit";

const ProfileTab = ({ selectedEntity, entityType, setSelectedEntity }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [isActive, setIsActive] = useState(false);
  console.log("Active Flag:", selectedEntity.active_flag);


  if (!selectedEntity) {
    return <div>Loading profile...</div>;
  }

  // Define dynamic fields for different entity types
  const entityLabels = {
    customer: { 
      name: "customer_name", 
      mobile: "customer_mobile", 
      email: "customer_email", 
      city: "customer_city", 
      state: "customer_state", 
      country: "customer_country", 
      pincode: "customer_pincode",
      geolocation:"customer_geolocation", 
      address: "customer_address", 
      type:"customer_type", 
      taxId:"tax_id", 
      licenseNumber:"license_number", 
      designation: "designation",
      companyName: "company_name" 
    },
    agent: { 
      name: "agent_name", 
      mobile: "agent_mobile", 
      email: "agent_email", 
      city: "agent_city", 
      state: "agent_state", 
      country: "agent_country", 
      pincode: "agent_pincode",
      geolocation:"agent_geolocation", 
      address: "agent_address" 
    },
    carrier: { 
      name: "carrier_name", 
      mobile: "carrier_mobile", 
      email: "carrier_email", 
      city: "carrier_city", 
      state: "carrier_state", 
      country: "carrier_country", 
      pincode: "carrier_pincode", 
      geolocation:"carrier_geolocation", 
      address: "carrier_address",
      account_number: "account_number",
      account_name:"account_name"

    }
  };

  const labels = entityLabels[entityType] || {};
  const customerType = selectedEntity[labels.type] || "Personal";

  const toggleActiveStatus = async () => {
    try {
        let newActiveFlag;
        let updateData = {};

        // Define API endpoints and correct email field names for each entity
        const entityEndpoints = {
            customer: { key: "customers", emailField: "customer_email" },
            agent: { key: "agents", emailField: "agent_email" },
            carrier: { key: "carriers", emailField: "carrier_email" },
            associate: { key: "associates", emailField: "associate_email" }
        };

        const entityData = entityEndpoints[entityType]; // Get the correct entity data
        if (!entityData) {
            console.error("Invalid entity type:", entityType);
            alert("Invalid entity type.");
            return;
        }

        const emailField = entityData.emailField; // Correct field name
        const entityKey = entityData.key; // Correct API endpoint

        // Check if email exists in selectedEntity
        if (!selectedEntity[emailField]) {
            alert(`Missing ${emailField} in selected entity.`);
            return;
        }

        // Determine new active_flag
        if (["agent", "carrier", "associate"].includes(entityType)) {
            if (![1, 2].includes(selectedEntity.active_flag)) {
                alert(`Invalid active flag value. Use 1 (Activate) or 2 (Suspend) for ${entityType}.`);
                return;
            }

            newActiveFlag = selectedEntity.active_flag === 1 ? 2 : 1;
            updateData = {
                [emailField]: selectedEntity[emailField], // Use correct field name
                active_flag: newActiveFlag,
                remarks: `Status changed to ${newActiveFlag === 1 ? "Activated" : "Suspended"}`,
            };
        } else if (entityType === "customer") {
            // Handle customer-specific logic
            newActiveFlag = selectedEntity.active_flag === 1 ? 2 : 1;
            updateData = {
                customer_email: selectedEntity.customer_email, // Explicitly use customer_email
                active_flag: newActiveFlag,
                verification_status: newActiveFlag === 1 ? "Verified" : "Pending",
                remarks: `Status changed to ${newActiveFlag === 1 ? "Verified" : "Pending"}`,
            };
        }

        //  Debugging: Log the request body before sending it
        console.log("Sending request body:", JSON.stringify(updateData));

        // Send API request
        const response = await fetch(`http://127.0.0.1:8000/thisaiapi/${entityKey}/suspend-or-activate/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(updateData),
        });

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`HTTP error! Status: ${response.status} - ${errorText}`);
        }

        const data = await response.json();
        console.log("Response:", data);

        // Update UI State
        setSelectedEntity((prevEntity) => ({
            ...prevEntity,
            active_flag: newActiveFlag,
        }));

        // Alert message
        alert(`${newActiveFlag === 1 ? "Activated" : "Suspended"} ${entityType}`);

    } catch (error) {
        console.error("Error:", error);
        alert(`Failed to update status: ${error.message}`);
    }
};


return (
  <div className="w-[734px] h-[100%] rounded-[10px] p-4 bg-[#F1F4F7] overflow-auto"> {/* Added overflow-auto for better handling of content overflow */}
    <div className="flex flex-col w-[100%] rounded-xl h-[100%] p-5 gap-[30px] bg-white">

    {entityType === "carrier" ? (
        // Carrier-specific layout
        <div className="flex flex-wrap gap-12">
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Carrier Name</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">
              {selectedEntity.carrier_name || "N/A"}
            </h1>
          </div>

          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Carrier Address</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">
              {selectedEntity.carrier_address || "N/A"}
            </h1>
          </div>

          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Account Number</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">
              {selectedEntity.account_number || "N/A"}
            </h1>
          </div>

          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Account Name</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">
              {selectedEntity.account_name || "N/A"}
            </h1>
          </div>
        </div>
      ) : (
        // Default layout for other entity types
        <> 




      {/* FIRST ROW */}
      <div className="flex flex-wrap gap-12"> {/* Changed to flex-wrap for better handling of multiple lines */}
        <div className="flex flex-col gap-1.2">
          <p className="text-[#718096] text-[12px] font-normal font-Inria">Mobile</p>
          <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.mobile] ? selectedEntity[labels.mobile] : "N/A"}</h1>
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

        <div className="flex flex-col gap-1.2">
          <p className="text-[#718096] text-xs font-normal font-Inria">Country</p>
          <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.country]}</h1>
        </div>
      </div>

      {/* SECOND ROW */}
      <div className="flex flex-wrap gap-12"> {/* Changed to flex-wrap for better handling of multiple lines */}

        <div className="flex flex-col gap-1.2">
          <p className="text-[#718096] text-xs font-normal font-Inria">Pincode</p>
          <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.pincode]}</h1>
        </div>

        <div className="flex flex-col gap-1.2">
          <p className="text-[#718096] text-xs font-normal font-Inria">Geolocation</p>
          <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.geolocation]}</h1>
        </div>

        <div className="flex flex-col gap-1.2">
          <p className="text-[#718096] text-xs font-normal font-Inria">Address</p>
          <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity[labels.address]}</h1>
        </div>

        <div className="flex flex-col gap-1.2">
          <p className="text-[#718096] text-[12px] font-normal font-Inria">Type</p>
          <h1 className="text-gray-900 text-xs font-bold font-Mono">{customerType}</h1>
        </div>

        {entityType !== "carrier" && (
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-[12px] font-normal font-Inria">Category</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">
              {selectedEntity[`${entityType}_category`] ? selectedEntity[`${entityType}_category`] : "N/A"}
            </h1>
          </div>
        )}
      </div>

      {/* BUSINESS DETAILS - Show only if the customer is Business Type */}
      {customerType === "corporate" && (
        <div className="flex flex-wrap gap-12"> {/* Changed to flex-wrap for better handling of multiple lines */}
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Tax Id</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">
              {selectedEntity.tax_id ? selectedEntity.tax_id : "N/A"}
            </h1>
          </div>
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">License Number</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity.license_number}</h1>
          </div>
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Designation</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity.designation}</h1>
          </div>
          <div className="flex flex-col gap-1.2">
            <p className="text-[#718096] text-xs font-normal font-Inria">Company Name</p>
            <h1 className="text-gray-900 text-xs font-bold font-Mono">{selectedEntity.company_name}</h1>
          </div>
        </div>
      )}
      </>
       )} 


      {/* THIRD ROW */}
      <div className="flex justify-between items-center flex-wrap gap-4"> {/* Added gap-4 for spacing */}
        <div className='flex flex-col gap-2'>
          <p className="text-[#718096] text-xs font-normal font-Inria">Contract Document</p>
          <div className="w-[120px] h-[100px] rounded-xl border-4 border-gray-300"><FaFileAlt className="relative text-[40px] text-[#4972b4] top-[24px] left-[40px]" /></div>
        </div>
        <div className="flex gap-4"> {/* Added gap-4 for spacing between buttons */}
          <button className=" px-6 py-[9px] text-white bg-[#902f01] rounded-lg inline-flex text-sm font-medium font-Roboto" onClick={() => setIsEditing(true)}><FaEdit className="text-white mr-1" />Edit</button>

          {selectedEntity?.active_flag !== undefined && (
            <button 
              className={`px-4 py-[9px] text-white rounded-lg inline-flex text-sm font-medium font-Roboto ${
                selectedEntity.active_flag === 0 || selectedEntity.active_flag === 2 ? "bg-green-600" : "bg-red-600"
              }`}
              onClick={toggleActiveStatus}
            >
              {selectedEntity.active_flag === 0 || selectedEntity.active_flag === 2 ? "Activate" : "Suspend"}
            </button>
          )}
        </div>
      </div>

      {isEditing && (
        <EditEntityForm
          entityType={entityType}
          onClose={() => setIsEditing(false)}
          initialData={selectedEntity}
        />
      )}
    </div>
  </div>
);

};

ProfileTab.propTypes = {
  selectedEntity: PropTypes.object,
  entityType: PropTypes.string.isRequired, 
};

export default ProfileTab;
