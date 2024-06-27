import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { useNodeSearch } from '../context/NodeSearchContext';

export default function Navbar() {
  const [searchTerm, setSearchTerm] = useState('');
  const { setSearchResults } = useNodeSearch();

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.get(
        'http://localhost:5000/api/node_data/query',
        {
          params: { node: searchTerm },
        },
      );
      setSearchResults(response.data.results);
    } catch (err: any) {
      console.error(
        'Error searching:',
        err.response ? err.response.data.message : err.message,
      );
    }
  };

  return (
    <nav className="bg-gray-800 p-4 text-white">
      <div className="container mx-auto">
        <div className="flex items-center justify-start space-x-4">
          <a href="/" className="pl-20 pr-40 text-2xl font-bold">
            Kursplanen
          </a>
          <form
            onSubmit={handleSearch}
            className="mx-4 flex items-center gap-2"
          >
            <label
              htmlFor="search"
              className="input input-bordered flex w-full items-center gap-2"
            >
              <input
                id="search"
                type="text"
                className="grow"
                placeholder="Search"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <button type="submit" className="btn btn-primary">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  viewBox="0 0 16 16"
                  fill="currentColor"
                  className="size-4 opacity-70"
                >
                  <path
                    fillRule="evenodd"
                    d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </label>
          </form>
          <Link
            to="/add-node"
            className="text-base font-bold text-gray-300 hover:text-gray-100"
          >
            Lägg till nyckelord
          </Link>
        </div>
      </div>
    </nav>
  );
}
