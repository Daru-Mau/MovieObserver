import axios from 'axios';
import { Theater } from '@/types/theater';

const API_URL = process.env.API_URL || 'http://localhost:8000';

export const getTheaters = async (): Promise<Theater[]> => {
  try {
    const response = await axios.get(`${API_URL}/theaters`);
    return response.data;
  } catch (error) {
    console.error('Error fetching theaters:', error);
    throw error;
  }
};

export const getTheaterById = async (theaterId: string): Promise<Theater> => {
  try {
    const response = await axios.get(`${API_URL}/theaters/${theaterId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching theater with ID ${theaterId}:`, error);
    throw error;
  }
};
