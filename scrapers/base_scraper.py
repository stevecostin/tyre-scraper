from abc import ABC, abstractmethod
from tyre import Tyre

class BaseScraper(ABC):
    def __init__(self, url: str, tyre_width: int, aspect_ratio: int, rim_diameter: int) -> None:
        self.url = url
        self.tyre_width = tyre_width
        self.aspect_ratio = aspect_ratio
        self.rim_diameter = rim_diameter

    @abstractmethod
    def get_request_url(self) -> str:
        """Returns the url needed to query the website"""
        pass

    @abstractmethod
    def scrape(self) -> list[Tyre]:
        """Starts the scraping for the particular Scraper"""
        pass