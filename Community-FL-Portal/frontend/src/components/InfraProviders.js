import React, { useEffect, useState } from 'react';
import API from '../api';
import '../styles/InfraProviders.css';

function InfraProviders() {
    const [infraProviders, setInfraProviders] = useState([]);

    useEffect(() => {
        const fetchInfraProviders = async () => {
            try {
                const response = await API.get('/infra_providers', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                setInfraProviders(response.data);
            } catch (error) {
                console.error('Error fetching infra providers:', error);
            }
        };
        fetchInfraProviders();
    }, []);

    return (
        <div>
            <h2>Infrastructure Providers</h2>
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
                    {infraProviders.map((providers) => (
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

export default InfraProviders;
