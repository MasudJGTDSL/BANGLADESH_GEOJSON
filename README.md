# Bangladesh Administrative Boundary GIS

A comprehensive Geographic Information System (GIS) built with Django for managing and visualizing the administrative boundaries of Bangladesh. This project provides detailed geographical data from the Division level down to the Union level, featuring interactive maps, data visualization, and automated data processing tools.

## 🚀 Features

- **Administrative Hierarchy**: Full support for Bangladesh's administrative structure:
  - Divisions
  - Districts
  - Upazilas (Sub-districts)
  - Unions
- **Interactive Mapping**: Uses **Leaflet.js** to render GeoJSON polygons for each administrative level.
- **Data Visualization**: Integrated **Plotly** charts for area and perimeter comparisons across different regions.
- **Geospatial Analysis**: Automatic calculation of area (km²) and perimeter (km) using **GeoPandas** and **Shapely**.
- **Dynamic Filtering**: Seamlessly filter and drill down through administrative levels via AJAX-powered interfaces.
- **Automated Data Processing**: Suite of Python utility scripts for:
  - GeoJSON data cleaning and validation.
  - Coordinate collection and matching.
  - SQLite database management and bulk insertion.
- **Modern UI**: Styled with **Tailwind CSS** and **DaisyUI** for a responsive and clean user experience.

## 🛠️ Tech Stack

- **Backend**: Python 3.x, Django 6.0.5
- **Database**: SQLite (default)
- **Frontend**: Tailwind CSS, DaisyUI, Leaflet.js
- **Data Science/GIS**: GeoPandas, Shapely, Pandas, NumPy
- **Visualization**: Plotly
- **Utilities**: tqdm, WhiteNoise, python-dotenv

## 📋 Project Structure

```text
├── BANGLADESH_GEOJSON/   # Project settings and configuration
├── geo_locations/        # Main application logic, models, and views
├── data/                 # Compressed GeoJSON data files
├── static/               # CSS, JavaScript, and Image assets
├── templates/            # HTML templates for the map and dashboard
├── theme/                # Tailwind CSS theme application
├── py_*.py               # Data processing and utility scripts
└── manage.py             # Django management script
```

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/MasudJGTDSL/BANGLADESH_GEOJSON.git
cd BANGLADESH_GEOJSON
```

### 2. Create a Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and add the following:
```env
SECRET_KEY=%$!5%t)zwe3avg7+gubhfbqo@a1788k=9y2oukfgmgj4mbs-$c
DEBUG=1
ALLOWED_HOSTS=localhost 127.0.0.1
STATIC_ROOT=static_files
MEDIA_ROOT=media
NPM_BIN_PATH=C:/Program Files/nodejs/npm.cmd  # Adjust to your npm path
```

### 5. Run Migrations
```bash
python manage.py migrate
```

### 6. Initialize Tailwind CSS
```bash
python manage.py tailwind install
python manage.py tailwind build
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

## 📊 Data Processing Utilities

The project includes several `py_*.py` scripts to handle data:
- `py_json_to_sqlite3.py`: Bulk import JSON data into the SQLite database.
- `py_geojson.py`: Geospatial calculations and matching between records and GeoJSON features.
- `py_collect_union_coordinates.py`: Aggregate coordinate data for unions.
- `py_delete_data_from_table.py`: Utility for cleaning specific database tables.

## 🗺️ Usage

1. **Dashboard**: The main index page provides an overview of Bangladesh's divisions with area statistics.
2. **Interactive Selection**: Use the dropdown menus to select a Division, District, Upazila, or Union.
3. **Map Display**: Upon selection, the map will automatically zoom to the selected region and highlight its boundaries.
4. **Information Card**: Detailed information, including area and perimeter, will be displayed for the selected entity.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
