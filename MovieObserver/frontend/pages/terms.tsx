import React from "react";
import Head from "next/head";

export default function Terms() {
  return (
    <>
      <Head>
        <title>Terms of Service - MovieObserver</title>
        <meta name="description" content="MovieObserver Terms of Service" />
      </Head>

      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-primary-800 mb-6">
          Terms of Service
        </h1>

        <div className="prose prose-lg text-gray-600 max-w-none">
          <p>Last updated: May 31, 2025</p>

          <h2 className="text-2xl font-semibold text-gray-800 my-4">
            1. Introduction
          </h2>
          <p>
            Welcome to MovieObserver ("we," "our," or "us"). These Terms of
            Service ("Terms") govern your access to and use of our website,
            services, and applications (collectively, the "Service").
          </p>
          <p>
            By accessing or using our Service, you agree to be bound by these
            Terms. If you disagree with any part of the Terms, you do not have
            permission to access the Service.
          </p>

          <h2 className="text-2xl font-semibold text-gray-800 my-4">
            2. Use of the Service
          </h2>
          <p>
            MovieObserver provides information about movie showtimes and
            theaters, with a focus on original language screenings. Our service
            aggregates publicly available data from movie theaters and cinema
            websites.
          </p>
          <p>
            You may use our Service only as permitted by law and these Terms.
            The Service and all content, information, and functionality are
            protected by copyright, trademark, and other laws.
          </p>

          <h2 className="text-2xl font-semibold text-gray-800 my-4">
            3. User Accounts
          </h2>
          <p>
            Some features of our Service may require you to register for an
            account. You agree to provide accurate, current, and complete
            information during the registration process and to update such
            information to keep it accurate, current, and complete.
          </p>
          <p>
            You are responsible for safeguarding your account and for all
            activities that occur under your account. You must notify us
            immediately of any unauthorized use of your account.
          </p>

          <h2 className="text-2xl font-semibold text-gray-800 my-4">
            4. Content Accuracy
          </h2>
          <p>
            While we strive to provide accurate and up-to-date information about
            movie showtimes and theaters, we cannot guarantee the accuracy or
            completeness of this information. Movie schedules, prices, and
            availability are subject to change by the theaters themselves.
          </p>
          <p>
            We recommend confirming all information directly with the theater
            before making plans.
          </p>

          <h2 className="text-2xl font-semibold text-gray-800 my-4">
            5. Privacy
          </h2>
          <p>
            Our Privacy Policy explains how we collect, use, and protect your
            personal information. By using our Service, you agree to our
            collection and use of information in accordance with our Privacy
            Policy.
          </p>

          <h2 className="text-2xl font-semibold text-gray-800 my-4">
            6. Changes to Terms
          </h2>
          <p>
            We may modify these Terms at any time. If we make material changes
            to these Terms, we will notify you by email or by posting a notice
            on our website. Your continued use of the Service after such
            notification constitutes your acceptance of the new Terms.
          </p>

          <h2 className="text-2xl font-semibold text-gray-800 my-4">
            7. Contact Us
          </h2>
          <p>
            If you have any questions about these Terms, please contact us at:
          </p>
          <p>
            Email: legal@movieobserver.com
            <br />
            Address: 123 Cinema Street, Movie Town, MT 12345
          </p>
        </div>
      </div>
    </>
  );
}
