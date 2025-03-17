"use client";
import React, { useState, useEffect } from "react";
import { FaEye } from "react-icons/fa";
import PropTypes from "prop-types";
import { useRouter } from "next/navigation";

const BookingTable = ({ selectedEntity = {}, userType }) => {

  const [bookings, setBookings] = useState([]);
  const router = useRouter();

  useEffect(() => {
    async function fetchBookings() {
      try {
        console.log(" Fetching bookings...");
        console.log("Before fetching: selectedEntity =", selectedEntity || {});
        console.log("Before fetching: userType =", userType);
  
        if (!userType) {
          console.error("userType is missing:", userType);
          return;
        }
  
        if 
          (!selectedEntity || Object.keys(selectedEntity).length === 0) {
            console.warn(" selectedEntity is empty, API call may fail!");
          }
  
        let apiUrl = "";
        const bookingId = selectedEntity?.booking_id
          ? `?booking_id=${selectedEntity.booking_id}`
          : "";
  
        switch (userType) {
          case "customer":
  if (!selectedEntity?.customer_email) {
    console.error(" ERROR: Customer email is missing", selectedEntity);
    return;
  }

            apiUrl = `http://127.0.0.1:8000/thisaiapi/customers/${encodeURIComponent(
              selectedEntity.customer_email
            )}/bookinglist${bookingId}`;
            break;
  
          case "agent":
            if (!selectedEntity?.agent_email) {
              console.error(" ERROR: Agent email is missing");
              return;
            }
            apiUrl = `http://127.0.0.1:8000/thisaiapi/agents/${encodeURIComponent(
              selectedEntity.agent_email
            )}/bookings${bookingId}`;
            break;
  
          case "booking":
            apiUrl = `http://127.0.0.1:8000/thisaiapi/bookings/allbookingslist/${bookingId}`;
            break;
  
          case "quotation":
            apiUrl = `http://127.0.0.1:8000/thisaiapi/quotations/allquotations/${bookingId}`;
            break;
  
          case "carrier":
            if (!selectedEntity?.carrier_email) {
              console.error(" ERROR: Carrier email is missing");
              return;
            }
            apiUrl =  `http://127.0.0.1:8000/thisaiapi/carriers/${encodeURIComponent(selectedEntity.carrier_email)}/profile`;
            break;
  
          default:
            console.error("Invalid userType provided.");
            return;
        }
  
        const response = await fetch(apiUrl);
  
        if (!response.ok) {
          const errorText = await response.text();
          console.error(`${userType} fetch error:`, errorText);
  
          if (errorText.includes("No bookings found")) {
            setBookings([]);
            return;
          }
  
          throw new Error("Network response was not ok");
        }
  
        const data = await response.json();
        console.log("API Response:", data);
  
        if (["quotation", "carrier"].includes(userType)) {
          setBookings(data || []);
        } else {
          if (!data || typeof data !== "object" || !Array.isArray(data.bookings)) {
            console.error(" Invalid API response format:", data);
            setBookings([]);
            return;
          }
          setBookings(data.bookings || []);
        }
      } catch (error) {
        console.error(`Failed to fetch ${userType} data:`, error);
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
      headers: [
        "Booking ID",
        "Tracking ID",
        "From",
        "To",
        "Package Type",
        "Carrier Name",
        "Carrier Plan",
        "Status",
        "Action",
      ],
      fields: [
        "booking_id",
        "tracking_number",
        "from_city",
        "to_city",
        "package_type",
        "carrier_name",
        "carrier_plan",
        "booking_status",
      ],
    },
    carrier: {
      headers: [
        "Carrier Name",
        // "Carrier Plan",
        "Account ID",
        "Account",
        "Amount",
        "Payment Status",
        "Payment Mode",
        "Invoice",
      ],
      fields: [
        "carrier_name",
        // "carrier_plan",
        "account_id",
  "account_name",
  "account_number",
        "payment_status",
        "payment_mode",
        "invoice",
      ],
    },

    quotation: {
      headers: [
        "Quotation Number",
        "From",
        "To",
        "Package Type",
        "Carrier Name",
        "Carrier Plan",
        "Action",
      ],
      fields: [
        "quotation_id",
        "from_pincode",
        "to_pincode",
        "package_details",
        "shipping_rates",
        "shipping_rates",
      ],
    },
  };

  const { headers, fields } = tableConfig[userType] || {
    headers: [],
    fields: [],
  };

  const listTitle =
    userType === "quotation"
      ? "Quotation List"
      : userType === "carrier"
      ? "Payments"
      : "Booking List";

  const noDataMessage =
    userType === "quotation"
      ? "No quotations available"
      : userType === "carrier"
      ? "No payments available"
      : "No bookings available";

  console.log("Selected Entity:", selectedEntity);

  console.log("User Type:", userType);
  console.log("Bookings Data:", bookings);

  return (
    <div className="container mx-auto md:w-[100%]">
      <h1 className="text-[#4972b4] text-2xl font-bold font-Condensed mb-4">
        {listTitle}
      </h1>

      {/* Table Container with Scrollable Body */}
      <div className=" border rounded-lg overflow-hidden">
        <div className="max-h-96 overflow-y-auto no-scrollbar ">
          <table className="min-w-full bg-white border">
            {/* Fixed Table Header */}
            <thead className=" ">
              <tr className="bg-[#4972b4] text-gray-900 font-bold font-Condensed">
                {headers.map((header, index) => (
                  <th
                    key={index}
                    className={`py-2 px-4 border-r border-gray-300 ${
                      index === 0
                        ? "rounded-tl-lg"
                        : index === headers.length - 1
                        ? "rounded-tr-lg"
                        : ""
                    }`}
                  >
                    {header}
                  </th>
                ))}
              </tr>
            </thead>

            {/* Scrollable Table Body */}
            <tbody className="overflow-y-auto">
            {Array.isArray(bookings) && bookings.length > 0 ? (
    bookings.map((booking, index) => (
      <tr key={index} className="text-left text-gray-800 font-normal font-Mono hover:bg-gray-100">
      {fields.map((field, idx) => {
        let cellValue = "N/A";

                      if (userType === "carrier") {
                        switch (field) {
                          case "carrier_name":
                            cellValue = booking.carrier_name || "N/A";
                            break;
                          case "account_id":
                            cellValue = booking.account_id || "N/A";
                            break;
                          case "account_name":
                            cellValue = booking.account_name || "N/A";
                            break;
                          case "account_number":
                            cellValue = booking.account_number || "N/A";
                            break;
                          case "payment_status":
                            cellValue = booking.payment_status || "N/A";
                            break;
                          case "payment_mode":
                            cellValue = booking.payment_mode || "N/A";
                            break;
                          case "invoice":
                            cellValue = booking.invoice || "N/A";
                            break;
                          default:
                            cellValue = booking[field] || "N/A";
                        }
                      } else if (userType === "quotation") {
                        switch (field) {
                          case "from_pincode":
                            cellValue =
                              booking.address?.ship_from?.postal_code || "N/A";
                            break;
                          case "to_pincode":
                            cellValue =
                              booking.address?.ship_to?.postal_code || "N/A";
                            break;
                          case "package_details":
                            cellValue =
                              Array.isArray(booking.package_details) &&
                              booking.package_details.length > 0
                                ? booking.package_details[0]?.package_type ||
                                  "N/A"
                                : "N/A";
                            break;

                          case "shipping_rates":
                            cellValue =
                              Array.isArray(booking.shipping_rates) &&
                              booking.shipping_rates.length > 0
                                ? idx === 4
                                  ? booking.shipping_rates[0]?.carrier_name ||
                                    "UPS"
                                  : booking.shipping_rates[0]?.service_name ||
                                    "N/A"
                                : "N/A";
                            break;

                          default:
                            cellValue = booking[field] || "N/A";
                        }
                      } else if (booking) {
                        switch (field) {
                          case "booking_id":
  cellValue =
    userType === "agent" || userType === "customer" || userType === "carrier" || userType === "booking"
      ? booking?.booking_id || booking?.booking_items?.[0]?.booking_id || "N/A"
      : "N/A";
  break;

                          case "package_type":
                            cellValue =
                              Array.isArray(booking?.booking_items) &&
                              booking?.booking_items.length > 0
                                ? booking?.booking_items[0]?.package_type ||
                                  "N/A"
                                : "N/A";
                            break;

                          case "tracking_number": // Added tracking number case
                            cellValue = booking.tracking_number || "N/A";
                            break;
                          default:
                            cellValue = booking[field] || "N/A";
                        }
                      }

                      return (
                        <td key={idx} className="py-2 px-4 border-b">
                          {cellValue}
                        </td>
                      );
                    })}
                    <td className="py-2 px-4 border-b text-center">
                    <button
  className="text-blue-500 hover:text-blue-700"
  onClick={() => {
    console.log(" Button Clicked! userType:", userType, "Booking:", booking);

    if (!booking) {
      console.error(" Booking object is undefined or null:", booking);
      alert("Error: Booking data is missing!");
      return;
    }

    let currentBookingId = null;

    if (userType === "quotation") {
      // For quotations, check if there is a valid booking ID
      currentBookingId = booking?.quotation_id || null;
    } else if (
      userType === "agent" ||
      userType === "customer" ||
      userType === "carrier" ||
      userType === "booking"
    ) {
      currentBookingId =
        booking?.booking_id ||
        (Array.isArray(booking?.booking_items) &&
          booking.booking_items.length > 0 &&
          booking.booking_items[0]?.booking_id) ||
        null;
    }

    if (!currentBookingId) {
      console.error(" Booking/Quotation ID is missing:", booking);
      alert("Error: ID not found!");
      return;
    }

    console.log("🔍 Navigating to review page with ID:", currentBookingId);

    // Navigate based on userType
    const path =
      userType === "quotation"
        ? `/quotations/review?quotation_id=${encodeURIComponent(currentBookingId)}`
        : `/bookings/bookingdetails?booking_id=${encodeURIComponent(currentBookingId)}`;

    router.push(path);
  }}
>
  <FaEye />
</button>


                    </td>
                  </tr>
                ))
              ) : (
                <tr>
                  <td
                    colSpan={fields.length + 1}
                    className="text-center py-4 text-gray-500 border-b"
                  >
                    {noDataMessage}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

BookingTable.propTypes = {
  selectedEntity: PropTypes.object,
  userType: PropTypes.string.isRequired, // "customer", "agent", "booking" or "quotation"
};

export default BookingTable;
