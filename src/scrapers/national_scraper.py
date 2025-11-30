import requests
from bs4 import BeautifulSoup
from bs4.element import Tag
import re
from src.scrapers.base_scraper import BaseScraper
from src.tyre import Tyre

class NationalScraper(BaseScraper):
    """Scraper for National tyres website"""
    def __init__(self, tyre_width: int, aspect_ratio: int, rim_diameter: int) -> None:
        super().__init__(tyre_width, aspect_ratio, rim_diameter)

    def get_url(self) -> str:
        return "https://national.co.uk"

    def get_request_url(self, url: str, *extras) -> str:
        return f"{url}/tyres-search/{self.tyre_width}-{self.aspect_ratio}-{self.rim_diameter}?pc=DN67RL"
    
    def scrape(self) -> list[Tyre]:
        tyres: list[Tyre] = []

        try:
            response = requests.get(self.get_request_url(self.get_url()), timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')
        except requests.RequestException as e:
            raise requests.RequestException(e)

        divs = soup.select('div[id^="PageContent_ucTyreResults_rptTyres_divTyre_"]')

        for div in divs:
            # Gets the brand of tyre
            brand: str | None = div.get('data-brand')
            brand = brand.strip().title() if brand else None

            # Gets the current price of a single tyre
            price_temp: str | None = div.get('data-price')
            try:
                price: float | None = float(price_temp.strip()) if price_temp else None
            except ValueError:
                price = None

            # Gets the wet grip rating
            wet_grip: str | None = div.get('data-grip')
            wet_grip = wet_grip[-1].strip() if wet_grip else None

            # Gets the season the tyre should be driven in
            season: str | None = div.get('data-tyre-season')
            season = season.strip() if season else None

            # Gets the fuel efficiency rating
            fuel_efficiency: str | None = div.get('data-fuel')
            fuel_efficiency = fuel_efficiency[-1].strip() if fuel_efficiency else None

            # Gets whether the tyre is a budget tyre or not
            budget_tmp: str | None = div.get('data-budget')
            budget: bool | None = budget_tmp.strip().lower() == 'true' if budget_tmp else None

            # Gets whether the tyre is designed for an EV car
            electric_tmp: str | None = div.get('data-electric')
            electric: bool | None = electric_tmp.strip().lower() == 'yes' if electric_tmp else None

            # Gets the vehicle type the tyre was made for
            tyre_type: str | None = div.get('data-tyre-type')
            tyre_type = tyre_type.strip() if tyre_type else None

            db_rating_number: int | None = None
            db_rating_letter: str | None = None
            sku: str | None = None

            try:
                tyre_result_div: Tag | None = div.find('div', class_='tyreresult')

                if tyre_result_div:
                    button = tyre_result_div.find('button')

                    if button:
                        part_code: str | None = button.get('data-partcode')

                        # Must have a sku, if it doesn't the tyre entry is skipped
                        if part_code:
                            sku = part_code.strip()
                        else:
                            continue

                    # Finds the div with an id that starts with 'PageContent_ucTyreResults_rptTyres_divTyreLabel_'
                    db_div: Tag | None = div.find('div', id=re.compile('^PageContent_ucTyreResults_rptTyres_divTyreLabel_'))

                    if db_div:
                        background_img_css: str | None = db_div.get('style')

                        if background_img_css:
                            # Matches everything inside the brackets of template url('/tyre-eprel-image.ashx?NL=70&NMV=B&RRC=D&WG=A')
                            match = re.search(r"\(([^)]+)\)", background_img_css)

                            if match:
                                image_url = match.group(1)[1:-1] # Removes the first and last quote

                                if image_url:
                                    image_url = image_url[image_url.find('?')+1:] # Gets the query string (e.g. NL=70&NMV=B&RRC=C&WG=B)
                                    amp_1: int = image_url.find('&')
                                    db_rating_number = int(image_url[image_url.find("=")+1:amp_1]) # Extracts the decibel number from between the = and &
                                    amp_2: int = image_url.find('&', amp_1 + 1)
                                    db_rating_letter = image_url[image_url.find("=", amp_1+1)+1:amp_2] # Extracts the decibel letter from the next iteration of = and &
            except (AttributeError, ValueError) as e:
                print(f"Error getting decibel data: {e}")

            # Finds the div with an id that starts with 'PageContent_ucTyreResults_rptTyres_hypPattern_' which is the tyre pattern type
            pattern_temp: Tag | None = div.find('a', id=re.compile('^PageContent_ucTyreResults_rptTyres_hypPattern_'))
            pattern: str | None = pattern_temp.get_text().strip() if pattern_temp else None

            details_div: Tag | None = div.find('div', class_='details')

            tyre_specs_overall: list | None = None
            tyre_width: int | None = None
            aspect_ratio: int | None = None

            try:
                # Drill down 2 <p> tags
                details_div_p: Tag | None = details_div.find('p')
                details_div_p_p: Tag | None = details_div_p.find_next_sibling('p') if details_div_p else None

                if details_div_p_p:
                    tyre_specs_text: str = details_div_p_p.get_text(strip=True)

                    if tyre_specs_text:
                        # Splits out the aspects of the tyre specs (e.g. 205/55)
                        tyre_specs_overall = tyre_specs_text.split()
                        if tyre_specs_overall:
                            tyre_width_aspect: list = tyre_specs_overall[0].split('/')
                            tyre_width = int(tyre_width_aspect[0])
                            aspect_ratio = int(tyre_width_aspect[1])
            except (AttributeError, IndexError, ValueError) as e:
                print(f"Error setting tyre spec data: {e}")

            rim_diameter: int | None = None
            load_index: int | None = None
            speed_rating: str | None = None

            try:
                # Extract out the other parts of the tyre specs
                rim_diameter = int(tyre_specs_overall[1][1:]) # Removes the 'R' from the diameter
                load_index = int(tyre_specs_overall[2][:-1]) # Gets the number from something like '91V'
                speed_rating = tyre_specs_overall[2][-1] # Stores the 'V' part
            except (IndexError, ValueError) as e:
                print(f"Error setting tyre spec data: {e}")

            tyres.append(
                Tyre(
                    sku=sku,
                    brand=brand,
                    pattern=pattern,
                    tyre_width=tyre_width,
                    aspect_ratio=aspect_ratio,
                    rim_diameter=rim_diameter,
                    load_index=load_index,
                    speed_rating=speed_rating,
                    price=price,
                    wet_grip=wet_grip,
                    season=season,
                    fuel_efficiency=fuel_efficiency,
                    db_rating_number=db_rating_number,
                    db_rating_letter=db_rating_letter,
                    budget=budget,
                    electric=electric,
                    tyre_type=tyre_type
                )
            )

        return tyres