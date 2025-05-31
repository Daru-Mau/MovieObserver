import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import Head from "next/head";
import Link from "next/link";
import { format } from "date-fns";
import { getTheaterById } from "../../utils/theaters";
import { Theater, Movie } from "../../types/theater";

export default function TheaterDetail() {
  const router = useRouter();
  const { id } = router.query;

  const [theater, setTheater] = useState<Theater | null>(null);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDate] = useState<Date>(new Date());

  useEffect(() => {
    if (!id) return;

    const fetchTheater = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch theater details
        const theaterData = await getTheaterById(id as string);
        setTheater(theaterData);

        // In a real app, you would fetch movies for this theater
        // For now, we'll use mock data
        setMovies([]);
      } catch (err) {
        console.error("Failed to fetch theater:", err);
        setError("Failed to load theater information. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchTheater();
  }, [id]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error || !theater) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded mb-6">
        {error || "Theater not found"}
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>{theater.name} - MovieObserver</title>
        <meta
          name="description"
          content={`Movie showtimes at ${theater.name}`}
        />
      </Head>

      <div>
        {/* Breadcrumbs */}
        <div className="text-sm mb-6">
          <Link href="/" className="text-primary-600 hover:text-primary-800">
            Home
          </Link>
          {" > "}
          <Link
            href="/theaters"
            className="text-primary-600 hover:text-primary-800"
          >
            Theaters
          </Link>
          {" > "}
          <span className="text-gray-700">{theater.name}</span>
        </div>

        {/* Theater Info */}
        <div className="bg-white shadow-md rounded-lg overflow-hidden mb-8">
          <div className="p-6">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {theater.name}
            </h1>
            <p className="text-gray-600 mb-1">{theater.address}</p>
            <p className="text-gray-600 mb-3">{theater.city}</p>

            <div className="flex flex-wrap gap-4 mb-4">
              {theater.phone && (
                <p className="text-gray-600">
                  <span className="font-medium">Phone:</span> {theater.phone}
                </p>
              )}

              {theater.website && (
                <p className="text-gray-600">
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
            </div>

            {theater.features && theater.features.length > 0 && (
              <div className="mt-4">
                <h3 className="text-sm font-semibold text-gray-700 mb-2">
                  Features:
                </h3>
                <div className="flex flex-wrap gap-2">
                  {theater.features.map((feature, index) => (
                    <span
                      key={index}
                      className={`px-3 py-1 text-sm rounded-full ${
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
          </div>
        </div>

        {/* Movies Section */}
        <div>
          <h2 className="text-2xl font-bold text-gray-800 mb-4">
            Movies Playing on {format(selectedDate, "MMMM d, yyyy")}
          </h2>

          {movies.length > 0 ? (
            <div className="space-y-6">
              {/* Movie list would go here */}
              <p>Movie list coming soon</p>
            </div>
          ) : (
            <div className="bg-gray-50 p-6 rounded-lg text-center">
              <p className="text-gray-600">
                No movies available for this date at {theater.name}.
              </p>
              <p className="text-gray-500 mt-2">
                Please check back later or try another date.
              </p>
            </div>
          )}
        </div>
      </div>
    </>
  );
}
