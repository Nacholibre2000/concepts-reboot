import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from '../views/index';
import AddNode from '../components/AddNode';
import Layout from '../components/Layout';

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
      </Routes>
    </Router>
  );
};

export default AppRoutes;
