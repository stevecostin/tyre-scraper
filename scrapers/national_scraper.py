import requests
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper
from tyre import Tyre

class NationalScraper(BaseScraper):
    def __init__(self, url: str, tyre_width: int, aspect_ratio: int, rim_diameter: int) -> None:
        super().__init__(url, tyre_width, aspect_ratio, rim_diameter)

    def get_request_url(self) -> str:
        return f"{self.url}/tyres-search/{self.tyre_width}-{self.aspect_ratio}-{self.rim_diameter}?pc=DN67RL"
    
    def scrape(self) -> list[Tyre]:
        tyres: list[Tyre] = []

        soup = BeautifulSoup(requests.get(self.get_request_url()).content, 'lxml')

        

        return tyres