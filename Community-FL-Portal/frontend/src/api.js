import axios from 'axios';

const baseURL = process.env.REACT_APP_API_BASE_URL;
console.log('API Base URL:', baseURL);

const API = axios.create({
    baseURL,
    // baseURL: 'http://localhost:8088/user',
});

export default API;