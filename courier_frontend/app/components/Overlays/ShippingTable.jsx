// import { useState } from 'react';

// const ShippingTable = () => {
//   const items = [
//     { carrier: 'Blue Dart', package: 'Box', estCost: '$20', estDelivery: '02-11-24' },
//     { carrier: 'UPS', package: '', estCost: '', estDelivery: '' },
//     { carrier: 'FedEx', package: '', estCost: '', estDelivery: '' },
//   ];

//   const [selectedItems, setSelectedItems] = useState([]);

//   const handleCheckboxChange = (index) => {
//     setSelectedItems((prevSelected) =>
//       prevSelected.includes(index)
//         ? prevSelected.filter((i) => i !== index)
//         : [...prevSelected, index]
//     );
//   };

//   return (
//     <div className="container mx-auto">
//       <div className="overflow-x-auto">
//         <table className="lg:w-full bg-white h-[422px] w-[600px] flex flex-col">
//           <thead>
//             <tr className="tTitle">
//               <th className="w-[40px]"></th>
//               <th className="">Carrier</th>
//               <th className="ml-24">Package</th>
//               <th className="ml-24">Est. Cost</th>
//               <th className="ml-20">Est. Delivery Date</th>
//             </tr>
//           </thead>
//           <tbody>
//             {items.map((item, index) => (
//               <tr key={index} className="itemText flex items-center">
//                 <td className="checkbox">
//                   <input
//                     type="checkbox"
//                     checked={selectedItems.includes(index)}
//                     onChange={() => handleCheckboxChange(index)}
//                     className=""
//                   />
//                 </td>
//                 <td className="itemList">{item.carrier}</td>
//                 <td className="itemList">{item.package}</td>
//                 <td className="itemList">{item.estCost}</td>
//                 <td className="itemList">{item.estDelivery}</td>
//               </tr>
//             ))}
//           </tbody>
//         </table>
//       </div>
//     </div>
//   );
// };

// export default ShippingTable;


import { useState } from 'react';

function ShippingTable({ shippingRates, selectedRate, handleRateSelect }) {
  // Fallback for empty shippingRates
  if (!shippingRates || shippingRates.length === 0) {
    return <p>No shipping rates available. Please try again later.</p>;
  }

  return (
    <div className="container mx-auto">
      <div className="overflow-x-auto">
        <table className="lg:w-full bg-white border-collapse border border-gray-300">
          <thead>
            <tr className="bg-gray-200 text-left">
              <th className="border border-gray-300 px-4 py-2">Select</th>
              <th className="border border-gray-300 px-4 py-2">Carrier</th>
              <th className="border border-gray-300 px-4 py-2">Transit Time</th>
              <th className="border border-gray-300 px-4 py-2">Total Cost</th>
              <th className="border border-gray-300 px-4 py-2">Est. Delivery Date</th>
            </tr>
          </thead>
          <tbody>
            {shippingRates.map((rate, index) => (
              <tr key={index} className="hover:bg-gray-100">
                <td className="border border-gray-300 px-4 py-2 text-center">
                  <input
                    type="radio"
                    name="rateSelection"
                    checked={selectedRate === rate}
                    onChange={() => handleRateSelect(rate)}
                  />
                </td>
                <td className="border border-gray-300 px-4 py-2">{rate.carrier_name}</td>
                <td className="border border-gray-300 px-4 py-2">{rate.transit_time}</td>
                <td className="border border-gray-300 px-4 py-2">{rate.total_cost}</td>
                <td className="border border-gray-300 px-4 py-2">{rate.est_delivery_date || "N/A"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ShippingTable;


