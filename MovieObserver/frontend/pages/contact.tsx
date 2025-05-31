import React, { useState } from "react";
import Head from "next/head";

export default function Contact() {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const [status, setStatus] = useState({
    submitted: false,
    error: false,
    message: "",
  });

  const handleChange = (
    e: React.ChangeEvent<
      HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement
    >
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    // Validate form
    if (!formData.name || !formData.email || !formData.message) {
      setStatus({
        submitted: false,
        error: true,
        message: "Please fill out all required fields",
      });
      return;
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(formData.email)) {
      setStatus({
        submitted: false,
        error: true,
        message: "Please enter a valid email address",
      });
      return;
    }

    // In a real application, you would send the form data to the server here

    // Simulate form submission
    setStatus({
      submitted: true,
      error: false,
      message: "Thank you! Your message has been received.",
    });

    // Reset form
    setFormData({
      name: "",
      email: "",
      subject: "",
      message: "",
    });
  };

  return (
    <>
      <Head>
        <title>Contact Us - MovieObserver</title>
        <meta
          name="description"
          content="Contact MovieObserver for questions, suggestions or feedback"
        />
      </Head>

      <div className="max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-primary-800 mb-6">Contact Us</h1>

        <div className="bg-white shadow-md rounded-lg overflow-hidden mb-8">
          <div className="p-6">
            <p className="text-gray-600 mb-6">
              Have questions, suggestions, or feedback about MovieObserver? We'd
              love to hear from you! Please fill out the form below and we'll
              get back to you as soon as possible.
            </p>

            {status.submitted ? (
              <div className="bg-green-50 border border-green-200 text-green-700 p-4 rounded mb-6">
                {status.message}
              </div>
            ) : status.error ? (
              <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded mb-6">
                {status.message}
              </div>
            ) : null}

            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label
                  htmlFor="name"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Name *
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <div>
                <label
                  htmlFor="email"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Email *
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <div>
                <label
                  htmlFor="subject"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Subject
                </label>
                <select
                  id="subject"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                >
                  <option value="">Select a subject</option>
                  <option value="general">General Question</option>
                  <option value="feedback">Feedback</option>
                  <option value="bug">Report a Bug</option>
                  <option value="feature">Feature Request</option>
                  <option value="other">Other</option>
                </select>
              </div>

              <div>
                <label
                  htmlFor="message"
                  className="block text-sm font-medium text-gray-700 mb-1"
                >
                  Message *
                </label>
                <textarea
                  id="message"
                  name="message"
                  rows={5}
                  value={formData.message}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <button
                type="submit"
                className="w-full bg-primary-600 text-white py-2 px-4 rounded-md hover:bg-primary-700 transition-colors"
              >
                Send Message
              </button>
            </form>
          </div>
        </div>

        <div className="bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl font-semibold text-gray-800 mb-3">
            Other Ways to Reach Us
          </h2>
          <div className="space-y-3">
            <p className="text-gray-600">
              <span className="font-medium">Email:</span>{" "}
              contact@movieobserver.com
            </p>
            <p className="text-gray-600">
              <span className="font-medium">Address:</span> 123 Cinema Street,
              Movie Town, MT 12345
            </p>
            <p className="text-gray-600">
              <span className="font-medium">Hours:</span> Monday - Friday, 9am -
              5pm
            </p>
          </div>
        </div>
      </div>
    </>
  );
}
