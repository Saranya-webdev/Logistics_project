"use client";
import React, { useState } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  FaTachometerAlt,
  FaTruck,
  FaUsers,
  FaUserTie,
  FaBox,
  FaClipboardList,
  FaUserAlt,
  FaAngleDoubleLeft,
  FaFileAlt
} from "react-icons/fa";

const menuItems = [
  { name: "Dashboard", href: "/dashboard", icon: <FaTachometerAlt className="text-2xl" /> },
  { name: "Tracking", href: "/Tracking", icon: <FaTruck className="text-2xl" /> },
  { name: "Quotations", href: "/quotations", icon: <FaFileAlt className="text-2xl" /> },
  { name: "Customers", href: "/customers", icon: <FaUsers className="text-2xl" /> },
  { name: "Agents", href: "/agents", icon: <FaUserTie className="text-2xl" /> },
  { name: "Carriers", href: "/carriers", icon: <FaBox className="text-2xl" /> },
  { name: "Bookings", href: "/bookings", icon: <FaClipboardList className="text-2xl" /> },
  { name: "Users", href: "/Users", icon: <FaUserAlt className="text-2xl" /> },

];

const Sidebar = () => {
  const pathname = usePathname(); // Get the current route
  const [isOpen, setIsOpen] = useState(true);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="flex flex-col items-center justify-left mr-5 h-[100%]">
      <Link href="/" className="flex items-center justify-center mb-6 gap-5">
        <h1 className="text-[#FA0526] text-4xl font-semibold font-['Roboto']">THISAI</h1>
      </Link>
      <nav
        className={`transition-all duration-300 ${isOpen ? "w-[265px]" : "w-[80px]"} h-[100%] px-5 py-14 gap-4 bg-[#074E73] rounded-[20px] flex flex-col justify-start relative`}
      >
        <FaAngleDoubleLeft
          className={`absolute top-10 -right-3 p-2 text-4xl text-[#074E73] bg-white shadow-[0px_4px_4px_0px_rgba(0,0,0,0.25)] rounded-full cursor-pointer transform transition-transform duration-300 ${!isOpen ? "rotate-180" : ""}`}
          onClick={toggleSidebar}
          aria-label="Toggle Sidebar"
        />
        {menuItems.map((item, index) => {
          const isActive = pathname.startsWith(item.href); // Active if the current path starts with the menu item's href
          return (
            <Link key={index} href={item.href} passHref>
              <div
                className={`flex items-center rounded font-['Roboto'] font-medium px-3 py-2 cursor-pointer transition-colors duration-200 ${
                  isActive ? "text-white" : "text-[#9CA3AF]"
                }`}
              >
                <span className="mr-2">{item.icon}</span>
                <span
                  className={`${
                    !isOpen
                      ? "opacity-0 w-0 ml-2 overflow-hidden whitespace-nowrap transition-all duration-300"
                      : "opacity-100 w-auto ml-2 transition-all duration-300"
                  }`}
                >
                  {item.name}
                </span>
              </div>
            </Link>
          );
        })}
      </nav>
    </div>
  );
};

export default Sidebar;
