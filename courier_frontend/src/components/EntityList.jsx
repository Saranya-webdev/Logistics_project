import React, { useState, useEffect }  from 'react';
import { FaCrown, FaPlus, FaSearch } from 'react-icons/fa';


// const customers = [
//   { name: 'Sujatha', phone: '9992057859', email: 'suja@gmail.com', href:'/dash/Customers/CusDetails', selected: true },
//   { name: 'Adhithya', phone: '9992857859', email: 'adhi@gmail.com', selected: false },
//   { name: 'Ajay Krishna', phone: '9992857859', email: 'ak@gmail.com', selected: false },
//   { name: 'Mukund', phone: '9992857859', email: 'mukundk@gmail.com', selected: false },
//   { name: 'Saranya', phone: '9992857859', email: 'saran@gmail.com', selected: false },
// ];


const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    useEffect(() => {
      // Fetch customers list from backend
      async function fetchCustomers() {
        const response = await fetch('http://127.0.0.1:8000/thisaiapi/customers/customerprofilelist/');
        const data = await response.json();
        setCustomers(data);
      }
      fetchCustomers();
    }, []); // Empty dependency array to run only once

  return ( 
    <div className="max-w-sm mx-auto w-[100%] h-[100%] px-4 py-4 bg-[#F1F4F7] rounded-[10px] flex flex-col md:w-[70%] gap-[2%] items-center m-[0]">
     <div className="flex items-center px-[6%] mb-[2%] h-[3rem] w-full bg-white">
    <FaSearch style={{color: '#111827',fontSize: '20px'}} />
    <input
      type="text"
      placeholder="Search Customer"
      className="w-[100%] p-[2%] outline-none rounded-[10px]"
    />
  </div>
  <ul className="w-full h-100% mb-[2%] flex flex-col gap-[1%]">
    {customers.map((customer, index) => (
      <li
        key={index}
        className={`w-full h-[100%] flex items-start px-3.5 py-3 mb-[1%] border rounded bg-white ${
          customer.selected ? 'border-2 border-[#4c62b8] bg-white' : ''
        }`}>
          
        <div className="w-10 h-10 bg-[#d9d9d9] rounded-full mr-[2%]"></div>
        <div className="flex-1">
          <div className="text-gray-900 text-[1rem] font-bold font-Inria">{customer.name}</div>
          <div className="text-[#718096] text-[1rem] font-normal font-Mono">{customer.phone}</div>
          <div className="text-[#718096] text-[1rem] font-normal font-Mono">{customer.email}</div>
        </div>
        <FaCrown style={{ fontSize: '1.5rem', color: '#4972b4' }} />
      </li>
    ))}
  </ul>
  <button className="h-[6%] px-[5%] py-[2%] text-white bg-[#902f01] rounded-xl flex items-center justify-center mt-[190px]">
    <FaPlus style={{ fontSize: '24px', color: 'white' }} className="mr-[2%]" /> Create
  </button>
  </div>
  )
};

export default CustomerList;