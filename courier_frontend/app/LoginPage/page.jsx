    "use client";
    
    import { useState } from "react";
    import Image from "next/image";
    import {  FaEnvelope, FaLock, FaUserCircle } from "react-icons/fa";
    
    export default function SignupPage() {
      const [isSignup, setIsSignup] = useState(true);
      const [countryCode, setCountryCode] = useState("+91");
      const [formData, setFormData] = useState({
        username: "",
        email: "",
        otp: "",
        mobile: "",
        password: "",
      });
      const [errors, setErrors] = useState({});
    
    
      const countryCodes = [
        { code: "+1", name: "USA" },
        { code: "+44", name: "UK" },
        { code: "+91", name: "India" },
        // Add more country codes as needed
      ];

      const validate = () => {
        let newErrors = {};
        if (isSignup && !formData.username.trim()) newErrors.username = "Username is required";
        if (!formData.email.trim()) {
          newErrors.email = "Email is required";
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
          newErrors.email = "Invalid email format";
        }
        if (isSignup && !formData.otp.trim()) newErrors.otp = "OTP is required";
        if (isSignup && !formData.mobile.trim()) newErrors.mobile = "Mobile number is required";
        if (!isSignup && !formData.password.trim()) newErrors.password = "Password is required";
        
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
      };
    
      const handleSubmit = () => {
        if (validate()) {
          console.log("Form Submitted", formData);
        }
      };
    
      return (
        <div className="w-[100%] h-screen bg-[#ffffff] rounded-[10px] flex justify-center items-start">
            <div className="relative h-screen w-[35%] bg-blue-100">
            <Image src="/sidelogo.jpeg" alt="logo" layout="fill" objectFit="cover" className="absolute left-0"/>
            </div>

          {/* Right Side: Signup/Login Form */}
          <div className="flex flex-col justify-between items-center w-[65%] h-full px-[230px] overflow-y-auto overflow-hidden no-scrollbar">
              <Image src="/signuplogo.jpeg" alt="logo" width={80} height={80}/>
            {/* Tabs: Signup / Login */}
            <div className="flex justify-around gap-10 m-auto mb-6">
              <button
                className={`text-[28px] font-semibold ${isSignup ? "text-[#074E73] border-b-4 w-[150px] border-[#074E73]" : "text-gray-500"}`}
                onClick={() => setIsSignup(true)}
              >
                Signup
              </button>
              <button
                className={`text-[28px] font-Roboto font-semibold ${!isSignup ? "text-[#074E73] border-b-4 w-[150px] border-[#074E73]" : "text-gray-500"}`}
                onClick={() => setIsSignup(false)}
              >
                Login
              </button>
            </div>
            
            <div className="w-[100%] h-[100%] px-8 pt-11 bg-[#f1f4f7] rounded-[10px] m-auto">
              {/* Form Fields */}
              <div className="">
                {isSignup ? (
                  <>
                  <div className="flex flex-col h-full mb-6">
                    <label htmlFor="" className="block text-gray-700 font-Roboto font-medium mb-2">Username</label>
                    <div className="flex items-center bg-white px-4 py-3 gap-3 rounded-lg border">
                    <FaUserCircle style={{ fontSize: "20px" }} className="text-gray-900" />

                        <input type="text" placeholder="Username" className="w-full focus:outline-none bg-transparent text-gray-900" value={formData.username} onChange={(e) => setFormData({...formData, username: e.target.value})}/>
                        {errors.username && <p className="error">{errors.username}</p>}
                      </div>
                  </div>

                  <div className="flex justify-between items-end mb-6 gap-3">
                    <div className="w-full ">
                    <label htmlFor="" className="block text-gray-700 font-Roboto font-medium mb-2">Email</label>
                    <div className="flex items-center bg-white px-4 gap-3 rounded-lg border">
                        <FaEnvelope style={{"font-size":"20px",}} className="text-gray-900" />
                        <input type="text" placeholder="Email" className="w-full h-11 focus:outline-none bg-transparent text-gray-900" value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})} />
                        {errors.email && <p className="error">{errors.email}</p>}
                      </div>
                    </div>
                    <button className="text-white text-base font-medium font-Roboto px-10 py-2.5 bg-[#074e73] rounded-lg ">
                        GetOTP
                    </button>
                    </div>
                  
                    <div className="flex flex-col h-full mb-6">
                    <label htmlFor="" className="block text-gray-700 font-Roboto font-medium mb-2">OTP</label>
                    <div className="flex items-center bg-white px-4 py-3 gap-3 rounded-lg border">
                        <FaLock style={{"font-size":"20px",}} className="text-gray-900" />
                        <input type="text" placeholder="OTP" className="w-full focus:outline-none bg-transparent text-gray-900" value={formData.otp} onChange={(e) => setFormData({...formData, otp: e.target.value})}/>
                        {errors.otp && <p className="error">{errors.otp}</p>}
                      </div>
                  </div>


                  <div className="flex justify-between items-end mb-6 gap-3">
                    <div className="w-full ">
                    <label htmlFor="" className="block text-gray-700 font-Roboto font-medium mb-2">Mobile Number</label>
                    <div className="flex items-center bg-white px-4 gap-3 rounded-lg border">

                    <select
                          className="bg-transparent focus:outline-none"
                          value={countryCode}
                          onChange={(e) => setCountryCode(e.target.value)}
                        >
                          {countryCodes.map((country) => (
                            <option key={country.code} value={country.code}>
                              {country.code}
                            </option>
                          ))}
                        </select>

                        <span className="opacity-5 px-1">|</span>
                        <input type="text" placeholder="Enter Mobile Number" className="w-full h-11 focus:outline-none bg-transparent text-gray-900" value={formData.mobile} onChange={(e) => setFormData({...formData, mobile: e.target.value})}/>
                        {errors.mobile && <p className="error">{errors.mobile}</p>}
                      </div>
                    </div>
                    <button className="text-white text-base font-medium font-Roboto px-10 py-2.5 bg-[#074e73] rounded-lg onClick={handleSubmit}">
                        GetOTP
                    </button>
                    </div>

                    <div className="flex flex-col h-full">
                    <label htmlFor="" className="block text-gray-700 font-Roboto font-medium mb-2">OTP</label>
                    <div className="flex items-center bg-white px-4 py-3 gap-3 rounded-lg border">
                        <FaLock style={{"font-size":"20px",}} className="text-gray-900" />
                        <input type="text" placeholder="OTP" className="w-full focus:outline-none bg-transparent text-gray-900" value={formData.otp} onChange={(e) => setFormData({...formData, otp: e.target.value})} />
                      </div>
                  </div>

                    <button className="w-full my-5  bg-[#074E73] text-white py-2 rounded-lg" onClick={handleSubmit}>Signup</button>
                  </>
                ) : (
                  <>

                  <div>
                    <div className="w-full ">
                    <label htmlFor="" className="block text-gray-700 font-Roboto font-medium mb-2">Email</label>
                    <div className="flex items-center bg-white px-4 gap-3 rounded-lg border">
                        <FaEnvelope style={{"font-size":"20px",}} className="text-gray-900" />
                        <input type="text" placeholder="Email" className="w-full h-11 focus:outline-none bg-transparent text-gray-900" value={formData.email} onChange={(e) => setFormData({...formData, email: e.target.value})}/>
                        {errors.email && <p className="error">{errors.email}</p>}
                      </div>
                    </div>

                    <div className="flex flex-col h-full mt-6">
                    <label htmlFor="" className="block text-gray-700 font-Roboto font-medium mb-2">Password</label>
                    <div className="flex items-center bg-white px-4 py-3 gap-3 rounded-lg border">
                        <FaLock style={{"font-size":"20px",}} className="text-gray-900" />
                        <input type="text" placeholder="OTP" className="w-full focus:outline-none bg-transparent text-gray-900" value={formData.password} onChange={(e) => setFormData({...formData, password: e.target.value})}/>
                        {errors.password && <p className="error">{errors.password}</p>}
                      </div>
                  </div>
                    </div>

                    <button className="w-full my-5 mt-40 bg-[#074E73] text-white py-2 rounded-lg" onClick={handleSubmit}>Log in</button>
                  </>
                )}
              </div>
            </div>
            <div className="text-gray-500 text-center text-sm tracking-wider">
      <span className="flex gap-1 justify-center items-center mt-2">
        <span className="px-1">Terms</span>
        <span className="px-1">•</span>
        <span className="px-1">Privacy</span>
        <span className="px-1">•</span>
        <span className="px-1">Docs</span>
        <span className="px-1">•</span>
        <span className="px-1">Helps</span>
      </span>
    </div>
    
    
          </div>
        </div>
      );
    }