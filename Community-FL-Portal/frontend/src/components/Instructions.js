import React, { useEffect, useState } from 'react';
import API from '../api';
import '../styles/Instructions.css';

function Instructions() {
    const [uid, setUid] = useState('');
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchUid = async () => {
            try {
                const response = await API.get('/uid', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
                setUid(response.data.uid);
            } catch (error) {
                console.error('Error fetching UID:', error);
                setError('Failed to load UID');
            } finally {
                setLoading(false);
            }
        };
        fetchUid();
    }, []);

    const handleDownload = () => {
        const data = {
            uid: uid,
            tags: ["MINST", "Decentralized", "Labelled"]
        };
        const jsonString = `data:text/json;charset=utf-8,${encodeURIComponent(JSON.stringify(data))}`;
        const link = document.createElement('a');
        link.href = jsonString;
        link.download = 'connection.json';

        link.click();
    };

    return (
        <div>
            <header className="header">
                <h1>Instructions to connect your Client (nodes) to the Community FL Portal</h1>
            </header>
            <div className="content">
                <ol>
                    <li>
                        Place the data in the home directory.
                        <p>Sample data: <a href="https://github.com/anandanlk/Compose/raw/main/enumerated_tensors_5_version1.pth">Download here</a></p>
                    </li>
                    <li>
                        Place the <code>connection.json</code> file in the home directory of your client (FL node) machine. This file contains your UID and sample tags. Please update the tags as per your data set.
                        <pre>
                            <code>
                                {"{"}"uid": "{uid}", "tags": ["MINST", "Decentralized", "Labelled"]{"}"}
                            </code>
                        </pre>
                        <button onClick={handleDownload}>Download connection.json</button>
                    </li>
                    <li>
                        Pull and deploy the following docker containers:
                        <p><code>anandanlk/client_register:latest</code></p>
                        <p><code>anandanlk/client_decentralized:latest</code></p>
                        <p>
                           Please use <a href="https://github.com/anandanlk/Compose"> client_compose.yml</a> docker-compose file to deploy the docker containers. The required data and connection.json files 
                           needs to be in the current directory from where the docker-compose command is executed.
                        </p>
                    </li>
                </ol>
                {loading ? <p>Loading...</p> : error ? <p>{error}</p> : <p className="uid">Your UID is: {uid}</p>}
            </div>
        </div>
    );
}

export default Instructions;