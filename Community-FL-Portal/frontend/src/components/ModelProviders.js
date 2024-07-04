import React, { useEffect, useState } from 'react';
import API from '../api';
import '../styles/ModelProviders.css';

function ModelProviders() {
    const [modelProviders, setModelProviders] = useState([]);

    useEffect(() => {
        const fetchModelProviders = async () => {
            try {
                const response = await API.get('/model_providers', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                setModelProviders(response.data);
            } catch (error) {
                console.error('Error fetching model providers:', error);
            }
        };
        fetchModelProviders();
    }, []);

    return (
        <div>
            <h2>Model Providers</h2>
            <table className="table">
                <thead>
                    <tr>
                        <th className="th">Username</th>
                        <th className="th">Type</th>
                        <th className="th">Group</th>
                        <th className="th">Email</th>
                        <th className="th">Model URL</th>
                    </tr>
                </thead>
                <tbody>
                    {modelProviders.map((provider) => (
                        <tr key={provider.id}>
                            <td className="td">{provider.username}</td>
                            <td className="td">{provider.type}</td>
                            <td className="td">{provider.group}</td>
                            <td className="td">{provider.email}</td>
                            <td className="td">{provider.modelURL}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default ModelProviders;