"use client";

import React, { useState } from 'react';
import { FaTachometerAlt, FaTruck, FaUsers, FaUserTie, FaBox, FaClipboardList, FaUserAlt,  FaAngleDoubleLeft  } from 'react-icons/fa';

const  menuItems = [
              { name: "Dashboard", href: "#dashboard", icon: <FaTachometerAlt className="text-2xl" />, },
              { name: "Tracking", href: "#tracking", icon: <FaTruck className="text-2xl" /> },
              { name: "Customers", href: "#customers", icon: <FaUsers className="text-2xl" />, active: true },
              { name: "Agents", href: "#agents", icon: <FaUserTie className="text-2xl" /> },
              { name: "Carriers", href: "#carriers", icon: <FaBox className="text-2xl" /> },
              { name: "Bookings", href: "#bookings", icon: <FaClipboardList className="text-2xl" /> },
              { name: "Users", href: "#users", icon: <FaUserAlt className="text-2xl" /> },
              ]; 

const Sidebar = () => {
const [isOpen, setIsOpen] = useState(true);

  return (
<nav className={`${isOpen ? 'w-full' : 'w-[64px]'} flex flex-col w-[265px] h-[890px] bg-white gap-3 rounded-2xl px-5 py-5`}>
<FaAngleDoubleLeft
className={`text-xl text-[#074E73] cursor-pointer transform ${!isOpen&& 'rotate-180'}`}
onClick={() =>setIsOpen(!isOpen)}
        aria-label="Toggle Sidebar"
      />
      {menuItems.map((item, index) => (
<a
          key={index}
href={item.href}
className={`flex items-center p-2 rounded font-['Roboto'] text-lg font-medium ${item.active ? 'text-[#902F01]' : 'text-[#718096] hover:text-[#902F01]'} transition-colors duration-200`}
>
<span className="mr-2">{item.icon}</span>
<span className={`${!isOpen&& "hidden"} transition duration-200`}>{item.name}</span>
</a>
      ))}
</nav>
  );
};

export default Sidebar;