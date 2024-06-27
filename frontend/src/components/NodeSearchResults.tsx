import React from 'react';
import { useNodeSearch } from '../context/NodeSearchContext';

const NodeSearchResults: React.FC = () => {
  const { searchResults } = useNodeSearch();

  console.log('Rendered NodeSearchResults with:', searchResults);

  if (!searchResults || !searchResults.length) {
    return <p>No results found.</p>;
  }

  return (
    <div className="overflow-x-auto p-4">
      <table className="table w-full">
        {/* head */}
        <thead>
          <tr>
            <th></th>
            <th>Concept</th>
            <th>Explanation</th>
          </tr>
        </thead>
        <tbody>
          {searchResults.map((result: any, index: number) => (
            <tr key={result.uid}>
              <th>{index + 1}</th>
              <td>{result.concept}</td>
              <td>{result.explanation}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default NodeSearchResults;
