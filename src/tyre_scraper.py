import time
import requests
from retailer import Retailer
from src.scrapers import BaseScraper, NationalScraper
from tyre import Tyre
from tyre_db import TyreDB

def start_scrap(scrapers: list[BaseScraper]) -> float:
    """
    Sequentially scrapes each scrapers website.
    Writes the gathered data to a CSV file and a database.

    Args:
        scrapers (list[BaseScraper]): The scrapers that will be scraped.

    Returns:
        float: The total time it took to scrap all the websites.
    """
    total_time_scraping: float = 0
    retailers: list[Retailer] = []

    SLEEP_COUNT: int = 5  # Seconds between each scrape

    # Initialise the database and create the tables if needed
    db = TyreDB()

    for scrape_count, scraper in enumerate(scrapers, start=1):
        print(f"Scraping {scraper.domain} for tyres with specs {scraper.get_basic_tyre_details()}.")

        start_time = time.time()

        try:
            scrape_data: list[Tyre] = scraper.scrape()
            retailer = Retailer(scraper.domain, scrape_data) # Stores the scrape data and the website in a single object
            total_results: int = len(scrape_data)
            time_for_scrape: float = time.time() - start_time
            total_time_scraping += round(time_for_scrape, 2)

            retailers.append(retailer) # Adds the retailer object to the existing list of retailers

            print(f"Scraping completed in {time_for_scrape:.2f} {get_seconds_formatted_str(time_for_scrape)} and found {total_results} result{'s' if total_results > 1 or total_results == 0 else ''}.")
        except requests.RequestException as e:
            print(f"There was a problem accessing the {scraper.domain} website: {e}")

        # Sleeps before starting the next scrape
        if scrape_count < len(scrapers):
            print(f"\nWaiting {SLEEP_COUNT} seconds before the next scrape...\n")
            time.sleep(SLEEP_COUNT)

    print(f"\nWriting CSV data to '{BaseScraper.get_csv_filename()}' and database data to '{TyreDB.get_db_name()}'...")

    # After all scraping has completed the data is saved to a CSV and the database
    BaseScraper.write_to_csv_file(retailers)
    write_scrapes_to_db(db, retailers)

    print("Complete.\n")

    return total_time_scraping

def get_seconds_formatted_str(seconds: float) -> str:
    """
    Pluralises the word "second" if the "seconds" argument is != 1.

    Args:
        seconds (float): The number to evaluate.

    Returns:
        Pluralised or non-pluralised word "second".
    """
    return "second" if seconds == 1 else "seconds"

def write_scrapes_to_db(db: TyreDB, retailers: list[Retailer]) -> None:
    """
    Writes the list of retailers and all associated tyres of that retailer to the database.

    Args:
        db (TyreDB): The instance of the database object.
        retailers (list[Retailer]): The retailer objects to write to the database.
    """
    for retailer in retailers:
        tyres: list[Tyre] = retailer.tyres
        retailer_id: int = db.get_or_create_retailer(retailer.retailer)

        for tyre in tyres:
            db.add_tyre(retailer_id, tyre)

def main() -> None:
    print("Welcome to the tyre scraper.")
    print("Scraping will now begin...\n")

    scrapers: list[BaseScraper] = [
        NationalScraper(205, 55, 16),
        NationalScraper(225, 50, 16),
        NationalScraper(185, 16, 14)
    ]

    total_time_scraping: float = round(start_scrap(scrapers), 2)

    print(f"Scraping completed in {total_time_scraping:.2f} {get_seconds_formatted_str(total_time_scraping)}.")

if __name__ == "__main__":
    main()