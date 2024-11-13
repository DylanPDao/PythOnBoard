// src/components/JobListings.js
import React, { useEffect, useState } from 'react';
import axios from 'axios';

const JobListings = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                // Fetch data from FastAPI backend
                const response = await axios.get('http://127.0.0.1:8000/jobs', {
                    params: {
                        job_name: 'Software Developer',
                        location: '92843'
                    }
                });
                setJobs(response.data.jobs);
            } catch (err) {
                setError('Could not fetch job listings.');
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchJobs();
    }, []);

    if (loading) return <div>Loading...</div>;
    if (error) return <div>{error}</div>;

    return (
        <div>
            <h1>Job Listings</h1>
            <ul>
                {jobs.map((job, index) => (
                    <li key={index}>
                        <h2>{job.title}</h2>
                        <p>{job.company}</p>
                        <p>{job.location}</p>
                        <a href={job.url} target="_blank" rel="noopener noreferrer">View Job</a>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default JobListings;
