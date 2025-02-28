import React from 'react';
import { FaUserCircle, FaBell } from 'react-icons/fa';


const Header = ({ title = "Customers " }) => {
  return (
<header className="flex text-white mb-8 flex md:py-6 lg:py-0 md:flex-collg:flex-row">
  <div className="flex items-center gap-8 pl-14 pr-32">
    <img src="/images/TSLogo.png" alt="Thisai Logo" className="w-36 h-12 "/>
  </div>

  <div className='flex justify-between items-center flex-grow' >
    <div className="text-[#4d1400] text-4xl font-semibold font-['Roboto'] ">
      {title}
    </div>

    <div className="flex items-center space-x-4 pl-6">
      <FaBell className="text-gray-400 h-8 w-8" />
      <FaUserCircle className="text-gray-400 h-8 w-8" />
    </div>
  </div>
</header>


  )
};

export default Header;
