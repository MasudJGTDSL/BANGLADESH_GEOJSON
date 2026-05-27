import requests
import csv

BASE_URL = "https://ekdak.com/thikana/pocode"
HEADERS = {
    "Authorization": "Token 2843d5e2131498eccc565e4d7cab3ea809b2b2c7"
}

def fetch_data(endpoint, params=None):
    """Fetch JSON data from API with optional query params."""
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}", headers=HEADERS, params=params)
        response.raise_for_status()
        return response.json().get("data", [])
    except Exception as e:
        print(f"Error fetching {endpoint}: {e}")
        return []

def main():
    rows = []
    # Step 1: Divisions
    divisions = fetch_data("divisions")
    for div in divisions:
        div_id, div_name = div["id"], div["en_name"]

        # Step 2: Districts
        districts = fetch_data("districts", {"v": div_id})
        for dist in districts:
            dist_id, dist_name = dist["id"], dist["en_name"]

            # Step 3: Police Stations
            police_stations = fetch_data("police-stations", {"d": dist_id})
            for ps in police_stations:
                ps_id, ps_name = ps["id"], ps["en_name"]

                # Step 4: Post Offices
                post_offices = fetch_data("post-offices", {"t": ps_id})
                for po in post_offices:
                    po_name, po_code = po["en_name"], po["code"]

                    rows.append([
                        div_id, div_name,
                        dist_id, dist_name,
                        ps_id, ps_name,
                        po_name, po_code
                    ])

    # Save to CSV
    with open("bangladesh_postcodes_1.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["div_id","Division","dist_id","District","ps_id","Police_Station","Post_Office","Post_Code"])
        writer.writerows(rows)

    print("✅ Data saved to bangladesh_postcodes.csv")

#  python py_postcode_collection_1.py

if __name__ == "__main__":
    main()
