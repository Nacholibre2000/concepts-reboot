import React, { createContext, useContext, useState, ReactNode } from 'react';

type ExpandedItemsContextType = {
  expandedItems: Set<string>;
  toggleExpand: (id: string) => void;
};

const ExpandedItemsContext = createContext<
  ExpandedItemsContextType | undefined
>(undefined);

export const ExpandedItemsProvider: React.FC<{ children: ReactNode }> = ({
  children,
}) => {
  const [expandedItems, setExpandedItems] = useState<Set<string>>(new Set());

  const toggleExpand = (id: string) => {
    setExpandedItems((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(id)) {
        newSet.delete(id);
      } else {
        newSet.add(id);
      }
      return newSet;
    });
  };

  return (
    <ExpandedItemsContext.Provider value={{ expandedItems, toggleExpand }}>
      {children}
    </ExpandedItemsContext.Provider>
  );
};

export const useExpandedItems = (): ExpandedItemsContextType => {
  const context = useContext(ExpandedItemsContext);
  if (!context) {
    throw new Error(
      'useExpandedItems must be used within a ExpandedItemsProvider',
    );
  }
  return context;
};
