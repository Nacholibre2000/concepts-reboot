import React, {createContext, useContext, useState, ReactNode, useCallback, useEffect } from 'react';

type SelectedItemsContextType = {
  selectedItems: Set<string>;
  toggleSelection: (compositeKey: string, allChildren: string[], table: string) => void;
  selectedContentAndRequirements: string[];
};

const SelectedItemsContext = createContext<SelectedItemsContextType | undefined>(undefined);

export const SelectedItemsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [selectedItems, setSelectedItems] = useState<Set<string>>(new Set());
  const [selectedContentAndRequirements, setSelectedContentAndRequirements] = useState<string[]>([]);

  const toggleSelection = useCallback((compositeKey: string, allChildren: string[], table: string) => {
    setSelectedItems((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(compositeKey)) {
        newSet.delete(compositeKey);
        allChildren.forEach(child => newSet.delete(child));
      } else {
        newSet.add(compositeKey);
        allChildren.forEach(child => newSet.add(child));
      }
      return newSet;
    });
  }, []);

  useEffect(() => {
    const newSelectedContentAndRequirements = Array.from(selectedItems).filter(item => {
      const [, table] = item.split('-');
      return table === 'central_contents' || table === 'central_requirements';
    });

    setSelectedContentAndRequirements(newSelectedContentAndRequirements);
    console.log('Selected central_contents and central_requirements:', newSelectedContentAndRequirements);
  }, [selectedItems]);

  return (
    <SelectedItemsContext.Provider value={{ selectedItems, toggleSelection, selectedContentAndRequirements }}>
      {children}
    </SelectedItemsContext.Provider>
  );
};

export const useSelectedItems = (): SelectedItemsContextType => {
  const context = useContext(SelectedItemsContext);
  if (!context) {
    throw new Error('useSelectedItems must be used within a SelectedItemsProvider');
  }
  return context;
};