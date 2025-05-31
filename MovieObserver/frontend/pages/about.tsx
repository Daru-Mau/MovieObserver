import React from 'react';
import Head from 'next/head';

const About = () => {
  return (
    <>
      <Head>
        <title>About - MovieObserver</title>
        <meta name="description" content="Learn about the MovieObserver app and how it helps you find movies in original language" />
      </Head>

      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-primary-800 mb-6">About MovieObserver</h1>
        
        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-3">Our Mission</h2>
          <p className="text-gray-600 mb-4">
            MovieObserver was created to help moviegoers easily find information about screenings in original language, 
            allowing you to enjoy films as they were meant to be seen.
          </p>
          <p className="text-gray-600">
            We aggregate data from multiple cinema websites to present you with a clear, unified view of 
            what's playing and where, with special attention to original language options.
          </p>
        </section>
        
        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-3">How It Works</h2>
          <p className="text-gray-600 mb-4">
            Our system automatically collects showtime data from cinema websites multiple times a day,
            ensuring you always have the latest information at your fingertips.
          </p>
          <div className="bg-gray-50 p-6 rounded-lg mt-4">
            <h3 className="text-lg font-medium mb-3 text-primary-700">Features:</h3>
            <ul className="list-disc pl-5 space-y-2 text-gray-700">
              <li>Find movies playing on specific dates</li>
              <li>Filter to show only original language screenings</li>
              <li>See all theaters showing a specific movie</li>
              <li>Direct links to booking pages</li>
              <li>Movie details including duration and genres</li>
            </ul>
          </div>
        </section>
        
        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-3">Contact Us</h2>
          <p className="text-gray-600">
            Have questions or suggestions? We'd love to hear from you!
          </p>
          <p className="text-gray-600 mt-3">
            Email: <a href="mailto:contact@movieobserver.com" className="text-primary-600 hover:text-primary-800">contact@movieobserver.com</a>
          </p>
        </section>
      </div>
    </>
  );
};

export default About;
