import re
import time
from bs4 import BeautifulSoup, ResultSet
from bs4.element import Tag
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import utils
from scrapers.base_scraper import BaseScraper
from tyre import Tyre

class DexelScraper(BaseScraper):
    """Scraper for Dexel tyres website"""
    def __init__(self, tyre_width: int, aspect_ratio: int, rim_diameter: int) -> None:
        super().__init__(tyre_width, aspect_ratio, rim_diameter)

    def get_url(self) -> str:
        return "https://www.dexel.co.uk"

    def get_request_url(self, url: str, *extras) -> str:
        return ""

    def load_webdriver(self) -> WebDriver:
        """
        Loads the webdriver with options enabled to try and minimise being detected as a bot.

        Returns:
            WebDriver: The WebDriver object for accessing the webpage.
        """
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...')
        driver = webdriver.Chrome(options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver.get(self.get_url())

        return driver

    @staticmethod
    def scroll_into_view(driver: WebDriver, element: WebElement) -> None:
        """
        Sends the JavaScript to scroll the WebElement into view.

        Args:
            driver (WebDriver): WebDriver instance.
            element (WebElement): The WebElement to be scrolled into view.
        """
        driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def navigate_to_results(self, driver: WebDriver) -> bool:
        """
        Step by step clicks and loads of part of the webpage to navigate to where the results will be listed.

        Args:
            driver (WebDriver): The object needed to be able to interact with the loaded webpage.
        Returns:
            bool: True if everything was successful, False if the search criteria wasn't found.
        """
        # Searches for the Search button
        tyre_select_button: WebElement = driver.find_element(By.LINK_TEXT, 'Search by Tyre Size.')
        DexelScraper.scroll_into_view(driver, tyre_select_button) # Scrolls the button into view otherwise an error will occur when simulating the click
        time.sleep(0.5)
        tyre_select_button.click()

        time.sleep(utils.random_number())

        # Wait until the width dropdown is populated
        width_dropdown: WebElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'width_list')))
        select = Select(width_dropdown)
        tyre_widths = [option.text for option in select.options] # Create a list of all the tyre width options

        # If the tyre_width doesn't appear in that list return None
        if str(self.tyre_width) not in tyre_widths:
            return False

        DexelScraper.scroll_into_view(driver, width_dropdown)
        time.sleep(0.5)
        select.select_by_visible_text(str(self.tyre_width))

        # Wait until the profile list exists
        profile_dropdown: WebElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'profile_list')))

        time.sleep(utils.random_number())

        # Check that there's more than one option available
        WebDriverWait(driver, 10).until(lambda dropdown: len(Select(dropdown.find_element(By.CLASS_NAME, 'profile_list')).options) > 1)
        DexelScraper.scroll_into_view(driver, profile_dropdown)
        time.sleep(0.5)
        select = Select(profile_dropdown)
        aspect_ratios = [option.text for option in select.options]

        if str(self.aspect_ratio) not in aspect_ratios:
            return False

        select.select_by_visible_text(str(self.aspect_ratio))

        rim_dropdown: WebElement = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'size_list')))

        time.sleep(utils.random_number())

        WebDriverWait(driver, 10).until(lambda dropdown: len(Select(dropdown.find_element(By.CLASS_NAME, 'size_list')).options) > 1)
        DexelScraper.scroll_into_view(driver, rim_dropdown)
        time.sleep(0.5)
        select = Select(rim_dropdown)
        rim_diameters = [option.text for option in select.options]

        if str(self.rim_diameter) not in rim_diameters:
            return False

        select.select_by_visible_text(str(self.rim_diameter))

        time.sleep(utils.random_number())

        search_button: WebElement = driver.find_element(By.PARTIAL_LINK_TEXT, 'Search')
        DexelScraper.scroll_into_view(driver, search_button)
        time.sleep(0.5)
        search_button.click()

        time.sleep(utils.random_number())

        branch_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Select This Branch']")))
        DexelScraper.scroll_into_view(driver, branch_button)
        time.sleep(0.5)
        branch_button.click()

        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.tkf-product')))

        return True

    def scrape(self) -> list[Tyre]:
        """
        Scrapes the Dexel website.

        Returns:
            list[Tyre]: The list of Tyres scraped.
        """
        driver: WebDriver = self.load_webdriver()
        # Navigates to the results page step by step with random time delay intervals.
        # If None is returned the match was unsuccessful
        if not self.navigate_to_results(driver):
            return []

        next_page_button: WebElement # Holds a reference to the '>' next page button each time a page loads
        tyres: list[Tyre] = []

        while True: # Keeps looping until there is no more '>' next page button.
            soup: BeautifulSoup = BeautifulSoup(driver.page_source, 'lxml')
            divs: ResultSet[Tag] = soup.select('div[class="tkf-product"]') # Each div tag holds 1 tyre product

            for div in divs:
                sku: str | None = None
                load_index: int | None = None
                speed_rating: str | None = None
                db_rating_letter = None # This website doesn't have letter ratings
                brand: str | None = None
                pattern: str | None = None
                price: float | None = None
                wet_grip: str | None = None
                season: str | None = None
                fuel_efficiency: str | None = None
                db_rating_number: int | None = None
                budget = None # This website doesn't list if a tyre is budget
                tyre_type: str | None = None

                tyre_details_div: Tag | None = div.find('p', class_='para-text')
                price_span: Tag | None = div.find('span', id='defaultBuyingOptionPrice')

                if price_span:
                    price_temp: str | None = re.sub(r'\s+', '', price_span.get_text(strip=True)[1:])
                    price = float(price_temp) if price_temp else None

                fuel_efficiency_div: Tag | None = div.find('div', class_=re.compile('^tyre_info_model fuel'))

                if fuel_efficiency_div:
                    fuel_efficiency = fuel_efficiency_div.get_text(strip=True).upper()

                wet_grip_div: Tag | None = div.find('div', class_=re.compile('^tyre_info_model grip'))

                if wet_grip_div:
                    wet_grip = wet_grip_div.get_text(strip=True).upper()

                db_rating_number_div: Tag | None = div.find('div', class_='exterior-noice')

                if db_rating_number_div:
                    db_rating_number = int(db_rating_number_div.get_text(strip=True))

                tyre_icons_div: Tag | None = div.find('div', class_='tyre-icons')

                if tyre_icons_div:
                    weather_icon_tag: Tag | None = tyre_icons_div.find('i', class_=re.compile('^icon-'))

                    if weather_icon_tag:
                        weather: str | None = weather_icon_tag.get('title')

                        if weather:
                            season = weather.capitalize()

                tyre_icons_vehicle_div: Tag | None = div.find('div', class_=re.compile('^tyre-icons vehicle-types'))

                if tyre_icons_vehicle_div:
                    vehicle_icon_tag: Tag | None = tyre_icons_vehicle_div.find('i', class_=re.compile('^icon-'))

                    if vehicle_icon_tag:
                        vehicle_type: str | None = vehicle_icon_tag.get('title')

                        if vehicle_type:
                            tyre_type = vehicle_type.capitalize()

                ev_button: Tag | None = div.find('button', title='Electric Vehicle')
                electric: bool = ev_button != None

                if tyre_details_div:
                    tyre_speed_details: str | None = tyre_details_div.get_text(strip=True).split()[1]
                    match = re.search(r'\d+[A-Z]', tyre_speed_details) # Removes any garbage around the load index and speed rating

                    if match:
                        tyre_speed_details = match.group()
                        load_index = int(tyre_speed_details[:-1])
                        speed_rating = tyre_speed_details[-1:].upper()

                form: Tag | None = div.find('form', class_='book_tyre')

                if form:
                    sku = form.find('input', {'name': 'prodCode'}).get('value').strip()
                    brand = form.find('input', {'name': 'brand'}).get('value').strip().title()
                    pattern = form.find('input', {'name': 'pattern'}).get('value').strip()

                tyres.append(
                    Tyre(
                        sku=sku,
                        brand=brand,
                        pattern=pattern,
                        tyre_width=self.tyre_width,
                        aspect_ratio=self.aspect_ratio,
                        rim_diameter=self.rim_diameter,
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

            try:
                # At the bottom of the search results page, as long as there's a '>' button it means there's more pages to load
                next_page_button = driver.find_element(By.LINK_TEXT, '>')
                DexelScraper.scroll_into_view(driver, next_page_button)
                time.sleep(0.5)
                next_page_button.click() # Click the '>' button and wait to see if there's another one, if not break out and finish
                WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.LINK_TEXT, '>')))
                time.sleep(utils.random_number())
            except NoSuchElementException:
                break # Breaks out of the while loop

        driver.close()

        return tyres