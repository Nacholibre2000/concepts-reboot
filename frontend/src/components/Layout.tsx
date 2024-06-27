import React, { ReactNode } from 'react';
import Navbar from './Navbar'; // Adjust the import to your folder structure
import Sidebar from './Sidebar'; // Import the Sidebar component
import { NodeSearchProvider } from '../context/NodeSearchContext'; // Import NodeSearchProvider

type LayoutProps = {
  children: ReactNode;
};

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <NodeSearchProvider>
      <div className="flex h-screen flex-col">
        <Navbar />
        <div className="flex flex-1">
          <Sidebar />
          <main>{children}</main>
        </div>
      </div>
    </NodeSearchProvider>
  );
};

export default Layout;
