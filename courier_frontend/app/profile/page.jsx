

import React from 'react'
import Image from "next/image";
import { FaArrowRight, FaEdit } from "react-icons/fa";


export default function Profile() {

  return (
    <>
    <div className="flex flex-col bg-white h-[100%] w-[100%] rounded-[12px]">
        <div className="w-full h-[100px] bg-gradient-to-r from-[#DFF3FF]  via-[#04B0F3] to-[#0070A9] rounded-t-xl"></div>
        <div className="flex flex-col h-full p-5 mt-13 ">
            <div className="flex w-full justify-between items-center mb-8">
                <div className="flex items-center gap-[22px] ">
                <Image src="/image.png" alt="logo" width={90} height={90}/>
                    <div>
                       <h1 className="text-gray-900 text-[25px] font-medium font-Roboto">Ananya</h1>
                       <p className="text-[#718096] text-lg font-normal font-Condensed">anan001@gmail.com</p>
                    </div>
                </div>
                <button className="flex justify-start items-center h-12 px-[22px] py-3 rounded-xl gap-3 text-white text-base font-medium font-Roboto bg-[#074e73]"><FaArrowRight/>Logout</button>
            </div>

            <div className="relative w-100% h-100% px-4 py-5 bg-[#f1f4f7] rounded-[10px] justify-start">
                <div className="flex flex-col bg-white p-6">
                    <h1 className="text-[#4972b4] text-xl font-bold font-Condensed mb-4">Information</h1>
                    <div className="flex gap-[64px] mb-4">
                        <div className="flex flex-col gap-1">
                        <p className="text-[#718096] text-[14px] font-normal font-Inria">Name</p>
                        <h1 className="text-gray-900 text-[14px] font-normal font-Mono">Ananya</h1> 
                        </div>

                        <div className="flex flex-col gap-1">
                        <p className="text-[#718096] text-[14px] font-normal font-Inria">Mobile</p>
                        <h1 className="text-gray-900 text-[14px] font-normal font-Mono">9992057859</h1> 
                        </div>

                        <div className="flex flex-col gap-1">
                        <p className="text-[#718096] text-[14px] font-normal font-Inria">Email</p>
                        <h1 className="text-gray-900 text-[14px] font-normal font-Mono">ana@gmail.com</h1> 
                        </div>

                        <div className="flex flex-col gap-1">
                        <p className="text-[#718096] text-[14px] font-normal font-Inria">Address</p>
                        <h1 className="text-gray-900 text-[14px] font-normal font-Mono">24XYZ, A2D street, Chennai, Tamil Nadu</h1> 
                        </div>

                        <div className="flex flex-col gap-1">
                        <p className="text-[#718096] text-[14px] font-normal font-Inria">City</p>
                        <h1 className="text-gray-900 text-[14px] font-normal font-Mono">Chennai</h1> 
                        </div>

                        <div className="flex flex-col gap-1">
                        <p className="text-[#718096] text-[14px] font-normal font-Inria">State</p>
                        <h1 className="text-gray-900 text-[14px] font-normal font-Mono">Tamil Nadu</h1> 
                        </div>

                        <div className="flex flex-col gap-1">
                        <p className="text-[#718096] text-[14px] font-normal font-Inria">Country</p>
                        <h1 className="text-gray-900 text-[14px] font-normal font-Mono">India</h1> 
                        </div>


                        
                    </div>

                    <div className="flex gap-[64px]">
                        <div className="flex flex-col gap-1">
                        <p className="text-[#718096] text-[14px] font-normal font-Inria">Pincode</p>
                        <h1 className="text-gray-900 text-[14px] font-normal font-Mono">600028</h1> 
                        </div>

                        <div className="flex flex-col gap-1">
                        <p className="text-[#718096] text-[14px] font-normal font-Inria">Geolocation</p>
                        <h1 className="text-gray-900 text-[14px] font-normal font-Mono">24XYZ, A2D street, Chennai, Tamil Nadu</h1> 
                        </div>
                    </div>

                </div>

            </div>
            
            <div className="flex gap-4 mt-8 ml-[870px]">
            <button className="flex justify-start items-center h-12 px-[60px] py-3 rounded-xl gap-3 text-white text-base font-medium font-Roboto bg-[#074e73]"><FaEdit/>Edit</button>
            <button className="flex justify-start items-center h-12 px-[60px] py-3 rounded-xl gap-3 text-[#074e73] text-base font-medium font-Roboto border border-[#074e73]">Delete</button>
            </div>
            </div>

    </div>
    </>
  )
}