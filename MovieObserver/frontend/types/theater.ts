export interface Theater {
  id: string;
  name: string;
  address: string;
  city: string;
  website?: string;
  phone?: string;
  features?: string[];
}

export interface Movie {
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

export interface Showtime {
  time: string;
  theater: string;
  room: string;
  is_original_language: boolean;
  is_3d: boolean;
  booking_url?: string;
}
