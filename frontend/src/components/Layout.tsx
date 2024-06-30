import React, { ReactNode } from 'react';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import { NodeSearchProvider } from '../context/NodeSearchContext';
import { ExpandedItemsProvider } from '../context/ExpandedItemsContext'; // Import ExpandedItemsProvider

type LayoutProps = {
  children: ReactNode;
};

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <ExpandedItemsProvider>
      <NodeSearchProvider>
        <div className="flex h-screen flex-col">
          <Navbar />
          <div className="flex flex-1">
            <Sidebar />
            <main className="flex-1 overflow-auto">{children}</main>
          </div>
        </div>
      </NodeSearchProvider>
    </ExpandedItemsProvider>
  );
};

export default Layout;
