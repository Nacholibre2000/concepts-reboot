import React from 'react';
import Layout from './components/Layout';
import NodeSearchResults from './components/NodeSearchResults'; // Import NodeSearchResults

const Home: React.FC = () => {
  return (
    <Layout>
      <NodeSearchResults />
    </Layout>
  );
};

export default Home;
