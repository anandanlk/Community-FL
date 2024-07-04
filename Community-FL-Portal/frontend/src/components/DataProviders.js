import React, { useEffect, useState } from 'react';
import API from '../api';
import '../styles/DataProviders.css';

function DataProviders() {
    const [dataProviders, setDataProviders] = useState([]);

    useEffect(() => {
        const fetchDataProviders = async () => {
            try {
                const response = await API.get('/data_providers', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                setDataProviders(response.data);
            } catch (error) {
                console.error('Error fetching data providers:', error);
            }
        };
        fetchDataProviders();
    }, []);

    return (
        <div>
            <h2>Data Providers</h2>
            <table className="table">
                <thead>
                    <tr>
                        <th className="th">Username</th>
                        <th className="th">Type</th>
                        <th className="th">Group</th>
                        <th className="th">Email</th>
                        <th className="th">Data URL</th>
                    </tr>
                </thead>
                <tbody>
                    {dataProviders.map((provider) => (
                        <tr key={provider.id}>
                            <td className="td">{provider.username}</td>
                            <td className="td">{provider.type}</td>
                            <td className="td">{provider.group}</td>
                            <td className="td">{provider.email}</td>
                            <td className="td">{provider.dataURL}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default DataProviders;