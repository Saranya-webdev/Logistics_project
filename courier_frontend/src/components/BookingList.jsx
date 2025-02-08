import React, { useState, useEffect } from 'react';
import { FaEye } from 'react-icons/fa';

// const bookings = [
//   { from: 'Chennai - 600028', to: 'US - 99950', type: 'Box', status: 'Delivered' },
//   { from: 'Chennai - 600028', to: 'US - 99950', type: 'Box', status: 'Delivered' },
//   { from: 'Chennai - 600028', to: 'US - 99950', type: 'Envelope', status: 'Delivered' },
//   { from: 'Chennai - 600028', to: 'US - 99950', type: 'Box', status: 'Delivered' },
//   { from: 'Chennai - 600028', to: 'US - 99950', type: 'Box', status: 'Delivered' },
// ];

const BookingList = () => {
    const [bookings, setBookings] = useState([]);

    useEffect(() => {
        async function fetchBookings() {
            try {
                const response = await fetch("http://127.0.0.1:8000/thisaiapi/bookings/allbookingslist/");
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const data = await response.json();
                console.log("fetched data:",data)
                setBookings(data.bookings);
            } catch (error) {
                console.error("Failed to fetch bookings:", error);
            }
        }
        fetchBookings();
    }, []); // Empty dependency array to run only once

    if (!Array.isArray(bookings)) {
        return <div>No bookings available</div>;
    }

    return (
        <div className="container mx-auto p-4">
            <h2 className="text-[#4972b4] text-2xl font-bold font-Condensed mb-6">Booking List</h2>
            <div className="overflow-x-auto">
                <table className="min-w-full bg-white border border-gray-200 h-[422px]">
                    <thead>
                        <tr className="bg-[#6aa9cf] text-gray-900 font-bold font-Condensed">
                            <th className="w-[100px] pl-[14px] pr-[90px] border-r border-gray-300 rounded-tl-[10px]">From</th>
                            <th className="w-[16px] pl-[14px] pr-[100px] py-[22px] border-r border-gray-300">To</th>
                            <th className="w-[30px] pl-[14px] pr-[90px] py-[22px] border-r border-gray-300">Type</th>
                            <th className="w-[42px] pl-[14px] pr-[90px] py-[22px] border-r border-gray-300">Status</th>
                            <th className="w-[42px] pl-[14px] pr-[40px] py-[22px] rounded-tr-[10px]">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        {bookings.map((booking, index) => (
                            <tr key={index} className="text-left gap-4 text-gray-800 font-normal font-Mono">
                                <td className="pl-[14px] border-b text-wrap">{booking.from_country} - <br/> {booking.from_pincode}</td>

                                <td className="pl-[14px] py-2 px-4 border-b">{booking.to_country} - <br/>{booking.to_pincode}</td>
                                <td className="py-2 px-4 border-b">{booking.carrier_plan}</td>
                                <td className="py-2 px-4 border-b">{booking.carrier_name}</td>
                                <td className="py-2 px-4 border-b">
                                    <button className="text-[#016290]">
                                        <FaEye />
                                    </button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default BookingList;