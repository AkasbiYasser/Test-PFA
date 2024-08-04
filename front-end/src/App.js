import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Dashboard from './components/Dashboard/Dashboard';
import ConfigGenerator from './components/ConfigGenerator/ConfigGenerator';
import ConfigServer from './components/ConfigServer/ConfigServer';
import Home from './home';
import './App.css';
import logo from './images/grupologo.jpg';

const App = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <Router>
      <div className="app bg-animated min-h-screen text-white">
        <button
          className="menu-button p-2 bg-gray-900 rounded fixed top-4 left-4 z-50 button "
          onClick={() => setIsMenuOpen(!isMenuOpen)}
        >
          Menu
        </button>
        <Link
          to="/contact"
          className="contact-button p-2 bg-gray-900 rounded fixed top-4 right-4 z-50 button "
        >
          Contact Us
        </Link>
        <nav className={`app-nav p-4 bg-gray-900 bg-opacity-75 flex flex-col justify-around fixed top-0 left-0 h-full w-64 transform ${isMenuOpen ? 'translate-x-0' : '-translate-x-full'} transition-transform duration-300 ease-in-out z-40`}>
          <Link to="/" className="hover:bg-gray-700 p-2 rounded" onClick={() => setIsMenuOpen(false)}>Home</Link>
          <Link to="/dashboard" className="hover:bg-gray-700 p-2 rounded" onClick={() => setIsMenuOpen(false)}>Dashboard</Link>
          <Link to="/config-generator" className="hover:bg-gray-700 p-2 rounded" onClick={() => setIsMenuOpen(false)}>Configure Generator</Link>
          <Link to="/config-server" className="hover:bg-gray-700 p-2 rounded" onClick={() => setIsMenuOpen(false)}>Configure The Server</Link>
        </nav>
        <div className={`content transition-opacity duration-300 ${isMenuOpen ? 'opacity-50' : 'opacity-100'}`}>
          <Routes>
            <Route path="/" element={<Home logo={logo} />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/config-generator" element={<ConfigGenerator />} />
            <Route path="/config-server" element={<ConfigServer />} />
            <Route path="/contact" element={<Contact />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
};

const Contact = () => (
  <div className="contact-page flex flex-col items-center justify-center min-h-screen text-center bg-animated">
    <h1 className="text-4xl font-bold mb-8">Contact Us</h1>
    <p className="text-xl mb-4">
      Hi There, We are looking forward to hearing from you. Please feel free to get in touch via contact info below and we will get back to you as soon as possible.
    </p>
    <p className="text-xl mb-4">Grupo Marpica SA</p>
    <p className="text-xl mb-4">78c Street, PH Sunshine By The Park,</p>
    <p className="text-xl mb-4">Panama City, Panama</p>
    <p className="text-xl mb-4">Mail: info@marpica.com</p>
    <p className="text-xl mb-4">Phone: +507-68252600</p>
  </div>
);

export default App;
