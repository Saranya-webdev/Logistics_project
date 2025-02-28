// // import React from 'react'
// // import { FaUserCircle, FaBell } from 'react-icons/fa';

// // function Header() {
// //   return (
// //     <div className='flex items-center justify-between mb-8'>
// //         {/* PAGE TITLE */}
// //         <h1 className="text-[#8f0d1f] text-4xl font-semibold font-['Roboto']">Customers</h1>

// //         {/* ICONS */}
// //         <div className="flex items-center space-x-4 pl-6">
// //         <FaBell className="text-gray-400 h-8 w-8" />
// //         <FaUserCircle className="text-gray-400 h-8 w-8" />
// //       </div>
// //     </div>
// //   )
// // }

// // export default Header;

// "use client"; // Ensure it's a client component in Next.js
// import React from "react";
// import { FaUserCircle, FaBell } from "react-icons/fa";
// import { usePathname } from "next/navigation"; // Use Next.js router

// function Header() {
//   const pathname = usePathname(); // Get the current route

//   const pageTitles = {
//     "/customers": "Customers",
//     "/agents": "Agents",
//     "/carriers": "Carriers",
//     "/bookings": "Bookings",
//   };

//   // Get the title or default to "Dashboard"
//   const title = pageTitles[pathname] || "";

//   return (
//     <div className="flex items-center justify-between mb-8">
//       {/* PAGE TITLE */}
//       <h1 className="text-[#074E73] text-4xl font-semibold font-['Roboto']">
//         {title}
//       </h1>

//       {/* ICONS */}
//       <div className="flex items-center space-x-4 pl-6">
//         <FaBell className="text-gray-400 h-8 w-8" />
//         <FaUserCircle className="text-gray-400 h-8 w-8" />
//       </div>
//     </div>
//   );
// }

// export default Header;

"use client";
import React from "react";
import { FaUserCircle, FaBell } from "react-icons/fa";
import { usePathname, useRouter } from "next/navigation";

function Header() {
  const pathname = usePathname();
  const router = useRouter();

  const pageTitles = {
    "/customers": "Customers",
    "/agents": "Agents",
    "/carriers": "Carriers",
    "/bookings": "Bookings",
    "/profile": "Profile",
  };

  const title = pageTitles[pathname] || "";

  return (
    <div className="relative">
      <div className="flex items-center justify-between mb-8">
        {/* PAGE TITLE */}
        <h1 className="text-[#074E73] text-4xl font-semibold font-['Roboto']">
          {title}
        </h1>

        {/* ICONS */}
        <div className="flex items-center space-x-4 pl-6">
          <FaBell className="text-gray-400 h-8 w-8" />
          <FaUserCircle
            className="text-gray-400 h-8 w-8 cursor-pointer"
            onClick={() => router.push("/profile")} // Navigate to Profile page
          />
        </div>
      </div>
    </div>
  );
}

export default Header;


