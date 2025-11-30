import sqlite3
from sqlite3 import Connection, Cursor

from tyre import Tyre


class TyreDB:
    """Database handler for tyre scraping"""
    def __init__(self):
        """Initialize database connection and create the tables."""
        self.conn: Connection = sqlite3.connect("tyres.db")
        self.cursor: Cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Create the schema if it doesn't already exist"""
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
                tyre_id   INTEGER PRIMARY KEY AUTOINCREMENT,
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
                FOREIGN KEY (pattern_id) REFERENCES pattern(pattern_id),
                FOREIGN KEY (vehicle_tyre_type_id) REFERENCES vehicle_tyre_type(vehicle_tyre_type_id)
            )
        ''')

        # Create all the season tyres
        self.get_or_create_season("Winter")
        self.get_or_create_season("Summer")
        self.get_or_create_season("All Season")

        # Create known vehicle tyre types
        self.get_or_create_vehicle_tyre_type("Car")

        self.conn.commit()

    def get_or_create_brand(self, brand_name: str) -> int:
        """
        Gets/creates the brand_id for a brand name

        Args:
            brand_name (str): The brand name to be retrieved or created

        Returns:
            int: The brand_id retrieved or created
        """
        self.cursor.execute(
            "SELECT brand_id FROM brand WHERE brand_name = ?", (brand_name,)
        )

        result: tuple = self.cursor.fetchone()

        if result:
            return result[0]

        self.cursor.execute(
            "INSERT INTO brand (brand_name) VALUES (?)", (brand_name,)
        )

        self.conn.commit()

        return self.cursor.lastrowid

    def get_or_create_season(self, season_name: str) -> int:
        """
        Gets/creates the season_id for a season name

        Args:
            season_name (str): The season name to be retrieved or created

        Returns:
            int: The season_id retrieved or created
        """
        self.cursor.execute(
            "SELECT season_id FROM season WHERE season_name = ?", (season_name,)
        )

        result: tuple = self.cursor.fetchone()

        if result:
            return result[0]

        self.cursor.execute(
            "INSERT INTO season (season_name) VALUES (?)", (season_name,)
        )

        self.conn.commit()

        return self.cursor.lastrowid

    def get_or_create_vehicle_tyre_type(self, vehicle_tyre_type_name: str) -> int:
        """
        Gets/creates the vehicle_tyre_type_id for a vehicle tyre type name

        Args:
            vehicle_tyre_type_name (str): The vehicle tyre type name to be retrieved or created

        Returns:
            int: The vehicle_tyre_type_id retrieved or created
        """
        self.cursor.execute(
            "SELECT vehicle_tyre_type_id FROM vehicle_tyre_type WHERE vehicle_tyre_type_name = ?", (vehicle_tyre_type_name,)
        )

        result: tuple = self.cursor.fetchone()

        if result:
            return result[0]

        self.cursor.execute(
            "INSERT INTO vehicle_tyre_type (vehicle_tyre_type_name) VALUES (?)", (vehicle_tyre_type_name,)
        )

        self.conn.commit()

        return self.cursor.lastrowid

    def get_or_create_pattern(self, pattern_name: str, brand_id: int, season_id: int) -> int:
        """
        Gets/creates the pattern_id for a tyre pattern

        Args:
            pattern_name (str): The pattern name to be retrieved or created
            brand_id (int): The brand id of the pattern
            season_id (int): The season id of the pattern

        Returns:
            int: The pattern_id retrieved or created
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

    def add_tyre(self, tyre: Tyre) -> int:
        """
        Adds a tyre to the database

        Args:
            tyre (Tyre): The tyre to be added

        Returns:
            int: The tyre_id added
        """
        brand_id: int = self.get_or_create_brand(tyre.brand)
        season_id: int = self.get_or_create_season(tyre.season)
        pattern_id: int = self.get_or_create_pattern(tyre.pattern, brand_id, season_id)

        self.cursor.execute('''
            INSERT INTO tyre (
                width, aspect_ratio, rim_diameter, load_index, speed_rating, pattern_id,
                price, wet_grip, fuel_efficiency, db_rating_number, db_rating_letter,
                budget, electric, vehicle_tyre_type_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                tyre.tyre_width, tyre.aspect_ratio, tyre.rim_diameter, tyre.load_index, tyre.speed_rating, pattern_id, tyre.price, tyre.wet_grip, tyre.fuel_efficiency,
                tyre.db_rating_number, tyre.db_rating_letter, tyre.budget, tyre.electric, tyre.tyre_type
            )
        )

        self.conn.commit()

        return self.cursor.lastrowid