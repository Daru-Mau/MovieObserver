import React from 'react';
import MovieCard from './MovieCard';

interface Showtime {
  time: string;
  theater: string;
  room: string;
  is_original_language: boolean;
  is_3d: boolean;
  booking_url?: string;
}

interface Movie {
  title: string;
  original_title?: string;
  date: string;
  image_url?: string;
  description?: string;
  duration?: number;
  genres?: string[];
  rating?: number;
  showtimes: Showtime[];
}

interface MovieListProps {
  movies: Movie[];
}

const MovieList = ({ movies }: MovieListProps) => {
  if (!movies || movies.length === 0) {
    return (
      <div className="text-center py-12 bg-gray-50 rounded-lg">
        <h3 className="text-xl text-gray-600">No movies found for this date</h3>
        <p className="text-gray-500 mt-2">Try selecting a different date or removing filters</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {movies.map((movie, index) => (
        <MovieCard key={index} movie={movie} />
      ))}
    </div>
  );
};

export default MovieList;
