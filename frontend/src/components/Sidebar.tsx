import React, { useEffect, useState } from 'react';
import FunnelIcon from './FunnelIcon';
import { useExpandedItems } from '../context/ExpandedItemsContext';

type Item = {
  id: number;
  table: string;
  [key: string]: any; // This allows for additional fields
};

export default function Sidebar() {
  const [data, setData] = useState<Item[]>([]);
  const { expandedItems, toggleExpand } = useExpandedItems(); // Use the context
  const [toggledItems, setToggledItems] = useState<Set<string>>(new Set());
  const [expandedTextItems, setExpandedTextItems] = useState<Set<string>>(new Set());

  useEffect(() => {
    // Fetch data from your API endpoint
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

        const mapDataRecursively = (data: any[]): any[] => {
          return data.map((item: any) => {
            const newItem = { ...item, displayName: mapToDisplayName(item) };
            if (item.children) {
              newItem.children = mapDataRecursively(item.children);
            }
            return newItem;
          });
        };

        const mappedData = mapDataRecursively(allData);
        setData(mappedData);
      });
  }, []);

  const toggleBold = (id: number, table: string, items: Item[]) => {
    const compositeKey = `${id}-${table}`;
    const newToggledItems = new Set(toggledItems);
    if (newToggledItems.has(compositeKey)) {
      newToggledItems.delete(compositeKey);
    } else {
      newToggledItems.add(compositeKey);
    }
    setToggledItems(newToggledItems);
  };

  const toggleTextExpand = (id: number, table: string) => {
    const compositeKey = `${id}-${table}`;
    const newTextItems = new Set(expandedTextItems);
    if (newTextItems.has(compositeKey)) {
      newTextItems.delete(compositeKey);
    } else {
      newTextItems.add(compositeKey);
    }
    setExpandedTextItems(newTextItems);
  };

  const renderTree = (items: Item[], level: number = 0) => {
    const indent = 10 * level;

    return (
      <ul style={{ marginLeft: `${indent}px` }}>
        {items.map((item) => (
          <li key={`${item.id}-${item.table}`} className="w-full">
            <div className={`flex w-full items-center justify-between rounded p-2 hover:bg-gray-700`}>
              <button
                className={`text-left text-base text-sm text-gray-400 ${toggledItems.has(`${item.id}-${item.table}`) ? 'font-bold' : 'font-normal'} mb-2 block w-full text-left hover:text-gray-100`}
                onClick={() => toggleExpand(`${item.id}-${item.table}`)} // Use the context's toggleExpand
              >
                {expandedTextItems.has(`${item.id}-${item.table}`)
                  ? item.displayName
                  : item.displayName.length > 20
                    ? item.displayName.substring(0, 20) + '...'
                    : item.displayName}
              </button>
              {item.displayName.length > 20 && (
                <button onClick={() => toggleTextExpand(item.id, item.table)}>
                  ...
                </button>
              )}
              <button onClick={() => toggleBold(item.id, item.table, data)}>
                <FunnelIcon toggled={toggledItems.has(`${item.id}-${item.table}`)} />
              </button>
            </div>
            {expandedItems.has(`${item.id}-${item.table}`) && item.children && renderTree(item.children, level + 1)}
          </li>
        ))}
      </ul>
    );
  };

  return (
    <aside className="w-80 bg-gray-800 p-10 text-white">
      {renderTree(data)}
    </aside>
  );
}