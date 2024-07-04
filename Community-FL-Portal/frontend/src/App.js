// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Home from './components/Home';
import DataProviders from './components/DataProviders';
import InfraProviders from './components/InfraProviders';
import DiscoverClients from './components/DiscoverClients';
import DataScientists from './components/DataScientists';
import InfraWithDataProviders from './components/InfraWithDataProviders';
import Instructions from './components/Instructions';
import ReservedClients from './components/ReservedClients';
import ModelProviders from './components/ModelProviders';
import AdvanceReservation from './components/AdvanceReservation';

function App() {
    return (
        <Router>
            <div>
                <Routes>
                    <Route path="/login" element={<Login />} />
                    <Route path="/register" element={<Register />} />
                    <Route path="/home" element={<Home />} />
                    <Route path="/data-providers" element={<DataProviders />} />
                    <Route path="/infra-providers" element={<InfraProviders />} />
                    <Route path="/infra-with-data-providers" element={<InfraWithDataProviders />} />
                    <Route path="/data-scientists" element={<DataScientists />} />
                    <Route path="/instructions" element={<Instructions />} />
                    <Route path="/discover-clients" element={<DiscoverClients />} />
                    <Route path="/reserved-clients" element={<ReservedClients />} />
                    <Route path="/model-providers" element={<ModelProviders />} />
                    <Route path="/advance-reservation" element={<AdvanceReservation />} />
                    <Route path="*" element={<Navigate to="/login" />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;