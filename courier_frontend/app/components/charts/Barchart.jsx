"use client"
import React from 'react';
import { Bar } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import { FaArrowUp, FaWallet } from 'react-icons/fa';

Chart.register(...registerables);

const data = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      data: [10, 30, 50, 70, 90, 110],
      backgroundColor: [
        'rgba(75, 192, 192, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(54, 162, 235, 0.2)',
      ],
      borderColor: [
        'rgba(75, 192, 192, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(54, 162, 235, 1)',
      ],
      borderWidth: 1,
    },
  ],
};

const options = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      display: false,
    },
  },
  scales: {
    y: {
      beginAtZero: false,
    },
  },
};

const ResponsiveBarChart = () => {
  return (
    <div className="w-[100%]  h-[100%] max-w-2xl p-4 rounded-lg shadow-[0px_0px_1.5px_0px_rgba(0,0,0,0.25)]">
      <div className="flex items-center gap-[6px] mb-[2px]">
             <FaWallet style={{ color: '#4c62b8', fontSize: '18px' }} /> 
             <h2 className="text-gray-900 font-semibold font-Condensed"> Income</h2>
           </div>
             <p className="text-gray-900 text-[32px] font-semibold font-Roboto">$20,245</p>
               <div className='flex items-center gap-[5px] mt-2 mb-2'>
               <button className='flex h-[21px] p-1 bg-[#e8fff4] rounded-[156.74px] border border-[#1dbf73] text-[#1dbf73] text-[10px] items-center'>< FaArrowUp style={{fontSize: '15px', color: '#1DBF73'}}/>12%</button>
            <p>vs last years</p>
            </div>
      <div className="w-[70%] h-full">
      {/* <div className="flex relative w-[100%] h-50"> */}
        <Bar data={data} options={options} />
      </div>
    </div>
  );
};

export default ResponsiveBarChart;
