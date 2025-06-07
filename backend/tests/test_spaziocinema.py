import asyncio
import json
from datetime import datetime
from scraper.spaziocinema_scraper import SpaziocinemaInfoScraper


async def test_spaziocinema():
    """
    Test function to verify the SpaziocinemaInfo scraper works
    """
    print("Testing SpaziocinemaInfo scraper...")

    # Create an instance of the scraper
    scraper = SpaziocinemaInfoScraper()

    # Get today's date in the required format
    today = datetime.now().strftime("%Y-%m-%d")

    # Try scraping movies for today
    movies = scraper.get_movies_for_date(today)

    # Print the results
    print(f"Found {len(movies)} movies for today ({today}):")
    for i, movie in enumerate(movies):
        print(
            f"\n{i+1}. {movie.get('title')} ({movie.get('original_title', 'N/A')})")
        print(f"   Showtimes: {len(movie.get('showtimes', []))}")
        for showtime in movie.get('showtimes', []):
            print(
                f"   - {showtime.get('time')}: {'Original language' if showtime.get('is_original_language') else 'Dubbed'}")

    # Save results to a JSON file for inspection
    with open("spaziocinema_test_results.json", "w", encoding="utf-8") as f:
        json.dump(movies, f, ensure_ascii=False, indent=2)

    print("\nComplete results saved to spaziocinema_test_results.json")

if __name__ == "__main__":
    asyncio.run(test_spaziocinema())
