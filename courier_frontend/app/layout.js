// Layout.js

import React from 'react';
import Sidebar from './components/sidebar';
import Header from './components/header';
import './globals.css';

export const metadata = {
  title: 'Courier App',
  description: 'Courier application frontend',
};

const Layout = ({ children }) => (
  <html lang="en">
    <body >
      <div className="relative flex w-[100%] h-screen p-4 bg-[#f3f3f3] overflow-hidden no-scrollbar overflow-y-auto">
      <Sidebar className="bg-red-200"/>
      <div className='w-[100%]'>
        <Header className="h-[20%]"/>
        <main className="flex h-[90%] w-[100%] bg-[#f3f3f3]">{children}</main>
      </div>
      </div>
    </body>
  </html>
);

export default Layout;