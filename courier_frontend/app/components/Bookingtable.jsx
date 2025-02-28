import React, { useState, useEffect } from "react";
import { FaEye } from "react-icons/fa";
import PropTypes from "prop-types";

const BookingTable = ({ selectedEntity, userType }) => {
  const [bookings, setBookings] = useState([]);

  useEffect(() => {
    async function fetchBookings() {
      try {
        if (!userType || !selectedEntity) return; // Prevent accessing properties on null
        console.log(`Fetching bookings for ${userType}:`, selectedEntity);
  
        let apiUrl = "";
  
        if (userType === "customer") {
          if (!selectedEntity.customer_email) {
            console.error("Customer email is missing");
            return;
          }
          apiUrl = `http://127.0.0.1:8000/thisaiapi/customers/${encodeURIComponent(selectedEntity.customer_email)}/bookinglist/`;
        } else if (userType === "agent") {
          if (!selectedEntity.agent_email) {
            console.error("Agent email is missing");
            return;
          }
          apiUrl = `http://127.0.0.1:8000/thisaiapi/agents/${encodeURIComponent(selectedEntity.agent_email)}/bookings/`;
        } else if (userType === "booking") {
          apiUrl = "http://127.0.0.1:8000/thisaiapi/bookings/allbookingslist/";
        }
  
        if (!apiUrl) return;
  
        const response = await fetch(apiUrl);
  
        if (!response.ok) {
          const errorText = await response.text();
          console.error("Booking fetch error:", errorText);
  
          if (errorText.includes("No bookings found")) {
            setBookings([]);
            return;
          }
  
          throw new Error("Network response was not ok");
        }
  
        const data = await response.json();
        console.log("API Response:", data);
  
        setBookings(data.bookings || []);
      } catch (error) {
        console.error("Failed to fetch bookings:", error);
        setBookings([]);
      }
    }
  
    fetchBookings();
  }, [selectedEntity, userType]);
  

  // Define headers and corresponding data fields based on userType
  const tableConfig = {
    customer: {
      headers: ["From", "To", "Type", "Status", "Action"],
      fields: ["from_city", "to_city", "package_type", "booking_status"],
    },
    agent: {
      headers: ["Booking ID", "From", "To", "Type", "Status", "Action"],
      fields: ["booking_id", "from_city", "to_city", "package_type", "booking_status"],
    },
    booking: {
      headers: ["Booking ID", "From", "To", "Type", "Carrier Name", "Carrier Plan", "Status", "Action"],
      fields: ["booking_id", "from_city", "to_city", "package_type",  "carrier_plan","carrier_name", "booking_status"],
    },
  };

  const { headers, fields } = tableConfig[userType] || { headers: [], fields: [] };

  return (
    <div className="container mx-auto p-4 md:w-[100%] no-scrollbar">
      <h1 className="text-[#4972b4] text-2xl font-bold font-Condensed mb-4">Booking List</h1>
      <div className="overflow-y-auto no-scrollbar">
        <table className="min-w-full bg-white border">
          <thead>
            <tr className="bg-[#4972b4] text-gray-900 font-bold font-Condensed">
              {headers.map((header, index) => (
                <th
                  key={index}
                  className={`py-2 px-4 border-r border-gray-300 ${
                    index === 0 ? "rounded-tl-lg" : index === headers.length - 1 ? "rounded-tr-lg" : ""
                  }`}
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {bookings.length > 0 ? (
              bookings.map((booking, index) => (
                <tr key={index} className="text-left text-gray-800 font-normal font-Mono hover:bg-gray-100">
                  {fields.map((field, idx) => (
                 <td key={idx} className="py-2 px-4 border-b">
                 {field === "booking_id"
                   ? userType === "agent"
                     ? booking.booking_id || "N/A"
                     : booking.booking_items?.length > 0
                     ? booking.booking_items[0].booking_id
                     : "N/A"
                   : field === "package_type"
                   ? booking.booking_items?.length > 0
                     ? booking.booking_items[0].package_type
                     : "N/A"
                   : booking[field] || "N/A"}
               </td>
               
               
                  ))}
                  <td className="py-2 px-4 border-b text-center">
                    <button className="text-blue-500 hover:text-blue-700">
                      <FaEye />
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={headers.length} className="text-center py-4 text-gray-500">
                  No bookings available
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

BookingTable.propTypes = {
  selectedEntity: PropTypes.object,
  userType: PropTypes.string.isRequired, // "customer", "agent", or "booking"
};

export default BookingTable;


// for service.jsx's booking table

// import React, { useEffect } from "react";
// import { FaEye } from "react-icons/fa";
// import PropTypes from "prop-types";

// const BookingTable = ({ selectedEntity, userType, bookings }) => {
//   useEffect(() => {
//     console.log("Updated bookings:", bookings);
//   }, [bookings]);

//   const tableConfig = {
//     customer: {
//       headers: ["From", "To", "Type", "Status", "Action"],
//       fields: ["from_city", "to_city", "package_type", "booking_status"],
//     },
//     agent: {
//       headers: ["Booking ID", "From", "To", "Type", "Status", "Action"],
//       fields: ["booking_id", "from_city", "to_city", "package_type", "booking_status"],
//     },
//     booking: {
//       headers: ["Booking ID", "From", "To", "Type", "Carrier Name", "Carrier Plan", "Status", "Action"],
//       fields: ["booking_id", "from_city", "to_city", "package_type", "carrier_name", "carrier_plan", "booking_status"],
//     },
//   };

//   const { headers, fields } = tableConfig[userType] || { headers: [], fields: [] };

//   return (
//     <div className="container mx-auto p-4 md:w-[100%] no-scrollbar">
//       <h1 className="text-[#4972b4] text-2xl font-bold font-Condensed">Booking List</h1>
//       <div className="overflow-y-auto no-scrollbar">
//         <table className="min-w-full bg-white border">
//           <thead>
//             <tr className="bg-[#4972b4] text-gray-900 font-bold font-Condensed">
//               {headers.map((header, index) => (
//                 <th key={index} className="py-2 px-4 border-r border-gray-300">{header}</th>
//               ))}
//             </tr>
//           </thead>
//           <tbody>
//             {bookings.length > 0 ? (
//               bookings.map((booking, index) => (
//                 <tr key={index} className="text-left text-gray-800 font-normal font-Mono hover:bg-gray-100">
//                    {fields.map((field, idx) => (
//                  <td key={idx} className="py-2 px-4 border-b">
//                  {field === "booking_id"
//                    ? userType === "agent"
//                      ? booking.booking_id || "N/A"
//                      : booking.booking_items?.length > 0
//                      ? booking.booking_items[0].booking_id
//                      : "N/A"
//                    : field === "package_type"
//                    ? booking.booking_items?.length > 0
//                      ? booking.booking_items[0].package_type
//                      : "N/A"
//                    : booking[field] || "N/A"}
//                </td>
//                   ))}
//                   <td className="py-2 px-4 border-b text-center">
//                     <button className="text-blue-500 hover:text-blue-700">
//                       <FaEye />
//                     </button>
//                   </td>
//                 </tr>
//               ))
//             ) : (
//               <tr>
//                 <td colSpan={headers.length} className="text-center py-4 text-gray-500">
//                   No bookings available
//                 </td>
//               </tr>
//             )}
//           </tbody>
//         </table>
//       </div>
//     </div>
//   );
// };

// BookingTable.propTypes = {
//   selectedEntity: PropTypes.object,
//   userType: PropTypes.string.isRequired,
//   bookings: PropTypes.array.isRequired, // Accept bookings as a prop
// };

// export default BookingTable;
