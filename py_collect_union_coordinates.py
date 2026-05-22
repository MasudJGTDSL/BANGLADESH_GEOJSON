import sqlite3, json, urllib3, requests, re, urllib.parse
from datetime import datetime
from requests.exceptions import SSLError
from bs4 import BeautifulSoup, SoupStrainer
from fake_useragent import UserAgent
from geopy.geocoders import Nominatim
from tqdm import tqdm
from geopy.extra.rate_limiter import RateLimiter

from py_display_colors import Colors as CLR
from py_unicode_char import unicode_char_tupple

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def collect_coordinates(db_path, table_name, tag_name = "a"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Fetch rows from table
    cursor.execute(f"SELECT id, url FROM {table_name} ORDER by id;")
    rows = cursor.fetchall()
    geolocator = Nominatim(user_agent="geoapi")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)
    ua = UserAgent()
    headers = {'User-Agent': str(ua.chrome)}
    only_tags = SoupStrainer(tag_name)
    lst = []
    for row in tqdm(rows, desc="Processing URLs", unit="url"):
        url = fr"https://{row[1]}"

        try:
            r = requests.get(url, headers=headers, verify=False)
            soup = BeautifulSoup(r.text, "html.parser", parse_only=only_tags) 
        except:
            print(f"\n{CLR.Fg.red}Request URL: {url} not found{CLR.reset}")
            continue
        
        if tag_name =="a":
            try:
                pattern = r'@\d+'
                match = soup.find_all("a", href=re.compile(pattern))
                
                if match:
                    for m in match:
                        print(m)
                        href = m.get('href')
                        try:
                            pattern = r'@(?P<lat>-?\d+\.\d+),\s*(?P<long>-?\d+\.\d+)'
                            coord = re.search(pattern, href)
                            lst.append((row[0], coord["lat"],coord["long"]))
                            print("Latitude: ",coord["lat"], "Latitude: ",coord["long"])
                        except  SSLError as e:
                            print(f"URL: {row[1]} → SSL error: {e}")
                            continue
            except:
                print(f"\nNo match found")
                    
        else:
            try:
                iframe = soup.find("iframe", src=True)
                if iframe and "src" in iframe.attrs:
                    src_url = iframe["src"]
                    parsed_url = urllib.parse.urlparse(src_url)
                    params = urllib.parse.parse_qs(parsed_url.query)
                    q_value = params.get("q", [None])[0]

                    if q_value and "," in q_value:
                        lat, lon = q_value.split(",")
                        lst.append((row[0], lat,lon))
                        print(f"\nID {row[0]}, {q_value} → Latitude: {lat}, Longitude: {lon}")
                    elif q_value:
                        try:
                            location = geocode(q_value + ", Bangladesh")
                            if location:
                                lst.append((row[0], location.latitude,location.longitude))
                                print(f"\nID {row[0]}, {q_value} → Geocoded Latitude: {location.latitude}, Longitude: {location.longitude}")
                            else:
                                print(f"\033[38;5;208m {CLR.Bg.cyan}{CLR.bold}\033[2:4m ID {row[0]} → Could not geocode: {q_value}{CLR.reset}")
                        except Exception as e:
                            print(f"\nID {row[0]} → Geocoding error: {e}")
                else:
                    print(f"\nID {row[0]} → No iframe found")
            except:
                print(f"\nNot found iframe: {row[1]}")
            # except  SSLError as e:
            #     print(f"URL: {row[1]} → SSL error: {e}")
            #     continue
            # print(f"ID {row[0]} → Error extracting coordinates: {e}")

    cursor.close()
    conn.close()
    with open(f"z_union_coordinates/union_coordinates_tag_{tag_name}_{str(datetime.now().strftime('%Y%m%d%H%M%S'))}.txt", "w", encoding="utf-8") as f: 
        f.write(str(lst))

        
