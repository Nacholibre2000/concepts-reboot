import React from 'react';
import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="bg-gray-800 p-4 text-white">
      <div className="container mx-auto">
        <div className="flex items-center justify-start space-x-4">
          <a href="/" className="pl-20 pr-40 text-2xl font-bold">
            Kursplanen
          </a>
          <label htmlFor="search" className="input input-bordered flex items-center gap-2 mx-4">
            <input id="search" type="text" className="grow" placeholder="Search" />
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 16 16"
              fill="currentColor"
              className="h-4 w-4 opacity-70">
              <path
                fillRule="evenodd"
                d="M9.965 11.026a5 5 0 1 1 1.06-1.06l2.755 2.754a.75.75 0 1 1-1.06 1.06l-2.755-2.754ZM10.5 7a3.5 3.5 0 1 1-7 0 3.5 3.5 0 0 1 7 0Z"
                clipRule="evenodd" />
            </svg>
          </label>
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
