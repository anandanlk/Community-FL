import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import API from '../api';
import '../styles/Register.css';

function Register() {
    const [formData, setFormData] = useState({
        username: '',
        password: '',
        email: '',
        type: '',
        group: '',
        modelURL: '',
        dataURL: ''
    });
    const [error, setError] = useState(null);
    const [uid, setUid] = useState(null);
    const navigate = useNavigate();

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleRegister = async (e) => {
        e.preventDefault();
        try {
            const response = await API.post('/register', formData);
            setUid(response.data.uid);
        } catch (error) {
            console.error('Registration failed:', error);
            if (error.response && error.response.data) {
                setError(error.response.data.message || 'Registration failed. Please check your inputs.');
            } else {
                setError('Registration failed. Please check your inputs.');
            }
        }
    };

    return (
        <div className="register-container">
            <form onSubmit={handleRegister} className="register-form">
                {error && <p className="register-error-message">{error}</p>}
                {uid && (
                    <div className="register-success-message" style={{ color: 'green' }}>
                        <p>Registration successful! Your UID is: {uid}</p>
                        <Link to="/login">Click here to Login</Link>
                    </div>
                )}
                {!uid && (
                    <>
                        <div className="register-form-group">
                            <label>Username</label>
                            <input
                                type="text"
                                name="username"
                                value={formData.username}
                                onChange={handleChange}
                            />
                        </div>
                        <div className="register-form-group">
                            <label>Password</label>
                            <input
                                type="password"
                                name="password"
                                value={formData.password}
                                onChange={handleChange}
                            />
                        </div>
                        <div className="register-form-group">
                            <label>Email</label>
                            <input
                                type="email"
                                name="email"
                                value={formData.email}
                                onChange={handleChange}
                            />
                        </div>
                        <div className="register-form-group">
                            <label>Type</label>
                            <select
                                name="type"
                                value={formData.type}
                                onChange={handleChange}
                            >
                                <option value="">Select Type</option>
                                <option value="Data Scientist">Data Scientist</option>
                                <option value="Data Provider">Data Provider</option>
                                <option value="Infrastructure Provider">Infrastructure Provider</option>
                                <option value="Infrastructure with Data Provider">Infrastructure with Data Provider</option>
                                <option value="Model Provider">Model Provider</option>
                            </select>
                        </div>
                        {formData.type === 'Model Provider' && (
                            <div className="register-form-group">
                                <label>Model URL</label>
                                <input
                                    type="text"
                                    name="modelURL"
                                    value={formData.modelURL}
                                    onChange={handleChange}
                                />
                            </div>
                        )}
                        {formData.type === 'Data Provider' && (
                            <div className="register-form-group">
                                <label>Data URL</label>
                                <input
                                    type="text"
                                    name="dataURL"
                                    value={formData.dataURL}
                                    onChange={handleChange}
                                />
                            </div>
                        )}
                        <div className="register-form-group">
                            <label>Group</label>
                            <input
                                type="text"
                                name="group"
                                value={formData.group}
                                onChange={handleChange}
                            />
                        </div>
                        <button type="submit" className="register-button">Register</button>
                    </>
                )}
            </form>
        </div>
    );
}

export default Register;