import sqlite3
import json
import os

def json_to_sqlite(json_file, db_path="example.db", table_name="my_table"):
    # ✅ Check if JSON file exists
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"{json_file} not found.")

    # ✅ Load JSON data
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Normalize: ensure list of records
    if isinstance(data, dict):
        data = [data]
    
    print(data[0])

    if not isinstance(data, list):
        raise ValueError("JSON must be an object or list of objects.")

    # ✅ Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # ✅ Auto-create table if not exists
    columns = data[0].keys()
    col_defs = ", ".join([f"{col} TEXT" for col in columns])
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({col_defs})")

    # ✅ Insert records
    placeholders = ", ".join(["?"] * len(columns))
    sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    try:
        cursor.executemany(sql, [tuple(record.values()) for record in data])
        conn.commit()
        print(f"Inserted {len(data)} records into {table_name}.")
    except Exception as e:
        conn.rollback()
        print(f"Error inserting data: {e}")
    finally:
        conn.close()
"""
UPDATE temp_postcodes
SET 
    upozila_from_upzila = (
        SELECT name 
        FROM temp_upazilas 
        WHERE temp_upazilas.name = temp_postcodes.upazila
    ),
    upozila_id = (
        SELECT id 
        FROM temp_upazilas 
        WHERE temp_upazilas.name = temp_postcodes.upazila
    )
WHERE EXISTS (
    SELECT 1 
    FROM temp_upazilas 
    WHERE temp_upazilas.name = temp_postcodes.upazila
);

UPDATE temp_postcodes
SET 
    bn_name = (
        SELECT bn_name
        FROM geo_locations_upazilas 
        WHERE temp_postcodes.upazila = geo_locations_upazilas.name
    ),
    upozila_id_2 = (
        SELECT id 
        FROM geo_locations_upazilas 
        WHERE temp_postcodes.upazila = geo_locations_upazilas.name
    )
WHERE EXISTS (
    SELECT 1 
    FROM geo_locations_upazilas 
    WHERE temp_postcodes.upazila = geo_locations_upazilas.name
);

INSERT INTO geo_locations_divisions (id, name, bn_name, lat, long)
SELECT id, name, bn_name, lat, long 
FROM temp_divisions;

INSERT INTO geo_locations_districts (id, name, bn_name, lat, long, division_id)
SELECT id, name, bn_name, lat, long, division_id 
FROM temp_districts;

INSERT INTO geo_locations_upazilas (id, name, bn_name, lat, long, district_id)
SELECT id, name, bn_name, 0, 0, district_id 
FROM temp_upazilas;

INSERT INTO geo_locations_divisions (id, name, bn_name, lat, long, url) 
SELECT id, name, bn_name,0,0,url FROM temp_divisions_2 ;

INSERT INTO geo_locations_districts (id, name, bn_name, lat, long, url,division_id) 
SELECT id, name, bn_name,0,0,url,division_id FROM temp_districts_2 ;


INSERT INTO geo_locations_upazilas (id, name, bn_name, lat, long, url,district_id) 
SELECT id, name, bn_name,0,0,url,district_id FROM temp_upazilas_2 ;

INSERT INTO geo_locations_unions (id, name, bn_name, lat, long, url,upazila_id) 
SELECT id, name, bn_name,0,0,url,upazilla_id FROM temp_unions_2 ;


UPDATE geo_locations_divisions 
SET 
    lat = (
        SELECT lat 
        FROM temp_divisions 
        WHERE geo_locations_divisions.name = temp_divisions.name
    ),
    long = (
        SELECT long 
        FROM temp_divisions 
        WHERE geo_locations_divisions.name = temp_divisions.name
    )
WHERE EXISTS (
    SELECT 1 
    FROM temp_divisions 
    WHERE geo_locations_divisions.name = temp_divisions.name
);

UPDATE geo_locations_districts 
SET 
    lat = (
        SELECT lat 
        FROM temp_districts 
        WHERE geo_locations_districts.name = temp_districts.name
    ),
    long = (
        SELECT long 
        FROM temp_districts 
        WHERE geo_locations_districts.name = temp_districts.name
    )
WHERE EXISTS (
    SELECT 1 
    FROM temp_districts 
    WHERE geo_locations_districts.name = temp_districts.name
);


UPDATE geo_locations_upazilas 
SET 
    lat = (
        SELECT Latitude 
        FROM UPAZILA_BD_WITH_LAT_LONG 
        WHERE geo_locations_upazilas.name = UPAZILA_BD_WITH_LAT_LONG.Name
    ),
    long = (
        SELECT Longitude 
        FROM UPAZILA_BD_WITH_LAT_LONG 
        WHERE geo_locations_upazilas.name = UPAZILA_BD_WITH_LAT_LONG.Name
    )
WHERE EXISTS (
    SELECT 1 
    FROM UPAZILA_BD_WITH_LAT_LONG 
    WHERE geo_locations_upazilas.name = UPAZILA_BD_WITH_LAT_LONG.Name
);

"""

#! To Run: python py_json_file_to_sqlite3.py
JASON_FILE = "z_data/unions.json"
DB_NAME = "db.sqlite3"
TABLE_NAME = "temp_unions_2"

if __name__ == "__main__":
    json_to_sqlite(json_file =JASON_FILE, db_path=DB_NAME, table_name=TABLE_NAME)