def iframe_collect_coordinates(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Fetch rows from table
    cursor.execute(f"SELECT id, url FROM {table_name} ORDER by id;")
    rows = cursor.fetchall()
    ua = UserAgent()
    headers = {'User-Agent': str(ua.chrome)}
    only_tags = SoupStrainer("iframe")
    lst = []
    for row in tqdm(rows, desc="Processing URLs", unit="url"):
        url = fr"https://{row[1]}"
        try:
            r = requests.get(url, headers=headers, verify=False)
            soup = BeautifulSoup(r.text, "html.parser", parse_only=only_tags) 
        except:
            print(f"\n{CLR.Fg.red}Request URL: {url} not found{CLR.reset}")
            continue
        try:
            iframe = soup.find("iframe", src=True)
            src = iframe["src"]
            print(f"\n{CLR.Fg.green}Request URL: {src} not found{CLR.reset}")
            # src = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2989.9143746688596!2d91.62583167444001!3d24.405168078229238!2m3!1f0!2f0!3f0!..."

            pattern = r"!2d(?P<long>-?\d+\.\d+)!3d(?P<lat>-?\d+\.\d+)"
            match = re.search(pattern, src)

            if match:
                lon = float(match.group("long"))
                lat = float(match.group("lat"))
                lst.append((row[0], lat,lon))
                print(f"\n{CLR.Fg.cornflower_blue}Latitude:, {lat}, Longitude:, {lon}{CLR.reset}")
            else:
                print(f"{CLR.Fg.red_3b}{row[1]} Not found{CLR.reset}")
        except TypeError as e:
            print(f"\n{CLR.Fg.red_3b}{row[1]} Not Iframe Found{CLR.reset}")
            # continue
    cursor.close()
    conn.close()
    with open(f"z_union_coordinates/union_coordinates_tag_iframe_2d_3d_{str(datetime.now().strftime('%Y%m%d%H%M%S'))}.txt", "w", encoding="utf-8") as f: 
        f.write(str(lst))
        
        
def all_a(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # Fetch rows from table
    cursor.execute(f"SELECT id, url FROM {table_name} ORDER by id;")
    rows = cursor.fetchall()
    ua = UserAgent()
    headers = {'User-Agent': str(ua.chrome)}
    only_tags = SoupStrainer("a")
    lst = []
    for row in tqdm(rows, desc="Processing URLs", unit="url"):
        url = fr"https://{row[1]}"

        try:
            r = requests.get(url, headers=headers, verify=False)
            soup = BeautifulSoup(r.text, "html.parser", parse_only=only_tags) 
        except:
            print(f"\n{CLR.Fg.red}Request URL: {url} not found{CLR.reset}")
            continue

        try:
            pattern = r'@\d+'
            match = soup.find_all("a", href=re.compile(pattern))
            
            if match:
                for m in match:
                    lst.append((row[0], m.get('href')))
        except:
            print(f"\nNo match found")
    cursor.close()
    conn.close()
    with open(f"z_union_coordinates/union_all_a_{str(datetime.now().strftime('%Y%m%d%H%M%S'))}.txt", "w", encoding="utf-8") as f: 
        f.write(str(lst))
        
"""def collect_coordinates(db_path, table_name):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT id, url FROM {table_name} ORDER BY id;")
    rows = cursor.fetchall()
    results = []

    ua = UserAgent()
    headers = {'User-Agent': str(ua.chrome)}
    geolocator = Nominatim(user_agent="geoapi")

    for row in tqdm(rows, desc="Processing URLs", unit="url"):
        url = f"https://{row[1]}"
        try:
            r = requests.get(url, headers=headers, timeout=10, verify=False)
            soup = BeautifulSoup(r.text, "html.parser", parse_only=SoupStrainer("a"))

            # Pattern for lat,long inside Google Maps href
            pattern = r'@(?P<lat>-?\d+\.\d+),(?P<long>-?\d+\.\d+)'
            match = None
            for a in soup.find_all("a", href=True):
                match = re.search(pattern, a["href"])
                if match:
                    lat, lon = match.group("lat"), match.group("long")
                    results.append({"id": row[0], "lat": lat, "lon": lon})
                    print(f"ID {row[0]} → Latitude: {lat}, Longitude: {lon}")
                    break

            # If no match, check iframe src
            if not match:
                # iframe = soup.find("iframe")
                soup_full = BeautifulSoup(r.text, "html.parser")
                iframe = soup_full.find("iframe")
                if iframe and "src" in iframe.attrs:
                    src_url = iframe["src"]
                    parsed_url = urllib.parse.urlparse(src_url)
                    params = urllib.parse.parse_qs(parsed_url.query)
                    q_value = params.get("q", [None])[0]

                    if q_value and "," in q_value:
                        lat, lon = q_value.split(",")
                        results.append({"id": row[0], "lat": lat, "lon": lon})
                        print(f"ID {row[0]} → Latitude: {lat}, Longitude: {lon}")
                    elif q_value:
                        try:
                            location = geolocator.geocode(q_value + ", Bangladesh", timeout=10)
                            if location:
                                results.append({"id": row[0], "lat": location.latitude, "lon": location.longitude})
                                print(f"ID {row[0]} → Geocoded Latitude: {location.latitude}, Longitude: {location.longitude}")
                            else:
                                print(f"ID {row[0]} → Could not geocode: {q_value}")
                        except Exception as e:
                            print(f"ID {row[0]} → Geocoding error: {e}")
                else:
                    print(f"ID {row[0]} → No iframe found")

        except requests.exceptions.RequestException as e:
            print(f"ID {row[0]} → Request error: {e}")
            continue

    conn.close()

    # Save results as JSON
    with open("py_coordinates.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return results"""


#! To Run: python py_collect_union_coordinates.py

if __name__ == "__main__":
    db_path, table_name = "db.sqlite3", "geo_locations_unions"
    # collect_coordinates(db_path, table_name, tag_name = "a")
    # collect_coordinates(db_path, table_name, tag_name = "iframe")
    # iframe_collect_coordinates(db_path, table_name)
    all_a(db_path, table_name)




