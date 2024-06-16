import React, { ReactNode } from 'react';
import Navbar from './Navbar'; // Adjust the import to your folder structure
import Sidebar from './Sidebar'; // Import the Sidebar component

type LayoutProps = {
  children: ReactNode;
};

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="flex h-screen flex-col">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main>{children}</main>
      </div>
    </div>
  );
};

export default Layout;
