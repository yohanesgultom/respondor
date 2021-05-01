from flask import Flask, render_template
import configparser
import os
import sys
import csv

DEFAULT_ZOOM = 12

# config
config = configparser.ConfigParser()
config.read('config.ini')
if not 'mapbox_access_token' in config['respondor']:
    raise ValueError('No mapbox_access_token found in config')
MAPBOX_ACCESS_TOKEN = config['respondor']['mapbox_access_token']

# get input path
if len(sys.argv) < 3:
    print('Usage: python app.py <LOCATIONS_PATH> <PYCGR_PATH>')
    sys.exit(1)

_, LOCATIONS_PATH, PYCGR_PATH = sys.argv
print(f'LOCATIONS_PATH={LOCATIONS_PATH}')
print(f'PYCGR_PATH={PYCGR_PATH}')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', MAPBOX_ACCESS_TOKEN=MAPBOX_ACCESS_TOKEN)

@app.route('/data')
def data():
    # read pycgr    
    coords_map = {}
    nodes = []
    routes = []
    total_nodes = None
    total_edges = None
    count_edges = 0
    count_nodes = 0
    print(f'reading {PYCGR_PATH}')
    with open(PYCGR_PATH) as f:
        count = 0
        for line in f:
            if count == 7:
                total_nodes = int(line)
            elif count == 8:
                total_edges = int(line)
            elif count > 8:
                if count_nodes < total_nodes:
                    # start reading nodes
                    node_id, lat, lon = line.split()
                    coords_map[node_id] = (float(lat), float(lon))
                    count_nodes += 1            
                else:
                    # start reading edges
                    source_id, target_id, length, street_type, max_speed, bidirectional = line.split()
                    routes.append({
                        'coords': [coords_map[source_id], coords_map[target_id]],
                        'color': '#0760f0',
                    })
                    count_edges += 1
            count += 1

    # read locations
    color_map = {
        'village': '#f5ad42',
        'shelter': '#4bf542',
        'depot': '#2fbdfa',
        'airport': '#2fbdfa',
        'warehouse': '#0b72e0',
        'damaged': '#e0260d',
    }
    symbol_map = {
        'village': 'pitch',
        'shelter': 'embassy',
        'warehouse': 'grocery',
        'depot': 'car',
        'airport': 'airport',
        'damaged': 'danger',
    }
    with open(LOCATIONS_PATH) as f:
        min_lat = 90.0
        min_lon = 180.0
        max_lat = -90.0
        max_lon = -180.0
        reader = csv.reader(f)
        for row in reader:
            assert len(row) >= 5
            name = row[0]
            cat = row[1]
            lat = row[2]
            lon = row[3]
            node_id = row[4]
            coords = coords_map[node_id]            
            nodes.append({
                'coords': coords,
                'type': cat,
                'color': color_map[cat] if cat in color_map else '#ccc' ,
                'symbol': symbol_map[cat] if cat in symbol_map else 'circle',
                'size': 'large',
            })
            lat, lon = coords
            min_lat = lat if lat <= min_lat else min_lat
            min_lon = lon if lon <= min_lon else min_lon
            max_lat = lat if lat >= max_lat else max_lat
            max_lon = lon if lon >= max_lon else max_lon

    center = ((max_lat+min_lat)/2, (max_lon+min_lon)/2)
    return {
        'center': { 'coords': center, 'zoom': DEFAULT_ZOOM},
        'routes': routes,
        'nodes': nodes,
    }


if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=5000)
