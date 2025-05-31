import React, { useState, useEffect } from "react";
import Head from "next/head";
import { getTheaters } from "../utils/theaters";
import { Theater } from "../types/theater";

export default function Theaters() {
  const [theaters, setTheaters] = useState<Theater[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  // Fetch theaters from the API
  useEffect(() => {
    const fetchTheaters = async () => {
      try {
        const data = await getTheaters();
        setTheaters(data);
      } catch (error) {
        console.error("Failed to fetch theaters:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchTheaters();
  }, []);

  return (
    <>
      <Head>
        <title>Theaters - MovieObserver</title>
        <meta
          name="description"
          content="Find theaters showing original language movies"
        />
      </Head>

      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-primary-800 mb-6">Theaters</h1>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {theaters.map((theater) => (
              <div
                key={theater.id}
                className="bg-white shadow-md rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
              >
                <div className="p-6">
                  <h2 className="text-xl font-bold text-gray-900 mb-2">
                    {theater.name}
                  </h2>
                  <p className="text-gray-600 mb-1">{theater.address}</p>
                  <p className="text-gray-600 mb-3">{theater.city}</p>

                  {theater.phone && (
                    <p className="text-gray-600 mb-1">
                      <span className="font-medium">Phone:</span>{" "}
                      {theater.phone}
                    </p>
                  )}

                  {theater.website && (
                    <p className="text-gray-600 mb-3">
                      <span className="font-medium">Website:</span>{" "}
                      <a
                        href={theater.website}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary-600 hover:text-primary-800"
                      >
                        Visit website
                      </a>
                    </p>
                  )}

                  {theater.features && theater.features.length > 0 && (
                    <div className="mt-4">
                      <h3 className="text-sm font-semibold text-gray-700 mb-2">
                        Features:
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {theater.features.map((feature, index) => (
                          <span
                            key={index}
                            className={`px-2 py-1 text-xs rounded-full ${
                              feature === "Original Language"
                                ? "bg-green-100 text-green-800"
                                : "bg-gray-100 text-gray-700"
                            }`}
                          >
                            {feature}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="mt-5">
                    <a
                      href={`/theaters/${theater.id}`}
                      className="text-primary-600 hover:text-primary-800 font-medium"
                    >
                      View showtimes →
                    </a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        <div className="mt-8 bg-gray-50 p-6 rounded-lg">
          <h2 className="text-xl font-semibold text-gray-800 mb-3">
            About Theater Information
          </h2>
          <p className="text-gray-600 mb-3">
            MovieObserver aggregates data from these theaters to help you find
            original language screenings.
          </p>
          <p className="text-gray-600">
            Please note that theater information and showtimes are subject to
            change. We recommend confirming details on the theater's official
            website before your visit.
          </p>
        </div>
      </div>
    </>
  );
}
