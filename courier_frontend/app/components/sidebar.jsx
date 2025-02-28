"use client"
import React, { useState } from 'react';
import Link from 'next/link';
import Image from 'next/image';
import { FaTachometerAlt, FaTruck, FaUsers, FaUserTie, FaBox, FaClipboardList, FaUserAlt, FaAngleDoubleLeft } from 'react-icons/fa';

const menuItems = [
  { name: "Dashboard", href: "/dashboard/", icon: <FaTachometerAlt className="text-2xl" /> },
  { name: "Tracking", href: "/Tracking/TrackingHome", icon: <FaTruck className="text-2xl" /> },
  { name: "Customers", href: "/customers", icon: <FaUsers className="text-2xl" />, active: true },
  { name: "Agents", href: "/agents", icon: <FaUserTie className="text-2xl" /> },
  { name: "Carriers", href: "/carriers", icon: <FaBox className="text-2xl" /> },
  { name: "Bookings", href: "/bookings", icon: <FaClipboardList className="text-2xl" /> },
  { name: "Users", href: "/Users/UsersHome", icon: <FaUserAlt className="text-2xl" /> },
];

const Sidebar = () => {
  const [isOpen, setIsOpen] = useState(true);

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className='flex flex-col items-center justify-left mr-5 h-[100%]'>
      <Link href='/' className="flex items-center justify-center mb-6 gap-5">
        {/* <Image src="/Composs.png" alt="logo" width={50} height={50}/>
        <Image src="/thisai.png" alt="logo" width={80} height={26} className={`${isOpen ? 'lg:block' : 'hidden'}`} /> */}
        <h1 className="text-[#FA0526] text-4xl font-semibold font-['Roboto']">THISAI</h1>
      </Link>
      <nav
        className={`transition-all duration-300 ${isOpen ? 'w-[265px]' : 'w-[80px]'} h-[100%] px-5 py-14 gap-6 bg-[#074E73] rounded-[20px] flex flex-col justify-start relative`}
      >
        <FaAngleDoubleLeft
          className={`absolute top-10 -right-3 p-2 text-4xl text-[#074E73] bg-white  shadow-[0px_4px_4px_0px_rgba(0,0,0,0.25)] rounded-full cursor-pointer transform transition-transform duration-300 ${!isOpen ? 'rotate-180' : ''}`}
          onClick={toggleSidebar}
          aria-label="Toggle Sidebar"
        />
       {menuItems.map((item, index) => (
  <Link key={index} href={item.href} passHref>
    <div
      className={`flex items-center rounded font-['Roboto'] font-medium ${
        item.active ? 'text-[#ffffff]' : 'text-[#9CA3AF] hover:text-[#718096]'
      } transition-colors duration-200`}
    >
      <span className="mr-2">{item.icon}</span>
      <span
        className={`${
          !isOpen
            ? 'opacity-0 w-0 ml-2 overflow-hidden whitespace-nowrap transition-all duration-300'
            : 'opacity-100 w-auto ml-2 transition-all duration-300'
        }`}
      >
        {item.name}
      </span>
    </div>
  </Link>
))}
      </nav>
    </div>
  );
};

export default Sidebar;

