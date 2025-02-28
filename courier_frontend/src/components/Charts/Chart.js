import React from 'react';
import { Doughnut } from 'react-chartjs-2';
import 'chart.js/auto';
import { FaChartPie } from 'react-icons/fa';

const BookingGraph = () => {
  const data = {
    datasets: [
      {
        data: [28, 150, 30], // Example data
        backgroundColor: ['#1E3A8A', '#FBBF24', '#10B981'],
        hoverBackgroundColor: ['#1E3A8A', '#FBBF24', '#10B981'],
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: 'bottom',
        labels: {
          color: '#000',
        },
      },
    },
  };

return (
  <div className="flex flex-col items-left bg-white rounded-lg shadow-custom-glow w-[100%] h-[100%] p-[5%]">
    <div className="flex items-center gap-[3%] mb-[5%]">
      <FaChartPie style={{ color: '#4c62b8', fontSize: '18px'}} />
      <h2 className="text-gray-900 font-semibold font-Condensed">Booking Graph</h2>
    </div>
    <div className='flex flex-col items-center'>
      <div className="mb-[10%] w-[80%] h-[80%]">
        <Doughnut data={data} options={options} />
      </div>
      <div className="flex justify-around gap-[5%] w-full">
        <div className="flex items-center justify-center gap-1">
          <div className="w-[8px] h-[8px] rounded bg-blue-500 mr-[2%]"></div>
          <span className='text-[#888888] text-[0.8rem] font-medium font-Roboto'>Picked</span>
        </div>
        <div className="flex items-center justify-center gap-1">
          <div className="w-[8px] h-[8px] rounded bg-yellow-500 mr-[2%]"></div>
          <span className='text-[#888888] text-[0.8rem] font-medium font-Roboto'>Transit</span>
        </div>
        <div className="flex items-center justify-center gap-1">
          <div className="w-[8px] h-[8px] rounded bg-green-500 mr-[2%]"></div>
          <span className='text-[#888888] text-[0.8rem] font-medium font-Roboto'>Delivered</span>
        </div>
      </div>
    </div>
  </div>
);
};

export default BookingGraph;