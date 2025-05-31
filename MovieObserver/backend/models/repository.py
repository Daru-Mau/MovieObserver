"""
Repository module for database operations using Supabase
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
from models.supabase import get_client
from models.movie import Movie, Showtime


class MovieRepository:
    """Repository for movie-related database operations"""

    @staticmethod
    async def get_all_movies(date: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all movies for a specific date

        Args:
            date (str, optional): Date in format YYYY-MM-DD. If None, all movies.

        Returns:
            List[Dict[str, Any]]: List of movies
        """
        client = get_client()
        query = client.table('movies').select('*')

        if date:
            query = query.eq('date', date)

        response = query.order('title').execute()
        return response.data

    @staticmethod
    async def get_movie_with_showtimes(movie_id: int) -> Dict[str, Any]:
        """
        Get a movie by ID including its showtimes

        Args:
            movie_id (int): Movie ID

        Returns:
            Dict[str, Any]: Movie with showtimes
        """
        client = get_client()

        # Get movie details
        movie_response = client.table('movies').select(
            '*').eq('id', movie_id).single().execute()

        if not movie_response.data:
            return None

        movie = movie_response.data

        # Get showtimes for this movie
        showtimes_response = client.table('showtimes').select(
            '*').eq('movie_id', movie_id).execute()

        movie['showtimes'] = showtimes_response.data
        return movie

    @staticmethod
    async def insert_or_update_movie(movie: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new movie or update existing one

        Args:
            movie (Dict[str, Any]): Movie data

        Returns:
            Dict[str, Any]: Created or updated movie
        """
        client = get_client()

        # Check if movie exists
        response = client.table('movies').select('id').eq(
            'title', movie['title']).eq('date', movie['date']).execute()

        if response.data:
            # Update existing movie
            movie_id = response.data[0]['id']

            # Remove showtimes from movie for update
            showtimes = movie.pop('showtimes', [])

            # Update movie
            update_response = client.table('movies').update({
                **movie,
                'updated_at': datetime.utcnow().isoformat()
            }).eq('id', movie_id).execute()

            # Handle showtimes separately
            await MovieRepository.update_showtimes(movie_id, showtimes)

            return update_response.data[0] if update_response.data else None
        else:
            # Insert new movie
            # Remove showtimes from movie for insert
            showtimes = movie.pop('showtimes', [])

            # Insert movie
            insert_response = client.table('movies').insert({
                **movie,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }).execute()

            if insert_response.data:
                movie_id = insert_response.data[0]['id']
                # Handle showtimes separately
                await MovieRepository.update_showtimes(movie_id, showtimes)

            return insert_response.data[0] if insert_response.data else None

    @staticmethod
    async def update_showtimes(movie_id: int, showtimes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Update showtimes for a movie

        Args:
            movie_id (int): Movie ID
            showtimes (List[Dict[str, Any]]): Showtimes data

        Returns:
            List[Dict[str, Any]]: Updated showtimes
        """
        client = get_client()

        # Delete existing showtimes
        client.table('showtimes').delete().eq('movie_id', movie_id).execute()

        # Add new showtimes if any
        if showtimes:
            showtimes_data = [{**s, 'movie_id': movie_id} for s in showtimes]
            response = client.table('showtimes').insert(
                showtimes_data).execute()
            return response.data

        return []


class TheaterRepository:
    """Repository for theater-related database operations"""

    @staticmethod
    async def get_all_theaters() -> List[Dict[str, Any]]:
        """
        Get all theaters

        Returns:
            List[Dict[str, Any]]: List of theaters
        """
        client = get_client()
        response = client.table('theaters').select('*').order('name').execute()
        return response.data

    @staticmethod
    async def get_theater(theater_id: int) -> Dict[str, Any]:
        """
        Get a theater by ID

        Args:
            theater_id (int): Theater ID

        Returns:
            Dict[str, Any]: Theater data
        """
        client = get_client()
        response = client.table('theaters').select(
            '*').eq('id', theater_id).single().execute()
        return response.data

    @staticmethod
    async def insert_or_update_theater(theater: Dict[str, Any]) -> Dict[str, Any]:
        """
        Insert a new theater or update existing one

        Args:
            theater (Dict[str, Any]): Theater data

        Returns:
            Dict[str, Any]: Created or updated theater
        """
        client = get_client()

        # Check if theater exists by name
        response = client.table('theaters').select(
            'id').eq('name', theater['name']).execute()

        if response.data:
            # Update existing theater
            theater_id = response.data[0]['id']
            update_response = client.table('theaters').update({
                **theater,
                'updated_at': datetime.utcnow().isoformat()
            }).eq('id', theater_id).execute()
            return update_response.data[0] if update_response.data else None
        else:
            # Insert new theater
            insert_response = client.table('theaters').insert({
                **theater,
                'created_at': datetime.utcnow().isoformat(),
                'updated_at': datetime.utcnow().isoformat()
            }).execute()
            return insert_response.data[0] if insert_response.data else None
