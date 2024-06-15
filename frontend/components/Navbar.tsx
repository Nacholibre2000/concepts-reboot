import React from 'react';

export default function Navbar() {
  return (
    <nav className="bg-gray-800 p-4 text-white">
      <div className="container mx-auto">
        <div className="flex items-center justify-start">
          <a href="/" className="pl-20 pr-40 text-2xl font-bold">
            Kursplaner
          </a>
          <div>
            <button className="mx-12 text-base font-bold font-semibold text-gray-300 hover:text-gray-100">
              Begrepp
            </button>
            <button className="mx-12 text-base font-bold font-semibold text-gray-300 hover:text-gray-100">
              Provfrågor
            </button>
            <button className="mx-12 text-base font-bold font-semibold text-gray-300 hover:text-gray-100">
              Tidslinje
            </button>
            <button className="mx-12 text-base font-bold font-semibold text-gray-300 hover:text-gray-100">
              Logga in
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}
