
import React from 'react';
// import { Bar } from 'react-chartjs-2';
import { FaEye, FaDollarSign } from 'react-icons/fa';
import Chart from './Charts/Chart';
import Barchart from './Charts/Barchart';

const Both = () => {
  return (
    <div className="container mx-auto p-4 md:p-6 md:flex-col lg:p-2">
      <div className="flex items-center justify-start mb-4 gap-4">
        <h1 className="text-gray-900 text-xl font-bold font-Mono">Sujatha</h1>
        <div className="flex gap-4">
          <FaEye className="text-xl text-[#074E73]" />
          <FaDollarSign className="text-xl text-[#074E73]" />
        </div>
      </div>
      <div className="flex flex-wrap justify-space-between md:gap-6 w-full md:w-full lg:gap-8">
        <div className="w-full md:w-1/2 lg:w-1/3">
          <Chart />
        </div>
        <div className="w-full md:w-1/2 lg:w-1/2">
          <Barchart />
        </div>
      </div>
    </div>
  );
};

export default Both;