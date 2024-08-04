import React, { useState } from 'react';
import './ConfigServer.css';

const ConfigServer = () => {
  const [ip, setIp] = useState('');
  const [port, setPort] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  return (
    <div className="config-server-container flex items-center justify-center min-h-screen">
      <div className="config-server bg-gray-800 p-6 rounded shadow-lg max-w-4xl w-full mx-4">
        <h2 className="text-2xl font-bold mb-4 text-center text-white">Server Node</h2>
        <form className="space-y-4">
          <div className="flex flex-col space-y-4">
            <label className="block text-white">
              IP
              <input type="text" className="form-input mt-1 block w-full bg-gray-700 text-white" value={ip} onChange={(e) => setIp(e.target.value)} />
            </label>
            <label className="block text-white">
              Port
              <input type="text" className="form-input mt-1 block w-full bg-gray-700 text-white" value={port} onChange={(e) => setPort(e.target.value)} />
            </label>
            <label className="block text-white">
              Username
              <input type="text" className="form-input mt-1 block w-full bg-gray-700 text-white" value={username} onChange={(e) => setUsername(e.target.value)} />
            </label>
            <label className="block text-white">
              Password
              <input type="password" className="form-input mt-1 block w-full bg-gray-700 text-white" value={password} onChange={(e) => setPassword(e.target.value)} />
            </label>
          </div>
          <button className="btn" type="button">
            <strong>Save</strong>
            <div id="container-stars">
              <div id="stars"></div>
            </div>
            <div id="glow">
              <div className="circle"></div>
              <div className="circle"></div>
            </div>
          </button>
        </form>
      </div>
    </div>
  );
};

export default ConfigServer;
