import React from 'react';
import Head from 'next/head';

export default function Privacy() {
  return (
    <>
      <Head>
        <title>Privacy Policy - MovieObserver</title>
        <meta name="description" content="MovieObserver Privacy Policy" />
      </Head>

      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-primary-800 mb-6">Privacy Policy</h1>
        
        <div className="prose prose-lg text-gray-600 max-w-none">
          <p>
            Last updated: May 31, 2025
          </p>
          
          <h2 className="text-2xl font-semibold text-gray-800 my-4">1. Introduction</h2>
          <p>
            At MovieObserver, we respect your privacy and are committed to protecting your personal data. This Privacy Policy explains how we collect, use, disclose, and safeguard your information when you use our website or services.
          </p>
          <p>
            Please read this Privacy Policy carefully. If you do not agree with the terms of this Privacy Policy, please do not access our website or use our services.
          </p>
          
          <h2 className="text-2xl font-semibold text-gray-800 my-4">2. Information We Collect</h2>
          <p>
            We may collect several types of information from and about users of our website, including:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li>Personal information such as name and email address when you contact us or create an account</li>
            <li>Usage data about how you interact with our website</li>
            <li>Technical data such as IP address, browser type, and device information</li>
            <li>Cookie data as described in our Cookie Policy</li>
          </ul>
          
          <h2 className="text-2xl font-semibold text-gray-800 my-4">3. How We Use Your Information</h2>
          <p>
            We use the information we collect to:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li>Provide and maintain our service</li>
            <li>Notify you about changes to our service</li>
            <li>Allow you to participate in interactive features when you choose to do so</li>
            <li>Provide customer support</li>
            <li>Monitor and analyze usage patterns and trends</li>
            <li>Improve our website and user experience</li>
          </ul>
          
          <h2 className="text-2xl font-semibold text-gray-800 my-4">4. Disclosure of Your Information</h2>
          <p>
            We may disclose your personal information:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li>To comply with legal obligations</li>
            <li>To protect and defend our rights or property</li>
            <li>To prevent or investigate possible wrongdoing in connection with the service</li>
            <li>To protect the personal safety of users of the service or the public</li>
            <li>To protect against legal liability</li>
          </ul>
          <p>
            We do not sell, trade, or otherwise transfer your personal information to third parties without your consent, except as described in this Privacy Policy.
          </p>
          
          <h2 className="text-2xl font-semibold text-gray-800 my-4">5. Data Security</h2>
          <p>
            We implement reasonable security measures to protect your personal information. However, please be aware that no method of transmission over the internet or electronic storage is 100% secure, and we cannot guarantee absolute security.
          </p>
          
          <h2 className="text-2xl font-semibold text-gray-800 my-4">6. Your Data Protection Rights</h2>
          <p>
            Depending on your location, you may have certain rights regarding your personal data, including:
          </p>
          <ul className="list-disc pl-6 space-y-2">
            <li>The right to access, update, or delete your information</li>
            <li>The right to rectification if your information is inaccurate or incomplete</li>
            <li>The right to object to our processing of your personal data</li>
            <li>The right to request restriction of processing your personal data</li>
            <li>The right to data portability</li>
            <li>The right to withdraw consent</li>
          </ul>
          
          <h2 className="text-2xl font-semibold text-gray-800 my-4">7. Changes to This Privacy Policy</h2>
          <p>
            We may update our Privacy Policy from time to time. We will notify you of any changes by posting the new Privacy Policy on this page and updating the "Last updated" date.
          </p>
          <p>
            You are advised to review this Privacy Policy periodically for any changes. Changes to this Privacy Policy are effective when they are posted on this page.
          </p>
          
          <h2 className="text-2xl font-semibold text-gray-800 my-4">8. Contact Us</h2>
          <p>
            If you have any questions about this Privacy Policy, please contact us at:
          </p>
          <p>
            Email: privacy@movieobserver.com<br />
            Address: 123 Cinema Street, Movie Town, MT 12345
          </p>
        </div>
      </div>
    </>
  );
}
