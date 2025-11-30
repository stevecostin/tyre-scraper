from abc import ABC, abstractmethod
from src.retailer import Retailer
from src.tyre import Tyre

class BaseScraper(ABC):
    def __init__(self, tyre_width: int, aspect_ratio: int, rim_diameter: int) -> None:
        """
        Creates a new BaseScraper with the basic information that will be searched when scraping

        Args:
            tyre_width (int): The width of the tyre being scraped for.
            aspect_ratio (int): The aspect ratio of the tyre being scraped for.
            rim_diameter (int): The diameter of the tyre being scraped for.
        """
        self.tyre_width = tyre_width
        self.aspect_ratio = aspect_ratio
        self.rim_diameter = rim_diameter
        self.domain = self.get_url().replace('https://', '').replace('http://', '').split('/')[0] # Removes any http:// or https:// from the beginning of the URL

    @abstractmethod
    def get_url(self) -> str:
        """
        Returns:
            str: The URL name of the website to be scraped (e.g. https://national.co.uk, etc.).
        """
        pass

    @abstractmethod
    def get_request_url(self, url: str) -> str:
        """
        Args:
            url (str): The domain name of the website that will be scraped
        Returns:
            str: The exact URL needed to access the relevant tyre information on the website.
        """
        pass

    @abstractmethod
    def scrape(self) -> list[Tyre]:
        """
        Starts the scraping process on the URL provided by the get_request_url() method.

        Returns:
            list[Tyre]: The list of Tyres that have been scraped from the website.

        Raises:
            RequestException: There was a problem with the connection to the website
        """
        pass

    @staticmethod
    def get_csv_filename() -> str:
        """
        Returns:
            str: The name of the CSV file that will be used for writing data to (e.g. [domain].csv).
        """
        return "tyre_scrape.csv"

    @staticmethod
    def write_to_csv_file(retailers: list[Retailer]) -> None:
        """
        Writes each Tyre entry to a CSV file named after the return of get_csv_filename().
        If the file exists the file will be overwritten.

        Args:
            retailers (list[Retailer]): The list of retailer objects that were scraped
        """
        with open(BaseScraper.get_csv_filename(), "w", encoding='utf-8') as f:
            f.write(f"retailer,{Tyre.get_tyre_attribute_names()}\n")

            for retailer in retailers:
                tyres: list[Tyre] = retailer.tyres

                for tyre in tyres:
                    f.write(f"{retailer.retailer},{tyre}\n")

    def get_basic_tyre_details(self) -> str:
        """
        Returns:
            str: The tyre width, aspect ratio and rim diameter in a friendly format (e.g. 205/55/R16).
        """
        return f"{self.tyre_width}/{self.aspect_ratio}/R{self.rim_diameter}"