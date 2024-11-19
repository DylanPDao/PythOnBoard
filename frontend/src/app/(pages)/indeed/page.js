// src/pages/index.js
import React from 'react';
import JobListings from '../../../components/joblistings';

const HomePage = () => {
    return (
        <div>
            <h1>Job Search App</h1>
            <JobListings />
        </div>
    );
};

export default HomePage;