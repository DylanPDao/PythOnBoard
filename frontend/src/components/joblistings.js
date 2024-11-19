// src/components/JobListings.js
"use client";

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
  } from "@/components/ui/card"
  import { Button } from "@/components/ui/button"
  import Link from 'next/link';



const JobListings = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                // Fetch data from FastAPI backend
                const response = await axios.get('http://127.0.0.1:8000/indeed_jobs', {
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
                    <Card>
                        <CardHeader>
                            <CardTitle>{job.title}</CardTitle>
                            <CardDescription>{job.title}</CardDescription>
                        </CardHeader>
                    </Card>
                    <CardContent>
                        <p>Content</p>   
                    </CardContent>
                    <CardFooter>
                        <p>{job.location}</p>
                        <Button asChild>
                            <Link href={job.url}>View</Link>
                        </Button>
                    </CardFooter>
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default JobListings;
