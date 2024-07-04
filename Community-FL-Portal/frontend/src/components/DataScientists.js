import React, { useEffect, useState } from 'react';
import API from '../api';
import '../styles/DataScientists.css';

function DataScientists() {
    const [dataScientists, setDataScientists] = useState([]);

    useEffect(() => {
        const fetchDataScientists = async () => {
            try {
                const response = await API.get('/data_scientists', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                setDataScientists(response.data);
            } catch (error) {
                console.error('Error fetching data scientists:', error);
            }
        };
        fetchDataScientists();
    }, []);

    return (
        <div>
            <h2>Data Scientists</h2>
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
                    {dataScientists.map((scientist) => (
                        <tr key={scientist.id}>
                            <td className="td">{scientist.username}</td>
                            <td className="td">{scientist.type}</td>
                            <td className="td">{scientist.group}</td>
                            <td className="td">{scientist.email}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default DataScientists;
