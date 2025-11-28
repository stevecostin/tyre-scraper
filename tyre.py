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
                 fuel_efficiency: str = "",
                 budget: bool = False,
                 electric: bool = False,
                 tyre_type: str = "Car"
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
        self.budget = budget
        self.electric = electric
        self.tyre_type = tyre_type

    def __repr__(self) -> str:
        return (
            f"Tyre("
            f"brand='{self.brand}', "
            f"tyre_width={self.tyre_width}, "
            f"aspect_ratio={self.aspect_ratio}, "
            f"rim_diameter={self.rim_diameter}, "
            f"load_index={self.load_index}, "
            f"speed_rating='{self.speed_rating}', "
            f"pattern='{self.pattern}', "
            f"price={self.get_price()}, "
            f"wet_grip='{self.wet_grip}', "
            f"season='{self.season}', "
            f"fuel_efficiency='{self.fuel_efficiency}', "
            f"budget={self.budget}, "
            f"electric={self.electric}, "
            f"tyre_type='{self.tyre_type}'"
            f")"
        )

    def __str__(self):
        return (
            f"{self.brand},"
            f"{self.tyre_width},"
            f"{self.aspect_ratio},"
            f"{self.rim_diameter},"
            f"{self.load_index},"
            f"{self.speed_rating},"
            f"{self.pattern},"
            f"{self.get_price()},"
            f"{self.wet_grip},"
            f"{self.season},"
            f"{self.fuel_efficiency},"
            f"{self.budget},"
            f"{self.electric},"
            f"{self.tyre_type},"
        )

    def get_price(self) -> float:
        """Returns the price of the tyre as a decimal"""
        return self.price / 100
    
    def get_speed_as_str(self) -> str:
        """Returns the load index and speed rating (e.g., '91V')"""
        return f"{self.load_index}{self.speed_rating}"