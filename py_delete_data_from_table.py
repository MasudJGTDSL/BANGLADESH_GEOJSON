import json
from datetime import datetime
import sqlite3
import os
from tqdm import tqdm
# from py_decorators import time_of_execution
# from py_copy_delete_file import copy_file, delete_file
from py_display import display

def delete_data_from_table(table_name, DB_NAME):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"DELETE FROM {table_name}")
    cursor.execute(f"UPDATE sqlite_sequence SET seq = 0 WHERE name = '{table_name}'")
    conn.commit()
    conn.close()
    
#! To Run: python py_delete_data_from_table.py
DB_NAME = "db.sqlite3"
# TABLE_NAME = "geo_locations_divisions"

TABLE_LIST = [
"geo_locations_GeoFeatureBangladesh",
"geo_locations_GeoFeatureDivision",
"geo_locations_GeoFeatureDivisionSmall",
"geo_locations_GeoFeatureDistrict",
"geo_locations_GeoFeatureDistrictSmall",
"geo_locations_GeoFeatureUpazila",
"geo_locations_GeoFeatureUpazilaSmall",
"geo_locations_GeoFeatureUnion",
"geo_locations_GeoFeatureUnionSmall",
"geo_locations_GeoFeatureAll_1",
"geo_locations_GeoFeatureAll_2"
]

if __name__ == "__main__":
    for tbl in TABLE_LIST:
        delete_data_from_table(table_name=tbl.lower(), DB_NAME=DB_NAME)