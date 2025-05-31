import React from "react";
import Link from "next/link";
import Image from "next/image";

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

interface MovieCardProps {
  movie: Movie;
}

const MovieCard = ({ movie }: MovieCardProps) => {
  // Group showtimes by theater
  const showtimesByTheater = movie.showtimes.reduce((acc, showtime) => {
    if (!acc[showtime.theater]) {
      acc[showtime.theater] = [];
    }
    acc[showtime.theater].push(showtime);
    return acc;
  }, {} as Record<string, Showtime[]>);

  return (
    <div className="card">
      <div className="flex flex-col md:flex-row">
        {/* Movie Poster */}
        <div className="md:w-1/4 lg:w-1/5">
          <div className="relative h-60 md:h-full w-full">
            {movie.image_url ? (
              <Image
                src={movie.image_url}
                alt={movie.title}
                fill
                className="object-cover"
              />
            ) : (
              <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                <span className="text-gray-500">No image</span>
              </div>
            )}
          </div>
        </div>

        {/* Movie Details */}
        <div className="flex-1 p-4">
          <h3 className="text-xl font-bold text-gray-900">{movie.title}</h3>

          {movie.original_title && movie.original_title !== movie.title && (
            <p className="text-sm text-gray-500 italic mb-2">
              Original title: {movie.original_title}
            </p>
          )}

          <div className="flex flex-wrap gap-2 mb-2">
            {movie.genres?.map((genre, index) => (
              <span
                key={index}
                className="px-2 py-1 bg-gray-100 text-xs text-gray-700 rounded"
              >
                {genre}
              </span>
            ))}
          </div>

          {movie.duration && (
            <p className="text-sm text-gray-500 mb-2">
              Duration: {Math.floor(movie.duration / 60)}h {movie.duration % 60}
              m
            </p>
          )}

          {movie.rating && (
            <div className="flex items-center mb-3">
              <span className="text-yellow-500">★</span>
              <span className="ml-1 text-sm">{movie.rating.toFixed(1)}/10</span>
            </div>
          )}

          {movie.description && (
            <p className="text-gray-700 mb-4 line-clamp-3">
              {movie.description}
            </p>
          )}

          {/* Showtimes by theater */}
          <div className="mt-4">
            <h4 className="font-semibold text-gray-800 mb-2">Showtimes:</h4>

            {Object.entries(showtimesByTheater).map(([theater, times]) => (
              <div key={theater} className="mb-3">
                <h5 className="font-medium text-gray-700">{theater}</h5>
                <div className="flex flex-wrap gap-2 mt-1">
                  {times.map((showtime, index) => (
                    <Link
                      key={index}
                      href={showtime.booking_url || "#"}
                      className={`px-3 py-1 text-sm rounded border ${
                        showtime.is_original_language
                          ? "border-green-500 bg-green-50 text-green-700"
                          : "border-gray-300 bg-gray-50 text-gray-700"
                      }`}
                    >
                      {showtime.time}
                      {showtime.is_original_language && " (OV)"}
                      {showtime.is_3d && " 3D"}
                    </Link>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MovieCard;
