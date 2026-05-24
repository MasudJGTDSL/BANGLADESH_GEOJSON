import sqlite3
import json
import csv
from tqdm import tqdm
from shapely.geometry import Point, shape
from shapely.strtree import STRtree

import geopandas as gpd

def area_n_perimeter(file_path, output_file):
    # Load the GeoJSON file
    gdf = gpd.read_file(file_path)

    # Reproject to a metric CRS (Bangladesh is in UTM Zone 46N, EPSG:32646)
    gdf = gdf.to_crs(epsg=32646)

    # Calculate perimeter (km) and area (km²)
    gdf["Perimeter_km"] = gdf.geometry.length / 1000
    gdf["Area_km2"] = gdf.geometry.area / 1e6

    # Inspect Abaipur Union
    abaipur = gdf[gdf["ADM4_EN"] == "Abaipur"][["ADM4_EN", "Perimeter_km", "Area_km2"]]

    # Convert to dictionary (row-wise)
    result_dict = abaipur.to_dict(orient="records")[0]  # returns a list of dicts, take first
    print(result_dict)

    return result_dict

import geopandas as gpd

def area_n_perimeter_all(file_path, output_file, name_field):
    # Load the GeoJSON file
    gdf = gpd.read_file(file_path)
    print("Initial: ",gdf.head)
    # Reproject to a metric CRS (Bangladesh is in UTM Zone 46N, EPSG:32646)
    gdf = gdf.to_crs(epsg=32646)
    print("After .to_crs: ", gdf.head)
    # Calculate perimeter (km) and area (km²)
    gdf["Perimeter_km"] = gdf.geometry.length / 1000
    gdf["Area_km2"] = gdf.geometry.area / 1e6
    # gdf["feature_id"] = gdf.index

    # Select relevant columns
    result = gdf[[name_field, "Perimeter_km", "Area_km2"]]

    # Convert all rows to list of dictionaries
    result_dicts = result.to_dict(orient="records")
    
        # 5. Save to CSV

    result.to_csv(output_file, index=True, encoding='utf-8')

    # return result_dicts


def export_feature_matches(
    db_path="db.sqlite3",
    table_name="geo_locations_districts",
    json_path="bangladesh_geojson_adm2_64_districts_zillas.json",
    output_csv="district_feature_matches.csv"
):
    # 1. Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 2. Fetch rows from table
    cursor.execute(f"SELECT id, name, lat, long FROM {table_name}")
    rows = cursor.fetchall()

    # 3. Load GeoJSON
    with open(json_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    features = geojson_data["features"]

    results = []

    # 4. For each row, check if point lies inside any feature polygon
    for row in tqdm(rows, desc="Processing Rows", unit="Row"):
        row_id, name, lat, lon = row
        point = Point(lon, lat)  # GeoJSON uses (lon, lat)

        matched_feature_id = None
        for feature in features:
            geom = shape(feature["geometry"])
            if geom.contains(point):
                matched_feature_id = feature.get("id")
                break

        if matched_feature_id is not None:
            results.append({
                "table_id": row_id,
                "feature_id": matched_feature_id,
                "name": name,
                "lat": lat,
                "long": lon
            })

    # 5. Save to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["table_id", "feature_id", "name", "lat", "long"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    conn.close()
    print(f"✅ Exported {len(results)} matches to {output_csv}")


def export_feature_matches_fast(
    db_path="bd.sqlite3",
    table_name="geo_locations_districts",
    json_path="bangladesh_geojson_adm2_64_districts_zillas.json",
    output_csv="district_feature_matches.csv"
):
    # 1. Connect to SQLite
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, name, lat, long FROM {table_name}")
    rows = cursor.fetchall()

    # 2. Load GeoJSON
    with open(json_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    features = geojson_data["features"]

    # 3. Build shapely geometries + STRtree index
    geometries = [shape(feature["geometry"]) for feature in features]
    feature_ids = [feature.get("id") for feature in features]

    # STRtree for fast spatial queries
    tree = STRtree(geometries)

    results = []

    # 4. For each row, query nearby polygons via STRtree
    for row_id, name, lat, lon in tqdm(rows, desc="Processing Rows", unit="Row"):
        point = Point(lon, lat)

        # Candidate indices from spatial index
        candidate_idxs = tree.query(point)

        matched_feature_id = None
        for idx in candidate_idxs:
            geom = geometries[idx]   # use index to get geometry
            if geom.contains(point):
                matched_feature_id = feature_ids[idx]
                break

        if matched_feature_id is not None:
            results.append({
                "table_id": row_id,
                "feature_id": matched_feature_id,
                "name": name,
                "lat": lat,
                "long": lon
            })

    # 5. Save to CSV
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["table_id", "feature_id", "name", "lat", "long"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    conn.close()
    print(f"✅ Exported {len(results)} matches to {output_csv}")




#! To Run: python py_geojson.py

if __name__ == "__main__":
    """ 
    export_feature_matches_fast(
    db_path="db.sqlite3",
    table_name="geo_locations_districts",
    json_path="Bangladesh_GeoJSON_Data/bangladesh_geojson_adm2_64_districts_zillas.json",
    output_csv="feature_matches_geo_locations_districts.csv"
    ) """
    
    
    export_feature_matches_fast(
    db_path="db_backup.sqlite3",
    table_name="geo_locations_unions",
    json_path="BANGLADESH GEO_JSON SCRAP DATA/Bangladesh_GeoJSON_Data/bangladesh_geojson_adm4_5160_unions_thanas.json",
    output_csv="feature_matches_unions_fast.csv"
    )
    
    """ 
    export_feature_matches(
    db_path="db_backup.sqlite3",
    table_name="geo_locations_unions",
    json_path="BANGLADESH GEO_JSON SCRAP DATA/Bangladesh_GeoJSON_Data/bangladesh_geojson_adm4_5160_unions_thanas.json",
    output_csv="feature_matches_unions.csv"
    ) """
    # area_n_perimeter()
    
    """ 
    file_path = "Bangladesh_GeoJSON_Data/bangladesh_geojson_adm1_8_divisions_bibhags.json"
    output_file = "adm1_8_divisions.csv"
    name_field = "ADM1_EN"
    area_n_perimeter_all(file_path, output_file, name_field) 
    """