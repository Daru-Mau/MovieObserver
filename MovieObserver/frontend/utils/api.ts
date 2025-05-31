import axios from 'axios';
import { Theater, Movie } from '../types/theater';

const API_URL = process.env.API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getMovies = async (date: string): Promise<Movie[]> => {
  try {
    const response = await api.get(`/movies/${date}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching movies:', error);
    throw error;
  }
};

export const getOriginalLanguageMovies = async (date: string): Promise<Movie[]> => {
  try {
    const response = await api.get(`/movies/original/${date}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching original language movies:', error);
    throw error;
  }
};

export const getTheaters = async (): Promise<Theater[]> => {
  try {
    const response = await api.get('/theaters');
    return response.data;
  } catch (error) {
    console.error('Error fetching theaters:', error);
    throw error;
  }
};

export const getTheaterById = async (theaterId: string): Promise<Theater> => {
  try {
    const response = await api.get(`/theaters/${theaterId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching theater with ID ${theaterId}:`, error);
    throw error;
  }
};

export default api;
