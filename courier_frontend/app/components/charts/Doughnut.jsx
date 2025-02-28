
"use client"
import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import { Chart, ArcElement, Tooltip, Legend } from 'chart.js';
import { FaChartPie } from 'react-icons/fa';

Chart.register(ArcElement, Tooltip, Legend);

const data = {
  labels: ['Picked', 'Transit', 'Delivered'],
  datasets: [
    {
      data: [30, 150, 20], // Example data
      backgroundColor: [
        '#36a2eb', // Blue
        '#ffce56', // Yellow
        '#4bc0c0', // Green
      ],
      borderColor: [
        '#ffffff',
        '#ffffff',
        '#ffffff',
      ],
      borderWidth: 1,
    },
  ],
};

const options = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false,
      position: 'top',
      labels: {
        color: '#000',
      },
    },
  },
};

const DoughnutChart = () => {
  return (
    <div className="flex flex-col w-full h-[300px] max-w-xs p-4 items-center rounded-lg shadow-[0px_0px_1.5px_0px_rgba(0,0,0,0.25)]">
      <div className='flex inline-flex items-start gap-2'>
      <FaChartPie style={{ color: '#4c62b8', fontSize: '18px'}} />
      <h1 className="text-gray-900 font-semibold font-Condensed mb-4">Booking Graph</h1>
      </div>
      
      <div className="flex relative w-[80%] h-80">
        <Doughnut className="" data={data} options={options} />
      </div>
      <div className="flex gap-10 mt-4 inline-flex">
        <div className="flex items-center">
          <div className="w-2 h-2 rounded-full bg-[#36a2eb] mr-2"></div>
          <span className="text-[#888888] text-[12px] font-medium font-['Roboto']">Picked</span>
        </div>
        <div className="flex items-center">
          <div className="w-2 h-2 rounded-full bg-[#ffce56] mr-2"></div>
          <span className="text-[#888888] text-[12px] font-medium font-['Roboto']">Transit</span>
        </div>
        <div className="flex items-center">
          <div className="w-2 h-2 rounded-full bg-[#4bc0c0] mr-2"></div>
          <span className="text-[#888888] text-[12px] font-medium font-['Roboto']">Delivered</span>
        </div>
      </div>
    </div>
  );
};

export default DoughnutChart;
