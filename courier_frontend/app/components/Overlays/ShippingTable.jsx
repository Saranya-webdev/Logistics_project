function ShippingTable({ shippingRates, selectedRate, handleRateSelect }) {
  if (!shippingRates || shippingRates.length === 0) {
    return <p>No shipping rates available. Please try again later.</p>;
  }

  return (
    <div className="container mx-auto">
      <div className="overflow-x-auto">
        <table className="lg:w-full bg-white h-[422px] w-[600px] flex flex-col gap-2">
          <thead>
            <tr className="tTitle">
              <th className=" ml-2 mb-2 w-[40px]"></th>
              <th className="">Carrier</th>
              <th className="ml-24">Package</th>
              <th className="ml-20">Est. Delivery Date</th>
              <th className="ml-24">Est. Cost</th>
              
            </tr>
          </thead>
          <tbody>
            {shippingRates.map((rate, index) => (
              <tr
                key={index}
                className={`itemText flex items-center cursor-pointer`} // Removed conditional background color
                onClick={() => handleRateSelect(rate)}
              >
                <td className="checkbox">
                  <input
                    type="checkbox"
                    name="rateSelection"
                    onChange={(e) => {
                      e.stopPropagation();
                      handleRateSelect(rate);
                    }}
                    checked={selectedRate?.service_name === rate.service_name}
                    className=""
                  />
                </td>
                <td className="itemList">UPS</td>
                <td className="itemList">{rate.service_name || "N/A"}</td>
                <td className="itemList">
                  {rate.estimated_arrival_date || "N/A"} {rate.estimated_arrival_time || ""}
                </td>
                <td className="itemList">${rate.total_charges?.toFixed(2) || "N/A"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ShippingTable;
