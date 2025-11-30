import os
from abc import ABC, abstractmethod
from tyre import Tyre

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

    def get_basic_tyre_details(self) -> str:
        """
        Returns:
            str: The tyre width, aspect ratio and rim diameter in a friendly format (e.g. 205/55/R16).
        """
        return f"{self.tyre_width}/{self.aspect_ratio}/R{self.rim_diameter}"

    def get_csv_filename(self) -> str:
        """
        Returns:
            str: The name of the CSV file that will be used for writing data to (e.g. [domain].csv).
        """
        return f"{self.domain}.csv"

    def write_to_csv_file(self, tyres: list[Tyre]) -> None:
        """
        Writes each Tyre entry to a CSV file named after the URL (e.g. www.website.com.csv).
        If the file doesn't exist or is empty when it's opened for writing it will populate the first line with the csv headers, otherwise it will just write the tyre data.

        Args:
            tyres (list[Tyre]): The list of Tyres to be written to the file.
        """
        filename: str = self.get_csv_filename()
        file_exists: bool = os.path.exists(filename) and os.path.getsize(filename) > 0

        with open(filename, "a", encoding='utf-8') as f:
            if not file_exists:
                f.write(Tyre.get_tyre_attribute_names() + '\n')

            for tyre in tyres:
                f.write(str(tyre) + '\n')