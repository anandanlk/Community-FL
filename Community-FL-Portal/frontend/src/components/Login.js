import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import API from '../api';
import '../styles/Login.css';

function Login() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState(null);
    const navigate = useNavigate();

    const handleLogin = async (e) => {
        e.preventDefault();
        try {
            const response = await API.post('/login', new URLSearchParams({
                username,
                password
            }));
            localStorage.setItem('token', response.data.access_token);
            navigate('/home');
        } catch (error) {
            console.error('Login failed:', error);
            setError('Login failed. Please check your username and password.');
        }
    };

    return (
        <div className="container">
            <div className="welcome-message">
                <h1>Welcome to Community-based Federated Learning Portal</h1>
            </div>
            <form onSubmit={handleLogin} className="form">
                <h2>Login</h2>
                {error && <p className="error">{error}</p>}
                <div className="mb-10">
                    <label>Username</label>
                    <input
                        type="text"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        className="input"
                    />
                </div>
                <div className="mb-20">
                    <label>Password</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="input"
                    />
                </div>
                <div className="button-group">
                    <button type="submit" className="button">Login</button>
                    <Link to="/register" className="button-link">
                        Register
                    </Link>
                </div>
            </form>
        </div>
    );
}

export default Login;