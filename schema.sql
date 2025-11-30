CREATE TABLE retailer
            (
                retailer_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                retailer_name TEXT NOT NULL UNIQUE
            );
CREATE TABLE sqlite_sequence(name,seq);
CREATE TABLE brand (
                brand_id INTEGER PRIMARY KEY AUTOINCREMENT,
                brand_name TEXT NOT NULL UNIQUE
            );
CREATE TABLE season (
                season_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                season_name TEXT NOT NULL UNIQUE
            );
CREATE TABLE vehicle_tyre_type (
                vehicle_tyre_type_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                vehicle_tyre_type_name TEXT NOT NULL UNIQUE
            );
CREATE TABLE pattern (
                pattern_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                pattern_name TEXT NOT NULL UNIQUE,
                brand_id INTEGER NOT NULL,
                season_id INTEGER NOT NULL,
                FOREIGN KEY (brand_id) REFERENCES brand(brand_id),
                FOREIGN KEY (season_id) REFERENCES season(season_id),
                UNIQUE(pattern_name, brand_id)
            );
CREATE TABLE tyre (
                tyre_id   INTEGER PRIMARY KEY AUTOINCREMENT,
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
                FOREIGN KEY (retailer_id) REFERENCES retailer(retailer_id),
                FOREIGN KEY (pattern_id) REFERENCES pattern(pattern_id),
                FOREIGN KEY (vehicle_tyre_type_id) REFERENCES vehicle_tyre_type(vehicle_tyre_type_id)
            );
