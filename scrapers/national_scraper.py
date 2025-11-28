import requests
from bs4 import BeautifulSoup
import re
from bs4.element import Tag

from scrapers.base_scraper import BaseScraper
from tyre import Tyre

class NationalScraper(BaseScraper):
    def __init__(self, url: str, tyre_width: int, aspect_ratio: int, rim_diameter: int) -> None:
        super().__init__(url, tyre_width, aspect_ratio, rim_diameter)

    def get_request_url(self) -> str:
        return f"{self.url}/tyres-search/{self.tyre_width}-{self.aspect_ratio}-{self.rim_diameter}?pc=DN67RL"
    
    def scrape(self) -> list[Tyre]:
        tyres: list[Tyre] = []

        try:
            response = requests.get(self.get_request_url(), timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            print(f"Error fetching {self.url}: {e}")

            return []

        divs = soup.select('div[id^="PageContent_ucTyreResults_rptTyres_divTyre_"]')

        for div in divs:
            brand: str | None = div.get('data-brand')
            brand = brand.title() if brand else None

            price_temp: str | None = div.get('data-price')

            try:
                price: float | None = float(price_temp) if price_temp else None
            except ValueError:
                price = None

            wet_grip: str | None = div.get('data-grip')
            wet_grip = wet_grip[-1] if wet_grip else None

            season: str | None = div.get('data-tyre-season')

            fuel_efficiency: str | None = div.get('data-fuel')
            fuel_efficiency = fuel_efficiency[-1] if fuel_efficiency else None

            budget_tmp: str | None = div.get('data-budget')
            budget: bool | None = budget_tmp.lower() == 'true' if budget_tmp else None

            electric_tmp: str | None = div.get('data-electric')
            electric: bool | None = electric_tmp.lower() == 'yes' if electric_tmp else None

            tyre_type: str | None = div.get('data-tyre-type')

            pattern_temp: Tag | None = div.find('a', id=re.compile('^PageContent_ucTyreResults_rptTyres_hypPattern_'))
            pattern: str | None = pattern_temp.get_text() if pattern_temp else None

            details_div: Tag | None = div.find('div', class_='details')

            tyre_specs_overall: list | None = None
            tyre_width: int | None = None
            aspect_ratio: int | None = None

            try:
                details_div_p: Tag | None = details_div.find('p')
                details_div_p_p: Tag | None = details_div_p.find_next_sibling('p') if details_div_p else None

                if details_div_p_p:
                    tyre_specs_text: str = details_div_p_p.get_text(strip=True)
                    if tyre_specs_text:
                        tyre_specs_overall = tyre_specs_text.split()
                        if tyre_specs_overall:
                            tyre_width_aspect: list = tyre_specs_overall[0].split('/')

                            tyre_width = int(tyre_width_aspect[0])
                            aspect_ratio = int(tyre_width_aspect[1])
            except (AttributeError, IndexError, ValueError):
                pass

            rim_diameter: int | None = None
            load_index: int | None = None
            speed_rating: str | None = None

            try:
                rim_diameter = int(tyre_specs_overall[1][1:])
                load_index = int(tyre_specs_overall[2][:-1])
                speed_rating = tyre_specs_overall[2][-1]
            except (IndexError, ValueError):
                pass

            tyres.append(Tyre(brand, pattern, tyre_width, aspect_ratio, rim_diameter, load_index, speed_rating, price, wet_grip, season, fuel_efficiency, budget, electric, tyre_type))

        return tyres