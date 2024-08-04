import React, { useState } from 'react';
import axios from 'axios';
import './ConfigGenerator.css';

const ConfigGenerator = () => {
  const [configFile, setConfigFile] = useState(null);
  const [ip, setIp] = useState('');
  const [port, setPort] = useState('');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [smsPerSec, setSmsPerSec] = useState('');
  const [total, setTotal] = useState('');
  const [repeat, setRepeat] = useState(false);

  const handleConfigFileChange = (e) => {
    setConfigFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();

    if (configFile) {
      formData.append('configFile', configFile);
      try {
        const response = await axios.post('http://localhost:5000/api/upload', formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });

        console.log('Response:', response.data);
      } catch (error) {
        console.error('There was an error!', error);
      }
    } else {
      try {
        const response = await axios.post('http://localhost:5000/api/sms', {
          ip,
          port,
          user: username,
          password,
          files: [], // Assuming no files uploaded
          repeat,
          amount: total,
          amount_per_sec: smsPerSec,
        });

        console.log('Response:', response.data);
      } catch (error) {
        console.error('There was an error!', error);
      }
    }
  };

  return (
    <div className="config-generator-container flex items-center justify-center min-h-screen">
      <div className="config-generator bg-gray-800 p-6 rounded shadow-lg w-full mx-4">
        <h2 className="text-2xl font-bold mb-4 text-center text-white">Configuration Panel</h2>
        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className="flex flex-col space-y-4">
            <button className="container-btn-file" type="button">
              <svg fill="#fff" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 50 50">
                <path d="M28.8125 .03125L.8125 5.34375C.339844 
                5.433594 0 5.863281 0 6.34375L0 43.65625C0 
                44.136719 .339844 44.566406 .8125 44.65625L28.8125 
                49.96875C28.875 49.980469 28.9375 50 29 50C29.230469 
                50 29.445313 49.929688 29.625 49.78125C29.855469 49.589844 
                30 49.296875 30 49L30 1C30 .703125 29.855469 .410156 29.625 
                .21875C29.394531 .0273438 29.105469 -.0234375 28.8125 .03125ZM32 
                6L32 13L34 13L34 15L32 15L32 20L34 20L34 22L32 22L32 27L34 27L34 
                29L32 29L32 35L34 35L34 37L32 37L32 44L47 44C48.101563 44 49 
                43.101563 49 42L49 8C49 6.898438 48.101563 6 47 6ZM36 13L44 
                13L44 15L36 15ZM6.6875 15.6875L11.8125 15.6875L14.5 21.28125C14.710938 
                21.722656 14.898438 22.265625 15.0625 22.875L15.09375 22.875C15.199219 
                22.511719 15.402344 21.941406 15.6875 21.21875L18.65625 15.6875L23.34375 
                15.6875L17.75 24.9375L23.5 34.375L18.53125 34.375L15.28125 
                28.28125C15.160156 28.054688 15.035156 27.636719 14.90625 
                27.03125L14.875 27.03125C14.8125 27.316406 14.664063 27.761719 
                14.4375 28.34375L11.1875 34.375L6.1875 34.375L12.15625 25.03125ZM36 
                20L44 20L44 22L36 22ZM36 27L44 27L44 29L36 29ZM36 35L44 35L44 37L36 37Z"></path>
              </svg>
              Upload configuration file
              <input className="file" name="file" type="file" onChange={handleConfigFileChange} />
            </button>
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
            <label className="block text-white">
              SMS/sec
              <input type="text" className="form-input mt-1 block w-full bg-gray-700 text-white" value={smsPerSec} onChange={(e) => setSmsPerSec(e.target.value)} />
            </label>
            <label className="block text-white">
              Total
              <input type="text" className="form-input mt-1 block w-full bg-gray-700 text-white" value={total} onChange={(e) => setTotal(e.target.value)} />
            </label>
            <label className="block text-white flex items-center">
              Repeat
              <input type="checkbox" className="form-checkbox mt-1 ml-2" checked={repeat} onChange={(e) => setRepeat(e.target.checked)} />
            </label>
          </div>

          <button className="btn" type="submit">
            <strong>SEND</strong>
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

export default ConfigGenerator;
