import requests
import csv
import os
import argparse

BASE_URL = "https://ekdak.com/thikana/pocode"

def fetch_data(endpoint, token, params=None):
    """Fetch JSON data from API with optional query params."""
    headers = {"Authorization": f"Token {token}"}
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return []

def main(token, output_file):
    rows = []
    divisions = fetch_data("divisions", token)
    for div in divisions:
        div_id, div_name = div["id"], div["en_name"]

        districts = fetch_data("districts", token, {"v": div_id})
        for dist in districts:
            dist_id, dist_name = dist["id"], dist["en_name"]

            police_stations = fetch_data("police-stations", token, {"d": dist_id})
            for ps in police_stations:
                ps_id, ps_name = ps["id"], ps["en_name"]

                post_offices = fetch_data("post-offices", token, {"t": ps_id})
                for po in post_offices:
                    po_name, po_code = po["en_name"], po["code"]

                    rows.append([
                        div_name,
                        dist_name,
                        ps_name,
                        po_name,
                        po_code
                    ])

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Division", "District", "Police Station", "Post Office", "Post Code"])
        writer.writerows(rows)

    print(f"✅ Data saved to {output_file}")
#  python py_postcode_collection.py
# python 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download Bangladesh postal data as CSV")
    parser.add_argument("--token", help="API token", default=os.getenv("EKDAK_TOKEN"))
    parser.add_argument("--output", help="Output CSV file", default="bangladesh_postcodes.csv")
    args = parser.parse_args()

    if not args.token:
        raise ValueError("❌ No token provided. Use --token or set EKDAK_TOKEN environment variable.")

    main(args.token, args.output)
