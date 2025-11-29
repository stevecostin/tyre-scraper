from abc import ABC, abstractmethod
from tyre import Tyre

class BaseScraper(ABC):
    def __init__(self, url: str, tyre_width: int, aspect_ratio: int, rim_diameter: int) -> None:
        """
        Creates a new BaseScraper with essentials needed to access the website being scraped.

        Args:
            url (str): The simple URL of the website to be scraped (e.g. www.national.co.uk, etc.).
            tyre_width (int): The width of the tyre being scraped for.
            aspect_ratio (int): The aspect ratio of the tyre being scraped for.
            rim_diameter (int): The diameter of the tyre being scraped for.
        """
        self.url = url
        self.tyre_width = tyre_width
        self.aspect_ratio = aspect_ratio
        self.rim_diameter = rim_diameter

    def write_to_file(self, tyres: list[Tyre]) -> None:
        """
        Writes each Tyre entry to a CSV file named after the URL and basic tyre specs. e.g. www.website.com-205-55-16.csv.

        Args:
            tyres (list[Tyre]): The list of Tyres to be written to the file.
        """
        domain = self.url.replace('https://', '').replace('http://', '').split('/')[0] # Removes any http:// or https:// from the beginning of the URL
        filename = f"{domain}-{self.tyre_width}-{self.aspect_ratio}-{self.rim_diameter}.csv"

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(Tyre.get_tyre_attribute_names() + '\n')

            for tyre in tyres:
                f.write(str(tyre) + '\n')

    @abstractmethod
    def get_request_url(self) -> str:
        """
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
        """
        pass