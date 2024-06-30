import React, { useEffect, useState } from 'react';
import { useExpandedItems } from '../context/ExpandedItemsContext';
import { useSelectedItems } from '../context/SelectedItemsContext'; 

type Item = {
  id: number;
  table: string;
  displayName: string;
  children?: Item[];
  [key: string]: any;
};

export default function Sidebar() {
  const [data, setData] = useState<Item[]>([]);
  const { expandedItems, toggleExpand } = useExpandedItems(); 
  const { selectedItems, toggleSelection } = useSelectedItems(); 

  useEffect(() => {
    fetch('http://localhost:5000/api/curriculum_data')
      .then((res) => res.json())
      .then((allData) => {
        const mapToDisplayName = (item: any) => {
          return (
            item.school ||
            item.subject ||
            item.grade ||
            item.subsection ||
            item.central_requirement ||
            item.central_content ||
            'Unnamed Item'
          );
        };

        const mapDataRecursively = (data: any[]): Item[] => {
          return data.map((item: any) => ({
            ...item,
            displayName: mapToDisplayName(item),
            children: item.children ? mapDataRecursively(item.children) : undefined
          }));
        };

        const mappedData = mapDataRecursively(allData);
        setData(mappedData);
      });
  }, []);

  const getAllChildren = (item: Item): string[] => {
    let children: string[] = [];
    if (item.children) {
      item.children.forEach(child => {
        children.push(`${child.id}-${child.table}`);
        children = children.concat(getAllChildren(child));
      });
    }
    return children;
  };

  const renderTree = (items: Item[], level: number = 0) => {
    const indent = 10 * level;

    return (
      <ul style={{ marginLeft: `${indent}px` }}>
        {items.map((item) => {
          const compositeKey = `${item.id}-${item.table}`;
          const allChildren = getAllChildren(item);
          const isSelected = selectedItems.has(compositeKey);
          const areAllChildrenSelected = allChildren.every(child => selectedItems.has(child));

          return (
            <li key={compositeKey} className="w-full">
              <div className="flex w-full items-center justify-between rounded p-2 hover:bg-gray-700">
                <button
                  className={`text-left text-base text-sm text-gray-400 ${
                    isSelected ? 'font-bold' : 'font-normal'
                  } mb-2 block w-full text-left hover:text-gray-100`}
                  onClick={() => toggleExpand(compositeKey)}
                >
                  {item.displayName}
                </button>
                <button
                  onClick={() => toggleSelection(compositeKey, allChildren, item.table)}
                  className={`icon-button ${isSelected ? 'selected' : ''}`}
                >
                  {isSelected && areAllChildrenSelected ? '✓' : isSelected ? '◐' : '○'}
              </button>
              </div>
              {expandedItems.has(compositeKey) && item.children && renderTree(item.children, level + 1)}
            </li>
          );
        })}
      </ul>
    );
  };

  return (
    <aside className="w-80 bg-gray-800 p-10 text-white">
      {renderTree(data)}
    </aside>
  );
}