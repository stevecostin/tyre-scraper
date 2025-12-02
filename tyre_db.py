import sqlite3
from sqlite3 import Connection, Cursor
from tyre import Tyre

class TyreDB:
    """Database handler for tyre scraping"""
    def __init__(self):
        """Initialize database connection and create the tables."""
        self.conn: Connection = sqlite3.connect(TyreDB.get_db_name())
        self.cursor: Cursor = self.conn.cursor()
        self._create_tables()

    @staticmethod
    def get_db_name():
        return "tyres.db"

    def __enter__(self) -> "TyreDB":
        """Context manager entry point"""
        return self

    def __exit__(self, exception_type, exception_val, exception_tb) -> bool:
        """Context manager exit point - ensures connection is closed"""
        if exception_type is not None:
            # If an exception occurred, rollback any uncommitted changes
            self.conn.rollback()
        else:
            # Otherwise commit any pending changes
            self.conn.commit()

        self.conn.close()

        return False

    def _create_tables(self):
        """Create the schema if it doesn't already exist"""
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS retailer
                (
                    retailer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                    retailer_name TEXT NOT NULL UNIQUE
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS brand (
                    brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand_name TEXT NOT NULL UNIQUE
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS season (
                    season_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                    season_name TEXT NOT NULL UNIQUE
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS vehicle_tyre_type (
                    vehicle_tyre_type_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                    vehicle_tyre_type_name TEXT NOT NULL UNIQUE
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS pattern (
                    pattern_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                    pattern_name TEXT NOT NULL UNIQUE,
                    brand_id INTEGER NOT NULL,
                    season_id INTEGER NOT NULL,
                    FOREIGN KEY (brand_id) REFERENCES brand(brand_id),
                    FOREIGN KEY (season_id) REFERENCES season(season_id),
                    UNIQUE(pattern_name, brand_id)
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS tyre (
                    sku         TEXT NOT NULL,
                    retailer_id INTEGER NOT NULL,
                    width INTEGER NOT NULL,
                    aspect_ratio INTEGER NOT NULL,
                    rim_diameter INTEGER NOT NULL,
                    load_index INTEGER,
                    speed_rating TEXT,
                    pattern_id INTEGER,
                    price INTEGER,
                    wet_grip TEXT,
                    fuel_efficiency TEXT,
                    db_rating_number INTEGER,
                    db_rating_letter TEXT,
                    budget INTEGER,
                    electric INTEGER,
                    vehicle_tyre_type_id INTEGER,
                    PRIMARY KEY (sku, retailer_id),
                    FOREIGN KEY (retailer_id) REFERENCES retailer(retailer_id),
                    FOREIGN KEY (pattern_id) REFERENCES pattern(pattern_id),
                    FOREIGN KEY (vehicle_tyre_type_id) REFERENCES vehicle_tyre_type(vehicle_tyre_type_id)
                )
            ''')

            self.conn.commit()
        except Exception as e:
            print(f"There was a problem creating the database schema: {e}")
            self.conn.rollback()

        # Create all the season tyres
        self.get_or_create_season("Winter")
        self.get_or_create_season("Summer")
        self.get_or_create_season("All Season")

        # Create known vehicle tyre types
        self.get_or_create_vehicle_tyre_type("Car")

    def get_or_create_retailer(self, retailer_name: str) -> int:
        """
        Gets/creates the retailer_id for a retailer.

        Args:
            retailer_name (str): The retailer name to be retrieved or created.

        Returns:
            int: The retailer_id retrieved or created.
        """
        self.cursor.execute(
            "SELECT retailer_id FROM retailer WHERE retailer_name = ?", (retailer_name,)
        )

        result: tuple = self.cursor.fetchone()

        if result:
            return result[0]

        self.cursor.execute(
            "INSERT INTO retailer (retailer_name) VALUES (?)", (retailer_name,)
        )

        self.conn.commit()

        return self.cursor.lastrowid

    def get_or_create_brand(self, brand_name: str) -> int:
        """
        Gets/creates the brand_id for a brand name.

        Args:
            brand_name (str): The brand name to be retrieved or created.

        Returns:
            int: The brand_id retrieved or created.
        """
        self.cursor.execute(
            "SELECT brand_id FROM brand WHERE brand_name = ?", (brand_name.title(),)
        )

        result: tuple = self.cursor.fetchone()

        if result:
            return result[0]

        self.cursor.execute(
            "INSERT INTO brand (brand_name) VALUES (?)", (brand_name.title(),)
        )

        self.conn.commit()

        return self.cursor.lastrowid

    def get_or_create_season(self, season_name: str | None) -> int:
        """
        Gets/creates the season_id for a season name.
        Season names are normalized to title case for consistency.

        Args:
            season_name (str | None): The season name to be retrieved or created.

        Returns:
            int: The season_id retrieved or created.
        """
        # Normalize to title case for consistency, default to "None" if empty
        normalized_name = season_name.title() if season_name else "None"

        self.cursor.execute(
            "SELECT season_id FROM season WHERE season_name = ?", (normalized_name,)
        )

        result: tuple = self.cursor.fetchone()

        if result:
            return result[0]

        self.cursor.execute(
            "INSERT INTO season (season_name) VALUES (?)", (normalized_name,)
        )

        self.conn.commit()

        return self.cursor.lastrowid

    def get_or_create_vehicle_tyre_type(self, vehicle_tyre_type_name: str) -> int:
        """
        Gets/creates the vehicle_tyre_type_id for a vehicle tyre type name.

        Args:
            vehicle_tyre_type_name (str): The vehicle tyre type name to be retrieved or created.

        Returns:
            int: The vehicle_tyre_type_id retrieved or created.
        """
        self.cursor.execute(
            "SELECT vehicle_tyre_type_id FROM vehicle_tyre_type WHERE vehicle_tyre_type_name = ?", (vehicle_tyre_type_name.title(),)
        )

        result: tuple = self.cursor.fetchone()

        if result:
            return result[0]

        self.cursor.execute(
            "INSERT INTO vehicle_tyre_type (vehicle_tyre_type_name) VALUES (?)", (vehicle_tyre_type_name.title(),)
        )

        self.conn.commit()

        return self.cursor.lastrowid

    def get_or_create_pattern(self, pattern_name: str, brand_id: int, season_id: int) -> int:
        """
        Gets/creates the pattern_id for a tyre pattern.

        Args:
            pattern_name (str): The pattern name to be retrieved or created.
            brand_id (int): The brand id of the pattern.
            season_id (int): The season id of the pattern.

        Returns:
            int: The pattern_id retrieved or created.
        """
        self.cursor.execute(
            "SELECT pattern_id FROM pattern WHERE pattern_name = ? AND brand_id = ?", (pattern_name, brand_id)
        )

        result: tuple = self.cursor.fetchone()

        if result:
            return result[0]

        self.cursor.execute(
            "INSERT INTO pattern (pattern_name, brand_id, season_id) VALUES (?, ?, ?)", (pattern_name, brand_id, season_id)
        )

        self.conn.commit()

        return self.cursor.lastrowid

    def add_tyre(self, retailer_id: int, tyre: Tyre) -> int:
        """
        Adds a tyre to the database for a specific retailer.
        If the tyre already exists at a certain retailer the tyres information gets updated with any changes.

        Args:
            retailer_id (int): The ID of the retailer being added/changed.
            tyre (Tyre): The tyre to be added/changed.

        Returns:
            int: The tyre_id added.
        """
        brand_id: int = self.get_or_create_brand(tyre.brand)
        season_id: int = self.get_or_create_season(tyre.season)
        pattern_id: int = self.get_or_create_pattern(tyre.pattern, brand_id, season_id)
        vehicle_tyre_type_id: int = self.get_or_create_vehicle_tyre_type(tyre.tyre_type)

        self.cursor.execute('''
            INSERT INTO tyre (
                sku, retailer_id, width, aspect_ratio, rim_diameter, load_index, speed_rating, pattern_id,
                price, wet_grip, fuel_efficiency, db_rating_number, db_rating_letter,
                budget, electric, vehicle_tyre_type_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(sku, retailer_id) DO UPDATE SET
                width = excluded.width,
                aspect_ratio = excluded.aspect_ratio,
                rim_diameter = excluded.rim_diameter,
                load_index = excluded.load_index,
                speed_rating = excluded.speed_rating,
                pattern_id = excluded.pattern_id,
                price = excluded.price,
                wet_grip = excluded.wet_grip,
                fuel_efficiency = excluded.fuel_efficiency,
                db_rating_number = excluded.db_rating_number,
                db_rating_letter = excluded.db_rating_letter,
                budget = excluded.budget,
                electric = excluded.electric,
                vehicle_tyre_type_id = excluded.vehicle_tyre_type_id
            ''', (
                tyre.sku, retailer_id, tyre.tyre_width, tyre.aspect_ratio, tyre.rim_diameter, tyre.load_index, tyre.speed_rating, pattern_id, tyre.price_pence, tyre.wet_grip, tyre.fuel_efficiency,
                tyre.db_rating_number, tyre.db_rating_letter, tyre.budget, tyre.electric, vehicle_tyre_type_id
            )
        )

        self.conn.commit()

        return self.cursor.lastrowid