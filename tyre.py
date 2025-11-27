from decimal import Decimal

class Tyre:
    def __init__(self,
                 brand: str,
                 pattern: str,
                 tyre_width: int,
                 aspect_ratio: int,
                 rim_diameter: int,
                 load_index: int,
                 speed_rating: str,
                 price: float,
                 wet_grip: str = "",
                 season: str = "",
                 fuel_efficiency: str = ""
    ) -> None:
        self.brand = brand
        self.pattern = pattern
        self.tyre_width = tyre_width
        self.aspect_ratio = aspect_ratio
        self.rim_diameter = rim_diameter
        self.price = int(price * 100) # Converts decimal into a whole number
        self.load_index = load_index
        self.speed_rating = speed_rating
        self.wet_grip = wet_grip
        self.season = season
        self.fuel_efficiency = fuel_efficiency

    def get_price(self) -> float:
        return self.price / 100 # Returns the price as a decimal
    
    def get_speed_as_str(self) -> str:
        """Returns the load index and speed rating (e.g., '91V')"""
        return f"{self.load_index}{self.speed_rating}"