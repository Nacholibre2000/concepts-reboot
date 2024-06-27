import React, { createContext, useContext, useState, ReactNode } from 'react';

interface NodeSearchContextType {
  searchResults: any;
  setSearchResults: React.Dispatch<React.SetStateAction<any>>;
}

const NodeSearchContext = createContext<NodeSearchContextType | undefined>(
  undefined,
);

export const NodeSearchProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [searchResults, setSearchResults] = useState<any>(null);

  return (
    <NodeSearchContext.Provider value={{ searchResults, setSearchResults }}>
      {children}
    </NodeSearchContext.Provider>
  );
};

export const useNodeSearch = (): NodeSearchContextType => {
  const context = useContext(NodeSearchContext);
  if (!context) {
    throw new Error('useNodeSearch must be used within a NodeSearchProvider');
  }
  return context;
};
