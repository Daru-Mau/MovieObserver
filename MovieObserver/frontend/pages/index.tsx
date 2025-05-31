import React, { useState, useEffect } from "react";
import Head from "next/head";
import { format, addDays } from "date-fns";
import DateSelector from "../components/DateSelector";
import MovieList from "../components/MovieList";
import FilterOptions from "../components/FilterOptions";
import { getMovies, getOriginalLanguageMovies } from "../utils/api";
import type { Movie } from "../types/theater";

export default function Home() {
  const [selectedDate, setSelectedDate] = useState<Date>(new Date());
  const [showOriginalOnly, setShowOriginalOnly] = useState<boolean>(false);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Generate dates for the next 7 days
  const nextDays = Array.from({ length: 7 }, (_, i) => addDays(new Date(), i));

  // Fetch movies for the selected date
  useEffect(() => {
    const fetchMovies = async () => {
      setLoading(true);
      setError(null);

      try {
        const dateStr = format(selectedDate, "yyyy-MM-dd");
        const movies = showOriginalOnly
          ? await getOriginalLanguageMovies(dateStr)
          : await getMovies(dateStr);

        setMovies(movies);
      } catch (err) {
        setError("Error loading movies. Please try again later.");
        console.error("Error fetching movies:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchMovies();
  }, [selectedDate, showOriginalOnly]);

  return (
    <>
      <Head>
        <title>Movie Observer - Find Movies in Theaters</title>
      </Head>

      <section className="mb-6">
        <h1 className="text-3xl font-bold text-primary-800 mb-2">
          Movie Showtimes
        </h1>
        <p className="text-gray-600">
          Find movies playing in theaters today, with options for original
          language screenings.
        </p>
      </section>

      <DateSelector
        dates={nextDays}
        selectedDate={selectedDate}
        onSelectDate={setSelectedDate}
      />

      <FilterOptions
        showOriginalOnly={showOriginalOnly}
        setShowOriginalOnly={setShowOriginalOnly}
      />

      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
        </div>
      ) : error ? (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      ) : (
        <MovieList movies={movies} />
      )}
    </>
  );
}
