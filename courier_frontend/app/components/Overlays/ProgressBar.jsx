import React, { useState, useEffect } from 'react';
import { FaCheck } from 'react-icons/fa';

const ProgressBar = ({ steps, currentStep }) => {
  const [widths, setWidths] = useState([]);

  useEffect(() => {
    // Calculate widths based on currentStep
    const newWidths = steps.map((_, index) => {
      if (index < currentStep) {
        return 100; // Full width for completed steps
      } else if (index === currentStep) {
        return 50; // Half width for the current step (adjust as needed)
      } else {
        return 0; // Zero width for future steps
      }
    });
    setWidths(newWidths);
  }, [currentStep, steps]);

  // flex items-center justify-around gap-[10px] w-full

  return (
    <div className="Progress ">
      {steps.map((step, index) => (
        <div key={index} className="flex flex-col items-left">
          <div className="flex items-center">
            <div
              className={`rounded-full h-8 w-8 flex items-center justify-center 
                ${index < currentStep ? 'bg-[#006fa9] text-white' : 'border-2 border-[#006fa9] text-blue-500'}
                ${index === currentStep ? '' : ''}
              `}
            >
              {index < currentStep && <span className="text-white"><FaCheck/></span>}
              {index === currentStep && <div className="rounded-full h-3 w-3 bg-[#006fa9]"></div>}
            </div>
            {index < steps.length - 1 && (
              <div className="h-1 bg-gray-300 w-[120px] relative">
                <div 
                  className="absolute top-0 left-0 h-full bg-[#006fa9]"
                  style={{ width: `${widths[index]}%`}}
                ></div>
              </div>
            )}
          </div>
          <span className={`text-[14px] font-medium mt-2 ${index <= currentStep ? 'text-[#006fa9]' : 'text-gray-500'}`}>
            {step}
          </span>
        </div>
      ))}
    </div>
  );
};

export default ProgressBar;