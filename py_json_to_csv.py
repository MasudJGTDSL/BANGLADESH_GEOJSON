import pandas as pd
import json
import csv
import argparse
import os

def json_to_csv_copilot_saved_places(json_file, csv_file):
    # Load the JSON file
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract features
    features = data["features"]

    # Flatten the JSON into a list of dicts
    rows = []
    for feature in features:
        props = feature.get("properties", {})
        geom = feature.get("geometry", {})
        coords = geom.get("coordinates", [None, None])

        row = {
            "name": props.get("location", {}).get("name"),
            "address": props.get("location", {}).get("address"),
            "country_code": props.get("location", {}).get("country_code"),
            "comment": props.get("Comment"),
            "date": props.get("date"),
            "google_maps_url": props.get("google_maps_url"),
            "longitude": coords[0],
            "latitude": coords[1],
        }
        rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(rows)
    df = df[~((df["longitude"] == 0) & (df["latitude"] == 0))]

    # Save to CSV
    df.to_csv(csv_file, index=False, encoding="utf-8")

    print("CSV file created successfully!")


def json_to_csv_copilot_reviews(json_file, csv_file):
    # Load the JSON file
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract features
    features = data["features"]

    # Flatten the JSON into a list of dicts
    rows = []
    for feature in features:
        props = feature.get("properties", {})
        geom = feature.get("geometry", {})
        coords = geom.get("coordinates", [None, None])

        row = {
            "name": props.get("location", {}).get("name"),
            "address": props.get("location", {}).get("address"),
            "country_code": props.get("location", {}).get("country_code"),
            "comment": props.get("Comment"),
            "date": props.get("date"),
            "google_maps_url": props.get("google_maps_url"),
            "rating": props.get("five_star_rating_published"),
            "review_text": props.get("review_text_published"),
            "longitude": coords[0],
            "latitude": coords[1],
        }
        rows.append(row)

    # Create DataFrame
    df = pd.DataFrame(rows)
    # 🚫 Drop rows where longitude and latitude are both 0
    df = df[~((df["longitude"] == 0) & (df["latitude"] == 0))]

    # Save to CSV
    df.to_csv(csv_file, index=False, encoding="utf-8")

    print("CSV file created successfully!")

def json_to_csv_pandas(json_file, csv_file):
    """Converts a JSON file to a CSV file using pandas."""
    try:
        # Read JSON file into a pandas DataFrame
        df = pd.read_json(json_file)
        
        # Convert DataFrame to CSV file (index=False prevents writing row indices)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"Successfully converted {json_file} to {csv_file}")
        
    except ValueError as e:
        print(f"Error processing JSON: {e}. Consider using json_normalize for nested JSON.")
        # Example for nested JSON (requires different approach or data structure)
        # import json
        # with open(json_file, 'r', encoding='utf-8') as f:
        #     data = json.load(f)
        #     df = pd.json_normalize(data)
        #     df.to_csv(csv_file, index=False, encoding='utf-8')

# Example usage:
# Create a dummy json file for testing:
# with open('data.json', 'w') as f:
#     f.write('[{"col1": 1, "col2": 2}, {"col1": 3, "col2": 4}]')
# 
# json_to_csv_pandas('data.json', 'output.csv')
# F:\BANGLADESH_GEOJSON\src\data\bd-postcodes.json

def json_to_csv_builtin(json_file, csv_file):
    """Converts a flat JSON file (list of dicts) to a CSV file using built-in modules."""
    with open(json_file, 'r', encoding='utf-8') as f_in:
        data = json.load(f_in)

    # Ensure the data is a list of dictionaries
    if not isinstance(data, list) or not all(isinstance(row, dict) for row in data):
        print("Error: JSON data must be a list of uniform dictionaries for this method.")
        return

    # Extract field names (headers) from the first dictionary
    fieldnames = data[0].keys()

    with open(csv_file, 'w', newline='', encoding='utf-8') as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        
        writer.writeheader()  # Write the header row
        writer.writerows(data) # Write the data rows
    
    print(f"Successfully converted {json_file} to {csv_file}")

# Example usage:
# Create a dummy json file for testing:
# with open('employees.json', 'w') as f:
#     f.write('[{"name": "John", "age": 30}, {"name": "Jane", "age": 25}]')
#
# json_to_csv_builtin('employees.json', 'employees.csv')


def nested_json_to_csv(json_file, csv_file):
    """Converts a nested JSON file to a CSV file by flattening with pandas."""
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    data_final = []
#     geometry
# coordinates
    for dt in data["features"]:
        data_final.append({"id":dt["id"]}|{"union_id":0}|{"lat":dt["geometry"]["coordinates"][1]}|{"long":dt["geometry"]["coordinates"][0]}|dt["properties"])
    # print(data_final[0:2])
    # Flatten the JSON data
    df = pd.json_normalize(data_final)
    
    # Convert to CSV
    df.to_csv(csv_file, index=False, encoding='utf-8')
    print(f"Successfully converted nested JSON to {csv_file}")

# Example usage with nested data:
# with open('nested_data.json', 'w') as f:
#      f.write('[{"id": "0001", "type": "donut", "batters": {"batter": [{"id": "1001", "type": "Regular"}]}}]')
#
# nested_json_to_csv('nested_data.json', 'nested_output.csv')
def main():
    """
    Main function to handle command-line arguments for JSON to CSV conversion.
    """
    parser = argparse.ArgumentParser(
        description="""Convert a JSON file to an CSV file.

Example usage:
  python json_to_csv_pandas.py my_document.json
  python json_to_csv_pandas.py my_document.json -o my_output.csv
""",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "json_file",
        help="Path to the input JSON file."
    )
    parser.add_argument(
        "-o", "--output",
        dest="csv_file",
        help="Path to the output CSV file.\nIf not provided, it will be generated from the input file name (e.g., 'input.json' -> 'input.csv')."
    )

    args = parser.parse_args()

    json_path = args.json_file
    csv_path = args.csv_file

    if not csv_path:
        # If no output file is specified, create one from the input file name.
        base, _ = os.path.splitext(json_path)
        csv_path = base + ".csv"

    nested_json_to_csv(json_path, csv_path.format("_nested_json_to_csv"))
    json_to_csv_pandas(json_path, csv_path.format("_json_to_csv_pandas")) 
    json_to_csv_builtin(json_path, csv_path.format("_json_to_csv_builtin")) 

#! To Run: python py_json_to_csv.py "z_File_Conversion/input_file.json" -o "z_File_Conversion/output_file{}.csv"
#! To Run: python py_json_to_csv.py "z_File_Conversion/Saved Places.json" -o "z_File_Conversion/Saved Places{}.csv"
if __name__ == "__main__":
    # json_to_csv_copilot_saved_places("Bangladesh_GeoJSON_Data/small/small_bangladesh_geojson_adm3_492_upozila.json", "Bangladesh_GeoJSON_Data/Saved Places.csv")
    # json_to_csv_copilot_reviews("Bangladesh_GeoJSON_Data/small/small_bangladesh_geojson_adm3_492_upozila.json", "Bangladesh_GeoJSON_Data/Reviews.csv")
    # nested_json_to_csv("Bangladesh_GeoJSON_Data/bangladesh_geojson_admALL_2_entire_bd_division_district_unions.json", "Bangladesh_GeoJSON_Data/geojson_5160_unions_thanas.csv")
    # main()
    json_file = r"F:\BANGLADESH_GEOJSON\src\data\bd-postcodes.json"
    csv_file = r"F:\BANGLADESH_GEOJSON\src\data\bd-postcodes.csv"
    json_to_csv_pandas(json_file,csv_file)