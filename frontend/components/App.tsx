import React from 'react';
import AppRoutes from './AppRoutes'; // Importing AppRoutes

function App() {
  return (
    <div>
      <div className="gradient-bar flex items-center justify-center pr-80">
        <span className="mr-40 text-5xl font-semibold tracking-wider text-emerald-600">
          Kursplanen online
        </span>
      </div>
      <AppRoutes /> {/* Include AppRoutes */}
    </div>
  );
}

export default App;
