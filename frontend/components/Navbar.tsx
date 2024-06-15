// components/Navbar.tsx

import React from 'react';

export default function Navbar() {
    return (
        <nav className="bg-gray-800 text-white p-4">
            <div className="container mx-auto">
                <div className="flex justify-start items-center">
                    <a href="/" className="text-2xl font-bold pl-20 pr-40">Kursplaner</a>
                    <div>
                        <button className="mx-12 text-base text-gray-300 font-semibold hover:text-gray-100 font-bold">Begrepp</button>
                        <button className="mx-12 text-base text-gray-300 font-semibold hover:text-gray-100 font-bold">Provfrågor</button>
                        <button className="mx-12 text-base text-gray-300 font-semibold hover:text-gray-100 font-bold">Tidslinje</button>
                        <button className="mx-12 text-base text-gray-300 font-semibold hover:text-gray-100 font-bold">Logga in</button>
                    </div>
                </div>
            </div>
        </nav>
    );
}
