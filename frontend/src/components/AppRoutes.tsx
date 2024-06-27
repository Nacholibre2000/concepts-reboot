import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from '../index';
import AddNode from './AddNode';
import Layout from './Layout';
import NodeSearchResults from './NodeSearchResults';

//

const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route
          path="/add-node"
          element={
            <Layout>
              <AddNode />
            </Layout>
          }
        />
        <Route
          path="/flashcards-results"
          element={
            <Layout>
              <NodeSearchResults />
            </Layout>
          }
        />
      </Routes>
    </Router>
  );
};

export default AppRoutes;
