import React from "react";
import Link from "next/link";
import Image from "next/image";
import Icon from "./Icon";

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
            {" "}
            {movie.image_url &&
            movie.image_url.startsWith("https://image.tmdb.org/") ? (
              <Image
                src={movie.image_url}
                alt={movie.title}
                fill
                sizes="(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw"
                className="object-cover"
              />
            ) : (
              <div className="w-full h-full bg-gray-200 flex items-center justify-center">
                <Icon name="movie" size={48} className="text-gray-400" />
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
          </div>{" "}
          {movie.duration && (
            <div className="flex items-center text-sm text-gray-500 mb-2">
              <Icon name="showtime" size={16} className="mr-1" />
              Duration: {Math.floor(movie.duration / 60)}h {movie.duration % 60}
              m
            </div>
          )}{" "}
          {movie.rating && (
            <div className="flex items-center mb-3">
              <Icon name="rating" size={16} className="mr-1" />
              <span className="ml-1 text-sm">{movie.rating.toFixed(1)}/10</span>
            </div>
          )}
          {movie.description && (
            <p className="text-gray-700 mb-4 line-clamp-3">
              {movie.description}
            </p>
          )}{" "}
          {/* Showtimes by theater */}
          <div className="mt-4">
            <div className="flex items-center mb-2">
              <Icon name="theater" size={16} className="mr-1" />
              <h4 className="font-semibold text-gray-800">Showtimes:</h4>
            </div>

            {Object.entries(showtimesByTheater).map(([theater, times]) => (
              <div key={theater} className="mb-3">
                <h5 className="font-medium text-gray-700">{theater}</h5>
                <div className="flex flex-wrap gap-2 mt-1">
                  {times.map((showtime, index) => (
                    <Link
                      key={index}
                      href={showtime.booking_url || "#"}
                      className={`inline-flex items-center px-3 py-1 text-sm rounded border ${
                        showtime.is_original_language
                          ? "border-green-500 bg-green-50 text-green-700"
                          : "border-gray-300 bg-gray-50 text-gray-700"
                      }`}
                    >
                      <Icon name="ticket" size={14} className="mr-1" />
                      {showtime.time}
                      {showtime.is_original_language && (
                        <Icon
                          name="original-language"
                          size={14}
                          className="ml-1"
                        />
                      )}
                      {showtime.is_3d && (
                        <Icon name="3d" size={14} className="ml-1" />
                      )}
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
