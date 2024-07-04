import React, { useEffect, useState } from 'react';
import API from '../api';
import '../styles/InfraWithDataProviders.css';

function InfraWithDataProviders() {
    const [infraWithDataProviders, setInfraWithDataProviders] = useState([]);

    useEffect(() => {
        const fetchInfraWithDataProviders = async () => {
            try {
                const response = await API.get('/infra_with_data_providers', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                setInfraWithDataProviders(response.data);
            } catch (error) {
                console.error('Error fetching infra with data providers:', error);
            }
        };
        fetchInfraWithDataProviders();
    }, []);

    return (
        <div>
            <h2>Infrastructure with Data Providers</h2>
            <table className="table">
                <thead>
                    <tr>
                        <th className="th">Username</th>
                        <th className="th">Type</th>
                        <th className="th">Group</th>
                        <th className="th">Email</th>
                    </tr>
                </thead>
                <tbody>
                    {infraWithDataProviders.map((providers) => (
                        <tr key={providers.id}>
                            <td className="td">{providers.username}</td>
                            <td className="td">{providers.type}</td>
                            <td className="td">{providers.group}</td>
                            <td className="td">{providers.email}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default InfraWithDataProviders;
