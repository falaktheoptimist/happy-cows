""" String Constants and Table Definitions for database
"""

DATABASE_NAME = "happycows"
DATABASE_PATH = "data/intermediate/"

CREATE_CLASSIFICATION_TABLE = """
    CREATE TABLE IF NOT EXISTS classification(
        date            DATE    NOT NULL,
        animal_id       INT     NOT NULL,
        lactation       INT,
        date_calved     DATE,
        locomotion      INT,
        front_capacity  INT,
        dairy_strength  INT,
        rump            INT,
        feet_and_legs   INT,
        udder           INT,
        final_score     INT     NOT NULL,
        baa             REAL, 
        category        TEXT,
        PRIMARY KEY (date, animal_id)
    )
"""

CREATE_WEATHER_TABLE = """
    CREATE TABLE IF NOT EXISTS weather(
        date            DATE    NOT NULL,
        station_id      TEXT    NOT NULL,
        precipitation   REAL,
        temp_min        REAL,
        temp_max        REAL,
        PRIMARY KEY (date, station_ID)
    )
"""

CREATE_PRODUCTION_VOLUME_TABLE = """
    CREATE TABLE IF NOT EXISTS production_volume(
        date            DATETIME    NOT NULL,
        animal_id       INT         NOT NULL,
        milk_weight     REAL,
        duration        TEXT,
        average_flow    REAL,
        max_flow        REAL,
        PRIMARY KEY (date, animal_id)
    )
"""