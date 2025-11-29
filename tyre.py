class Tyre:
    def __init__(self,
                 brand: str | None,
                 pattern: str | None,
                 tyre_width: int | None,
                 aspect_ratio: int | None,
                 rim_diameter: int | None,
                 load_index: int | None,
                 speed_rating: str | None,
                 price: float | None,
                 wet_grip: str | None = None,
                 season: str | None = None,
                 fuel_efficiency: str | None = None,
                 budget: bool | None = None,
                 electric: bool | None = None,
                 tyre_type: str | None = None
    ) -> None:
        """
        Tyre that stores all the relevant specs relating to a tyre.

        Args:
            brand (str | None): Manufacturer of the tyre (e.g. Bridgestone, Goodyear, etc.).
            pattern (str | None): The tread name of the tyre (e.g. Turanza T001, Ecopia EP500, etc.).
            tyre_width (int | None): The width of the tyre (e.g. 205).
            aspect_ratio (int | None): The aspect ratio of the tyre (e.g. 55).
            rim_diameter (int | None): The diameter of the tyre in inches (e.g. 16).
            load_index (int | None): The load index of the tyre (e.g. 91).
            speed_rating (str | None): The speed rating of the tyre (e.g. V).
            price (float | None): The price of one tyre.
            wet_grip (str | None): The wet grip rating (e.g. A, B, C).
            season (str | None): The season the tyre is made for (e.g. Summer, Winter, All Seasons).
            fuel_efficiency (str | None): The fuel efficiency rating (e.g. A, B, C).
            budget (bool | None): Whether the tyre is a budget tyre.
            electric (bool | None): Whether the tyre was made for an electric car.
            tyre_type (str | None): The type of vehicle the tyre is for (e.g. Car).
        """
        self.brand = brand
        self.pattern = pattern
        self.tyre_width = tyre_width
        self.aspect_ratio = aspect_ratio
        self.rim_diameter = rim_diameter
        self.price = int(price * 100) if price is not None else None # Converts decimal into a whole number if the price isn't None
        self.load_index = load_index
        self.speed_rating = speed_rating
        self.wet_grip = wet_grip
        self.season = season
        self.fuel_efficiency = fuel_efficiency
        self.budget = budget
        self.electric = electric
        self.tyre_type = tyre_type

    def __repr__(self) -> str:
        """
        Returns a string representation of the Tyre object in a clearly defined way.

        Returns:
            str: An easy-to-read string formatted like Tyre(brand='brand_name',tyre_width=205,aspect_ratio=55,rim_diameter=16) etc.
        """
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

    def __str__(self) -> str:
        """
        A string representation of the Tyre object ready to be written to a CSV file.

        Returns:
            str: A string in CSV format containing all the properties of the Tyre. e.g. goodyear,205,55,16,91,V etc.
        """
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
            f"{self.tyre_type}"
        )

    @staticmethod
    def get_tyre_attribute_names() -> str:
        """
        A comma separated list of the header names for when writing to a CSV file

        Returns:
            str: The header names separated by commas
        """
        return (
            "brand,"
            "tyre_width,"
            "aspect_ratio,"
            "rim_diameter,"
            "load_index,"
            "speed_rating,"
            "pattern,"
            "price,"
            "wet_grip,"
            "season,"
            "fuel_efficiency,"
            "budget,"
            "electric,"
            "tyre_type"
        )

    def get_price(self) -> float | None:
        """
        Returns:
            float | None: The price of the tyre.
        """
        return self.price / 100 if self.price is not None else None