import React, { useState } from 'react';
import API from '../api';
import '../styles/AdvanceReservation.css';

function AdvanceReservation() {
    const [formData, setFormData] = useState({ no_of_clients: '', duration: '' });
    const [successMessage, setSuccessMessage] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await API.post('/advance_reservation', formData, {
                headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
            });
            if (response.data.reservation === 'accepted') {
                setSuccessMessage('Reservation successfully placed!');
            }
        } catch (error) {
            console.error('Failed to place reservation:', error);
        }
    };

    return (
        <div className="container">
            <form onSubmit={handleSubmit} className="form">
                {successMessage && <p className="success-message">{successMessage}</p>}
                <div className="mb-10">
                    <label>No. of Clients</label>
                    <input
                        type="number"
                        name="no_of_clients"
                        value={formData.no_of_clients}
                        onChange={handleChange}
                        className="input"
                        required
                    />
                </div>
                <div className="mb-20">
                    <label>Duration (In Hours)</label>
                    <input
                        type="number"
                        name="duration"
                        value={formData.duration}
                        onChange={handleChange}
                        className="input"
                        required
                    />
                </div>
                <button type="submit" className="button">Submit</button>
            </form>
        </div>
    );
}

export default AdvanceReservation;