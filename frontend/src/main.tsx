import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './components/App'; // Importing App instead of AppRoutes
import './styles/global.css'; // Global CSS file
import './styles/tailwind.css'; // Tailwind CSS file

// This is the entry point of the application.
// It initializes the root component App defined in App.tsx and renders it into the DOM.

const container = document.getElementById('root') as HTMLElement;
const root = createRoot(container!);
root.render(
  <React.StrictMode>
    <App /> {/* Render App instead of AppRoutes */}
  </React.StrictMode>,
);
