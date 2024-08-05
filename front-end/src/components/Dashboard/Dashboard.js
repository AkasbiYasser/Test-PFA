import React, { useEffect, useState } from 'react';
import './Dashboard.css';
import axios from 'axios';

const API_URL = 'http://20.164.56.175.nip.io'; 

const Dashboard = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`${API_URL}/api/data`)
      .then(response => {
        console.log(response.data);
        setData(response.data);
      })
      .catch(error => {
        console.error('Erreur lors de la récupération des données!', error);
      });
  }, []);

  const calculatePercentage = (smsSent, totalSms) => {
    if (totalSms === 0) return "100.00";
    return smsSent > 0 ? ((totalSms - smsSent) / totalSms * 100).toFixed(2) : "100.00";
  };

  return (
    <div className="dashboard-container flex justify-center">
      <div className="dashboard bg-gray-800 p-6 rounded shadow-lg w-full mx-4 mt-20">
        <h2 className="text-2xl font-bold mb-4 text-center text-white">SMS Generator</h2>
        <table className="dashboard-table w-full text-left mt-4">
          <thead className="bg-gray-700">
            <tr>
              <th className="p-2">ID</th>
              <th className="p-2">Generator</th>
              <th className="p-2">IP/Port</th>
              <th className="p-2">Template</th>
              <th className="p-2">SMS/Sec</th>
              <th className="p-2">Percent</th>
              <th className="p-2">Start</th>
              <th className="p-2">Edit</th>
            </tr>
          </thead>
          <tbody className="bg-gray-600">
            {data.map((row, index) => (
              <tr key={index}>
                <td className="p-2">{row[0]}</td>
                <td className="p-2">{index + 1000}</td> {/* Identifiant unique pour le générateur */}
                <td className="p-2">{row[1]}</td>
                <td className="p-2">{row[2]}</td> {/* Nom du fichier CSV */}
                <td className="p-2">{row[4]}</td>
                <td className="p-2">
                  <span className={`percentage ${calculatePercentage(row[3], row[4]) === "100.00" ? "complete" : ""}`}>
                    {calculatePercentage(row[3], row[4])}%
                  </span>
                </td> {/* Pourcentage de SMS envoyés */}
                <td className="p-2">
                  <button className="bg-blue-500 text-white py-1 px-2 rounded">Démarrer</button>
                </td>
                <td className="p-2">
                  <button className="bg-green-500 text-white py-1 px-2 rounded">Modifier</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
