# MovieObserver

![MovieObserver Logo](MovieObserver/frontend/public/logo.png)

MovieObserver is a web application that scrapes movie showtimes from different cinema websites and allows users to find movies playing in theaters, with specific focus on original language screenings.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Application](#running-the-application)
- [Development](#development)
  - [Adding New Scrapers](#adding-new-scrapers)
  - [API Documentation](#api-documentation)
  - [Frontend Development](#frontend-development)
- [Contributing](#contributing)
- [Deployment](#deployment)
- [Legal Considerations](#legal-considerations)
- [License](#license)

## ✨ Features

- Scrapes movie information from multiple cinema websites
- Displays showtimes for selected dates
- Filters movies by original language availability
- View theaters and their features
- Responsive design for mobile and desktop

## 🛠️ Tech Stack

### Backend

- **Python** with FastAPI for the API
- **Supabase** for database storage
- **BeautifulSoup/Selenium** for web scraping

### Frontend

- **Next.js** with React for the UI
- **TypeScript** for type safety
- **Tailwind CSS** for styling

## 📂 Project Structure

```
MovieObserver/
├── backend/
│   ├── api/            # FastAPI endpoints
│   ├── models/         # Data models
│   ├── scraper/        # Web scraping modules
│   └── utils/          # Utility functions
├── frontend/
│   ├── components/     # React components
│   ├── pages/          # Next.js pages
│   ├── public/         # Static assets
│   ├── styles/         # CSS styles
│   ├── types/          # TypeScript type definitions
│   └── utils/          # Utility functions
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- Chrome/Chromium (for Selenium)
- Supabase account

### Installation

You can use the setup scripts for quick installation:

**Windows:**

```powershell
.\setup.ps1
```

**macOS/Linux:**

```bash
chmod +x setup.sh
./setup.sh
```

**Manual Setup:**

1. Clone the repository:

```bash
git clone https://github.com/yourusername/MovieObserver.git
cd MovieObserver
```

2. **Backend Setup:**

```bash
# Create and activate a virtual environment
python -m venv movieobserver-env

# Windows
movieobserver-env\Scripts\Activate.ps1
# macOS/Linux
source movieobserver-env/bin/activate

# Install backend dependencies
cd MovieObserver/backend
pip install -r requirements.txt
```

3. **Frontend Setup:**

```bash
cd ../frontend
npm install
```

### Configuration

1. **Backend Configuration:**

Create a `.env` file in the `backend` directory:

```
SUPABASE_URL=your-supabase-project-url
SUPABASE_KEY=your-supabase-api-key
LOG_LEVEL=INFO
CHROME_DRIVER_PATH=/path/to/chromedriver  # Optional, for custom chromedriver location
```

2. **Frontend Configuration:**

Create a `.env.local` file in the `frontend` directory:

```
API_URL=http://localhost:8000
```

### Running the Application

1. **Supabase Setup:**

Make sure your Supabase project is properly set up with the required tables.

2. **Start Backend Server:**

```bash
cd MovieObserver/backend
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

3. **Start Frontend Development Server:**

```bash
cd MovieObserver/frontend
npm run dev
```

Visit `http://localhost:3000` in your browser to access the application.

## 💻 Development

### Adding New Scrapers

To add new cinema websites for scraping, follow these steps:

1. Create a new scraper class in `backend/scraper/` by extending the `BaseScraper` class
2. Implement the `get_movies_for_date` method for your specific cinema website
3. Add your new scraper to the `scrapers` list in the `ScraperService` class

Example:

```python
# In a new file: backend/scraper/new_cinema_scraper.py
from scraper.base_scraper import BaseScraper

class NewCinemaScraper(BaseScraper):
    def __init__(self, base_url: str = "https://www.new-cinema-website.com"):
        super().__init__(base_url)

    def get_movies_for_date(self, date: str):
        # Implementation for scraping this specific cinema website
        pass

# In scraper_service.py, add:
from scraper.new_cinema_scraper import NewCinemaScraper

# Then add to the scrapers list:
self.scrapers = [
    # Existing scrapers...
    NewCinemaScraper("https://www.new-cinema-website.com")
]
```

Current implemented scrapers:

- Yelmo Cinemas (Spain) - `https://www.yelmocines.es`
- Cinessa Cinemas (Example) - `https://www.cinessa.com`
- UCI Cinemas (Italy) - `https://ucicinemas.it`

### API Documentation

Once the backend is running, you can access the FastAPI documentation:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

Key API endpoints:

- GET `/movies/{date}` - Get movies for a specific date
- GET `/movies/original/{date}` - Get original language movies for a specific date
- GET `/theaters` - Get list of all theaters
- POST `/scrape/now` - Trigger scraping for today
- POST `/scrape/dates?days=7` - Trigger scraping for the next 7 days

### Frontend Development

The frontend is built with Next.js and follows the pages structure. Main components:

- `pages/index.tsx` - Home page with movie listings
- `pages/theaters.tsx` - List of theaters
- `pages/theaters/[id].tsx` - Theater detail page

Key components:

- `MovieList.tsx` - Displays a list of movies with filtering options
- `DateSelector.tsx` - Date selection component
- `FilterOptions.tsx` - Options for filtering movies

## 👥 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

Please make sure to update tests as appropriate and follow the code style.

### Code Style

- **Backend**: Follow PEP 8 guidelines
- **Frontend**: Use ESLint and Prettier configurations

## 🌐 Deployment

### Backend Deployment

1. Build a Docker image for the backend:

```bash
docker build -t movieobserver-backend ./backend
```

2. Deploy using your preferred hosting service (AWS, Google Cloud, Heroku, etc.)

### Frontend Deployment

Deploy using Vercel (recommended for Next.js applications):

```bash
cd frontend
vercel
```

Or build for production:

```bash
npm run build
npm start
```

## ⚖️ Legal Considerations

Before deploying this application, ensure you have reviewed the Terms of Service of the websites you're scraping. Web scraping may not be allowed by some websites, and legal restrictions may apply.

## 📄 License

[MIT License](LICENSE)

---

Made with ❤️ by [Your Name]
