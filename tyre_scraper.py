from time import time
from scrapers import NationalScraper

class TyreScraper:
    pass

def main() -> None:
    print("Welcome to the tyre scraper.")
    print("Scraping will now begin...\n")

    national_scraper = NationalScraper("https://national.co.uk", 205, 55, 16)

    print(f"Scraping {national_scraper.url} for tyres with specs {national_scraper.tyre_width}/{national_scraper.aspect_ratio}/{national_scraper.rim_diameter}.")
    print("Please wait...\n")

    start_time = time()

    national_tyres = national_scraper.scrape()

    print(f"Scraping completed in {(time() - start_time):.2f} seconds.")

if __name__ == "__main__":
    main()