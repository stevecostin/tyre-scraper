import sqlite3

class TyreDB:
    """Database handler for tyre scraping"""
    def __init__(self):
        """Initialize database connection and create the tables."""
        self.conn = sqlite3.connect("tyres.db")
        self.cursor = self.conn.cursor()
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

        self.conn.commit()