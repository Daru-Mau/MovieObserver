# Movie Observer Frontend

This is the frontend for the MovieObserver application, built using Next.js, React, and Tailwind CSS.

## Getting Started

First, install the dependencies:

```bash
npm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

## Backend Connection

This frontend is designed to work with the MovieObserver backend API. Make sure the backend server is running on http://localhost:8000 before trying to fetch data.

You can configure the backend API URL in the `.env.local` file:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

- `components/`: Reusable React components
- `pages/`: Next.js pages
- `public/`: Static assets
- `styles/`: CSS files
- `utils/`: Utility functions

## Features

- Display movies playing in theaters
- Filter by original language screenings
- Select movie showtimes by date
- Show theater information and booking options
