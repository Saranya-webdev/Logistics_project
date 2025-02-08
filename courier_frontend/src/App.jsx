"use client"
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import Charts from "./components/Combinedcharts";
import EntityList from "./components/EntityList";
import BookingList from "./components/BookingList";


export default function Page() {
  return (
    <div className="flex flex-col h-screen bg-[#f3f3f3] p-[20px]">
        <Header/>
          <div className="flex gap-8">
              <Sidebar className="w-[4%]"/>
            <div className="flex bg-white p-[20px] rounded-[12px] gap-[20px] w-[80%] md:w-col">
              <EntityList/>
                <div>
                  <Charts/>
                  <BookingList/>
                </div>
            </div>
          </div>
    </div>
  );
}