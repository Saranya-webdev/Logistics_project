import React from 'react';
import { Bar } from 'react-chartjs-2';
import { FaArrowUp, FaWallet } from 'react-icons/fa';


const BarChart = () => {
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
        'rgba(12, 89, 141, 0.6)', 
        'rgba(75, 192, 192, 0.2)',
      ],
      borderColor: [
        '#e8e8e8',
      ],
      borderRadius: 10,
    },
  ],
};

const options = { 
    responsive: true, 
    maintainAspectRatio: false, 
    scales: { y: 
        { beginAtZero: false, 
            grid: { display: false,  },
         }, x: { 
            grid: { 
                display: false,  
            }, 
        }, 
    },
 };


return (
    <div className=" bg-white rounded-lg  shadow-custom-glow w-[360px] h-[100%] p-[10px] rounded-[9px] items-center" >
      <div className="flex justify-between items-center mb-4">
        <div>
          <div className="flex items-center gap-[6px] mb-[9px]">
            <FaWallet style={{ color: '#4c62b8', fontSize: '18px' }} /> 
            <h2 className="text-gray-900 font-semibold font-Condensed"> Income</h2>
          </div>
            <p className="text-gray-900 text-[32px] font-semibold font-Roboto">$20,245</p>
              <div className='flex items-center gap-[5px]'>
                <button className='flex h-[21px] p-1 bg-[#e8fff4] rounded-[156.74px] border border-[#1dbf73] text-[#1dbf73] text-[10px] items-center'>< FaArrowUp style={{fontSize: '15px', color: '#1DBF73'}}/>12%</button>
            <p>vs last years</p>
          </div>
        </div>
      </div>
      <div className="relative h-64 w-[350px] h-[130px]">
        <Bar data={data} options={options} />
      </div>
    </div>
  );
};

export default BarChart;