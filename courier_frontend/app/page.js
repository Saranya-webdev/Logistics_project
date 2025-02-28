// "use client";

// import Image from "next/image";

// export default function Home() {
//   return (
//     <div className="">
      
//     </div>
//   );
// }

"use client"; 

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // router.push("/customers"); 
    router.push("/customers");
  }, []);

  return null; // Return nothing
}

