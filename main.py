import osm_graph
import network_risk
import json
import sys
import os

input_json = sys.argv[1]

with open(input_json) as f:
    input = json.load(f)
    output_dir = input['output_dir']
    locations_table_name = input['name'] + '_locations'
    subnetwork_json_path = os.path.join(output_dir, input['name'] + '_subnetwork.json')
    subnetwork_pycgr_path = os.path.join(output_dir, input['name'] + '_subnetwork.pycgrc')
    # process    
    osm_graph.load_locations_and_routes(input['name'], input['network_pycgr_file'])
    osm_graph.get_nearest_node_ids(locations_table_name, input['poi_file'])
    osm_graph.create_subgraph(input['poi_file'], input['network_json_file'], subnetwork_json_path)
    osm_graph.graph_to_pycgr(subnetwork_json_path, subnetwork_pycgr_path)
    osm_graph.resolve_conflicting_nodes(locations_table_name, input['poi_file'], subnetwork_pycgr_path)
    osm_graph.reindex_graph_locations(input['poi_file'])
    if 'risk_layer_file' in input and 'risk_coordinates_samples' in input:
        network_risk.generate_risk_from_pycgr(input['network_pycgr_file'], input['risk_layer_file'], input['risk_coordinates_samples'])
        network_risk.generate_risk_from_pycgr(subnetwork_pycgr_path, input['risk_layer_file'], input['risk_coordinates_samples'])
