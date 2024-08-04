import React from 'react';
import './Home.css';

const Home = ({ logo }) => {
  return (
    <div className="home flex flex-col items-center justify-center min-h-screen text-center relative overflow-hidden bg-animated">
      <div className="header-container flex justify-between items-center w-full px-8 py-4 absolute top-0">
        <div className="company-logo flex items-center justify-center w-full">
          <img src={logo} alt="Grupo Marpica Logo" className="company-logo-img w-12 h-12 mr-2" />
          <span className="company-name text-white text-2xl">Grupo Marpica</span>
        </div>
      </div>
      <div className="content-container flex flex-col items-center">
        <h1 className="text-6xl font-bold mb-8 animated-title">TEXT MESSAGING GENERATION SOFTWARE</h1>
        <p className="description text-xl text-white mb-8">
          Experience unmatched efficiency in text messaging generation with our software, powered by the industry-leading SMPP protocol for reliable and seamless communication.
        </p>
      </div>
    </div>
  );
};

export default Home;