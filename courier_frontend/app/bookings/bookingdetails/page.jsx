"use client";
import { useSearchParams } from "next/navigation";
import { useEffect, useState,Suspense } from "react";

export default function BookingDetailsReview() {
  return (
    <Suspense fallback={<div>Loading...</div>}>
      <BookingReview />
    </Suspense>
  );
}

function BookingReview() {
  const searchParams = useSearchParams();
  const bookingId = searchParams.get("booking_id");

  const [bookingDetails, setBookingDetails] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!bookingId) {
      setError("No booking ID provided.");
      setLoading(false);
      return;
    }

    async function fetchBookingDetails() {
      try {
        console.log(" Fetching booking details for ID:", bookingId);

        const response = await fetch(
          `http://127.0.0.1:8000/thisaiapi/bookings/allbookingslist/?booking_id=${encodeURIComponent(
            bookingId
          )}`
        );

        if (!response.ok) throw new Error(" Failed to fetch booking details");

        const data = await response.json();
        console.log(" Fetched Booking Details:", data);

        if (data.bookings && data.bookings.length > 0) {
          setBookingDetails(data.bookings[0]); 
        } else {
          console.error(" No booking found for this ID");
          setError("No booking details found.");
        }
      } catch (error) {
        console.error(" Error fetching booking details:", error);
        setError("Failed to fetch booking details.");
      } finally {
        setLoading(false);
      }
    }

    fetchBookingDetails();
  }, [bookingId]); //  Fixed dependency array

  if (loading) return <p className="text-center mt-10">Loading...</p>;
  if (error) return <p className="text-center mt-10 text-red-500">{error}</p>;

  return (
    <div className="w-full h-full flex flex-col gap-4 bg-[#ffffff] px-4 py-4 rounded-xl overflow-y-auto overflow-hidden no-scrollbar">
      {/* Address Details */}
      <div className="flex flex-col w-[660px] mb-11">
            <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
              Address
            </h1>
            <div className="flex gap-[40px]">
              <h1 className="text-[#718096] text-lg font-bold font-Inria">
                From
              </h1>
              <p className="text-gray-900 text-base font-normal font-Mono">
              {bookingDetails?.from_name || "-"} <br />
              {bookingDetails?.from_address || "-"}, <br />
              {bookingDetails?.from_city|| "-"},
              {bookingDetails?.from_state|| "-"}, <br />
               {bookingDetails?.from_pincode|| "-"}, 
               {bookingDetails?.from_country|| "-"}
              
            </p>
        
            <h1 className="text-[#718096] text-lg font-bold font-Inria pl-32">
                To
              </h1>
            <p className="text-gray-900">
            {bookingDetails?.to_name || "-"} <br />
              {bookingDetails?.to_address || "-"}, <br />
              {bookingDetails?.to_city|| "-"}, 
              {bookingDetails?.to_state|| "-"}, <br />
               {bookingDetails?.to_pincode|| "-"}, 
               {bookingDetails?.to_country|| "-"}
            
            </p>
          </div>
        </div>
     

      {/* Package & Instructions */}
      <div className="flex w-full justify-between">
        <div className="flex flex-col w-[35%] gap-[16px]">
        <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
                Package
              </h1>
          <div className="flex flex-col gap-[10px]">
          <div className="flex gap-[120px]">
          <p className="text-[#718096] text-lg font-normal font-Inria">
                    No. of Packages
                  </p>
              <p className="text-gray-900">{bookingDetails?.package_count ?? "-"}</p>
            </div>
            <div className="flex gap-[148px]">
            <p className="text-[#718096] text-lg font-normal font-Inria">
                    Pickup Date
                  </p>
                  <p className="text-gray-900 text-base font-normal font-Mono">{bookingDetails?.pickup_date}</p>
            </div>
            <div className="flex gap-[144px]">
            <p className="text-[#718096] text-lg font-normal font-Inria">
                    Pickup Time
                  </p>
                  <p className="text-gray-900 text-base font-normal font-Mono">{bookingDetails?.pickup_time}</p>

            </div>
            <div className="flex gap-[130px]">
            <p className="text-[#718096] text-lg font-normal font-Inria">
                    Package Type
                  </p>
                  <p className="text-gray-900 text-base font-normal font-Mono px-2 rounded">
  {bookingDetails?.booking_items?.[0]?.package_type ?? "-"}
</p>

            </div>
          </div>
        </div>

        {/* Carrier Plan */}
        <div className="flex flex-col w-[35%] gap-[16px]">
        <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
      Carrier
    </h1>
    <div className="flex flex-col gap-[10px]">
      <div className="flex justify-between">
        <p className="text-[#718096] text-lg font-normal font-Inria">
          Carrier Name
        </p>
        <p className="text-gray-900 text-base font-normal font-Mono">{bookingDetails?.carrier_name}</p>
            </div>
            <div className="flex justify-between">
            <p className="text-[#718096] text-lg font-normal font-Inria">
          Carrier Plan
        </p>
        <p className="text-gray-900 text-base font-normal font-Mono">{bookingDetails?.carrier_plan}</p>
            </div>
            <div className="flex justify-between">
        <p className="text-[#718096] text-lg font-normal font-Inria">
          Est. Cost
        </p>
        <p className="text-gray-900 text-base font-normal font-Mono">${bookingDetails?.total_cost}</p>
            </div>
            <div className="flex justify-between">
        <p className="text-[#718096] text-lg font-normal font-Inria">
          Est. Delivery Date
        </p>
        <p className="text-gray-900 text-base font-normal font-Mono">
                {bookingDetails?.est_delivery_date
                  ? new Date(bookingDetails?.est_delivery_date).toLocaleDateString()
                  : "-"}
              </p>
            </div>
          </div>
        </div>

        <div className="flex flex-col gap-1 w-[25%]">
              <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
                Instructions
              </h1>
              <div className="w-[290px] p-4 bg-neutral-50 rounded-xl shadow-[0px_0px_1px_0px_rgba(0,0,0,0.25)] justify-start items-start">
                Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
                eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim
                ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut
                aliquip
              </div>
            </div>
          </div>


      {/* Item Details */}
      
      <h1 className="text-[#4972b4] text-[22px] font-bold font-Condensed">
  Item 
</h1>
<div className="w-full flex gap-3 bg-[#edf2fa] p-4 rounded-xl shadow-md">
{bookingDetails?.booking_items && bookingDetails?.booking_items.length > 0 ? (
    bookingDetails.booking_items.map((item, index) => (
      <div key={index} className="w-[320px] bg-white p-4 rounded-xl shadow-md flex flex-col gap-2">
        <h1 className="text-[#4972b4] text-[18px] font-bold font-Condensed">
          Item {index + 1}
        </h1>
        <div className="w-full flex flex-col gap-2 pb-2">
          <div className="flex justify-between">
            <p className="text-[#718096] font-Mono">Length:</p>
            <p className="text-gray-900 font-Mono">
              {item.item_length ? `${item.item_length} ${item.item_length_unit || "cm"}` : "-"}
            </p>
          </div>
          <div className="flex justify-between">
            <p className="text-[#718096] font-Mono">Width:</p>
            <p className="text-gray-900 font-Mono">
              {item.item_width ? `${item.item_width} ${item.item_width_unit || "cm"}` : "-"}
            </p>
          </div>
          <div className="flex justify-between">
            <p className="text-[#718096] font-Mono">Height:</p>
            <p className="text-gray-900 font-Mono">
              {item.item_height ? `${item.item_height} ${item.item_height_unit || "cm"}` : "-"}
            </p>
          </div>
          <div className="flex justify-between">
            <p className="text-[#718096] font-Mono">Weight:</p>
            <p className="text-gray-900 font-Mono">
              {item.item_weight ? `${item.item_weight} ${item.item_weight_unit || "kg"}` : "-"}
            </p>
          </div>
        </div>
      </div>
      
    ))
  ) : (
    <p>No booking items found.</p>
  )}
</div>
    </div>
  );
};
