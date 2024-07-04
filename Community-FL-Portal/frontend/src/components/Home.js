import React, { useEffect, useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import API from '../api';
import '../styles/Home.css';

function Home() {
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchData = async () => {
            try {
                await API.get('/', {
                    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
                });
            } catch (error) {
                console.error('Error fetching data:', error);
                setError('Failed to load data');
                navigate('/login');
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, [navigate]);

    const handleLogout = () => {
        localStorage.removeItem('token');
        navigate('/login');
    };

    return (
        <div>
            <header className="header">
                <h1>Community FL Portal - Home</h1>
                <div className="nav-links">
                    <button onClick={handleLogout} className="logout-button">Logout</button>
                </div>
            </header>
            <div className="center">
                {loading ? <p>Loading...</p> : error ? <p>{error}</p> : null}
            </div>
            <div className="link-container">
                <div className="link-row">
                    <Link to="/data-scientists" className="button-link">Data Scientists</Link>
                    <Link to="/data-providers" className="button-link">Data Providers</Link>
                </div>
                <div className="link-row">
                    <Link to="/model-providers" className="button-link">Model Providers</Link>
                    <Link to="/infra-providers" className="button-link">Infrastructure Providers</Link>
                </div>
                <div className="link-row">
                    <Link to="/infra-with-data-providers" className="button-link">Infrastructure with Data Providers</Link>
                    <Link to="/instructions" className="button-link">Connect to Infrastructure</Link>
                </div>
                <div className="link-row">
                    <Link to="/discover-clients" className="button-link">Discover Clients</Link>
                    <Link to="/reserved-clients" className="button-link">Reserved Clients</Link>
                </div>
                <div className="link-row">
                    <Link to="/advance-reservation" className="button-link">Advance Reservation</Link>
                </div>
            </div>
        </div>
    );
}

export default Home;