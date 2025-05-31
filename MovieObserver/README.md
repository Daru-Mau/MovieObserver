# MovieObserver

MovieObserver is a web application that scrapes movie showtimes from different cinema websites and allows users to find movies playing in theaters, with specific focus on original language screenings.

## Features

- Scrapes movie information from multiple cinema websites
- Displays showtimes for selected dates
- Filters movies by original language availability
- View theaters and their features
- Responsive design for mobile and desktop

## Tech Stack

### Backend

- **Python** with FastAPI for the API
- **MongoDB** for database storage
- **BeautifulSoup/Selenium** for web scraping

### Frontend

- **Next.js** with React for the UI
- **TypeScript** for type safety
- **Tailwind CSS** for styling

## Project Structure

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
│   └── styles/         # CSS styles
```

## Configuring Cinema Website Scrapers

To add new cinema websites for scraping, follow these steps:

1. Create a new scraper class in `backend/scraper/` by extending the `BaseScraper` class
2. Implement the `get_movies_for_date` method for your specific cinema website
3. Add your new scraper to the `scrapers` list in the `ScraperService` class

Example for adding a new scraper:

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

The current implementation includes example scrapers for:
- Yelmo Cinemas (https://www.yelmocines.es)
- Cinessa Cinemas (https://www.cinessa.com)

You can trigger the scraping process manually via the API endpoints:
- `/scrape/now` - Scrape movies for today
- `/scrape/dates?days=7` - Scrape movies for the next 7 days

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js 14+
- MongoDB

### Backend Setup

1. Create a virtual environment (if not already created):

```bash
python -m venv movieobserver-env
```

2. Activate the virtual environment:

```bash
# Windows
movieobserver-env\Scripts\Activate.ps1

# macOS/Linux
source movieobserver-env/bin/activate
```

3. Navigate to the backend directory:

```bash
cd MovieObserver/backend
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file based on `.env.example`:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

6. Start MongoDB (install if not already installed):

```bash
# Install MongoDB Community Edition from:
# https://www.mongodb.com/try/download/community
```

7. Start the API server:

```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. Navigate to the frontend directory:

```bash
cd MovieObserver/frontend
```

2. Install dependencies:

```bash
npm install
```

3. Start the development server:

```bash
npm run dev
```

4. Visit `http://localhost:3000` to view the app

### Running Both Together

1. Open two terminal windows/tabs
2. In the first terminal:
   - Activate the virtual environment
   - Start the backend server
3. In the second terminal:
   - Start the frontend server
   
This way, you can see both frontend and backend logs separately.

## Deployment

### Backend Deployment

- Deploy the FastAPI application using a process manager like Gunicorn
- Set up a reverse proxy like Nginx
- Configure environment variables

### Frontend Deployment

- Build the Next.js app with `npm run build`
- Deploy using Vercel, Netlify, or any other Next.js-compatible hosting

## Legal Considerations

Before deploying this application, ensure you have reviewed the Terms of Service of the websites you're scraping. Web scraping may not be allowed by some websites, and legal restrictions may apply.

## License

[MIT License](LICENSE)
