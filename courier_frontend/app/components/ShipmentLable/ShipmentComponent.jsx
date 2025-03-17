"use client";
import { useRouter } from "next/navigation";
import Image from "next/image";

const ShipmentComponent = ({ labelPath, trackingNumber }) => {
  const router = useRouter();

  const handleClose = () => {
    router.push("/bookings"); // Redirect to /bookings page
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-between px-4 py-4 rounded-xl overflow-y-auto">
      {/* Tracking Number Display */}
      <h1 className="text-lg font-semibold mb-4">
        Your Tracking Number: <span className="text-[#4972b4] font-Mono">{trackingNumber}</span>
      </h1>

      {/* Image Container */}
      <div className="flex flex-grow items-center justify-center">
        <div className="relative w-[500px] h-[500px] transform rotate-90">
          {/* Rotated Image */}
          <Image
            src={labelPath}
            alt="Shipping Label"
            fill
            style={{ objectFit: "contain" }}
            unoptimized
            onError={() => console.error("Image failed to load:", labelPath)}
          />
        </div>
      </div>

      {/* Close Button */}
      <div className="w-full flex justify-end mt-4">
        <button
          type="button"
          className="submit px-4 py-2 bg-red-500 text-white rounded-md"
          onClick={handleClose}
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default ShipmentComponent;
