import React from 'react';
import { createRoot } from 'react-dom/client';
import AppRoutes from '../components/AppRoutes'; // Adjust the path if necessary
import '../styles/index.css'; // Global CSS file

// This is the entry point of the application.
// It initializes the root component App defined in
// /components/app.tsx and then renders it into
// the DOM.The DOM is the resulting tree structure of
// the HTML after the browser has parsed it.

const container = document.getElementById('root') as HTMLElement;
const root = createRoot(container!);
root.render(
  <React.StrictMode>
    <AppRoutes />
  </React.StrictMode>,
);
