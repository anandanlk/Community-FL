import React, { useEffect, useState } from 'react';
import API from '../api';
import '../styles/ReservedClients.css';

function ReservedClients() {
    const [clientList, setClientList] = useState([]);
    const [selectedClients, setSelectedClients] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    useEffect(() => {
        const fetchReservedClients = async () => {
            try {
                const response = await API.get('/reserved_clients', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                setClientList(response.data);
            } catch (error) {
                console.error('Error fetching reserved clients:', error);
                setErrorMessage('Error fetching reserved clients. Please try again.');
            }
        };
        fetchReservedClients();
    }, []);

    const handleCheckboxChange = (client, isChecked) => {
        if (isChecked) {
            setSelectedClients(prev => [...prev, client]);
        } else {
            setSelectedClients(prev => prev.filter(c => c.username !== client.username));
        }
    };

    const handleUnreserveClients = async () => {
        try {
            await API.post('/unreserve_clients', selectedClients, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
            });
            setSuccessMessage('Clients unreserved successfully.');
            setErrorMessage('');
            const response = await API.get('/reserved_clients', {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
            });
            setClientList(response.data);
            setSelectedClients([]);
        } catch (error) {
            setErrorMessage('An error occurred while unreserving clients. Please try again.');
            setSuccessMessage('');
            console.error('Error unreserving clients:', error);
        }
    };

    const handleDownloadClients = () => {
        const selectedData = selectedClients.map(client => ({
            client_ip: client.client_ip,
            weights: client.weights,
            last_seen: client.last_seen
        }));
        const data = JSON.stringify(selectedData, null, 2);
        const blob = new Blob([data], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'reserved_clients.json';
        a.click();
        URL.revokeObjectURL(url);
    };

    return (
        <div>
            <h2>Reserved Clients</h2>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            {successMessage && <p className="success-message">{successMessage}</p>}
            <table className="table">
                <thead>
                    <tr>
                        <th className="th">S.No</th>
                        <th className="th">Username</th>
                        <th className="th">Email</th>
                        <th className="th">Group</th>
                        <th className="th">Client IP</th>
                        <th className="th">Tags</th>
                        <th className="th">Status</th>
                        <th className="th">Select</th>
                    </tr>
                </thead>
                <tbody>
                    {clientList.map((client, index) => (
                        <tr key={index}>
                            <td className="td">{index + 1}</td>
                            <td className="td">{client.username}</td>
                            <td className="td">{client.email}</td>
                            <td className="td">{client.group}</td>
                            <td className="td">{client.client_ip}</td>
                            <td className="td">{client.tags ? client.tags.join(', ') : ''}</td>
                            <td className="td">{client.status}</td>
                            <td className="td">
                                <input
                                    type="checkbox"
                                    onChange={(e) => handleCheckboxChange(client, e.target.checked)}
                                />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <div className="button-group">
                <button onClick={handleDownloadClients} className="button">Download reserved_clients.json</button>
                <button onClick={handleUnreserveClients} className="button">Unreserve Clients</button>
            </div>
        </div>
    );
}

export default ReservedClients;