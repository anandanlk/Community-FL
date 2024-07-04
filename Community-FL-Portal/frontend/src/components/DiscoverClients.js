import React, { useEffect, useState } from 'react';
import API from '../api';
import '../styles/DiscoverClients.css';

function DiscoverClients() {
    const [clientList, setClientList] = useState([]);
    const [selectedClients, setSelectedClients] = useState([]);
    const [errorMessage, setErrorMessage] = useState('');
    const [successMessage, setSuccessMessage] = useState('');

    useEffect(() => {
        const fetchClientList = async () => {
            try {
                const response = await API.get('/discover_clients', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                setClientList(response.data);
            } catch (error) {
                console.error('Error fetching client list:', error);
                setErrorMessage('Error fetching client list. Please try again.');
            }
        };
        fetchClientList();
    }, []);

    const handleCheckboxChange = (client, isChecked) => {
        if (isChecked) {
            setSelectedClients(prev => [...prev, client]);
        } else {
            setSelectedClients(prev => prev.filter(c => c.username !== client.username));
        }
    };

    const handleReserveClients = async () => {
        try {
            const payload = selectedClients.map(client => ({
                username: client.username,
                client_ip: client.client_ip
            }));

            console.log('Selected Clients Payload:', payload);

            await API.post('/reserve_clients', payload, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
            });

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

            setSuccessMessage('Clients reserved successfully.');
            setSelectedClients([]);

            setTimeout(() => {
                setSuccessMessage('');
                window.location.reload();
            }, 2000);

        } catch (error) {
            setErrorMessage('An error occurred while reserving clients. Please try again.');
            console.error('Error reserving clients:', error);
        }
    };

    return (
        <div>
            <h2>Discovered Clients</h2>
            {errorMessage && <p className="error-message">{errorMessage}</p>}
            {successMessage && <p className="success-message">{successMessage}</p>}
            <table className="table">
                <thead>
                    <tr>
                        <th className="th">S.No</th>
                        <th className="th">Username</th>
                        <th className="th">Type</th>
                        <th className="th">Group</th>
                        <th className="th">Email</th>
                        <th className="th">Tags</th>
                        <th className="th">Status</th>
                        <th className="th">Reserved By</th>
                        <th className="th">Reserve</th>
                    </tr>
                </thead>
                <tbody>
                    {clientList.map((client, index) => (
                        <tr key={index}>
                            <td className="td">{index + 1}</td>
                            <td className="td">{client.username}</td>
                            <td className="td">{client.type}</td>
                            <td className="td">{client.group}</td>
                            <td className="td">{client.email}</td>
                            <td className="td">{client.tags ? client.tags.join(', ') : ''}</td>
                            <td className="td">{client.status === 'Online' ? 'Online' : 'Offline'}</td>
                            <td className="td">{client.reserved_by || ''}</td>
                            <td className="td">
                                <input
                                    type="checkbox"
                                    onChange={(e) => handleCheckboxChange(client, e.target.checked)}
                                    disabled={client.status !== 'Online' || client.reserved_by}
                                    className={(client.status !== 'Online' || client.reserved_by) ? 'checkbox-disabled' : ''}
                                />
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
            <button onClick={handleReserveClients} className="button">Reserve Clients</button>
        </div>
    );
}

export default DiscoverClients;