import json, os
from flask import Flask, request, jsonify
from shapely.geometry import Point, Polygon, shape

app = Flask(__name__)

flood_zones_geojson = []

zones_folder = "zones"

for filename in os.listdir(zones_folder):
    if filename.endswith(".geojson"):
        with open(os.path.join(zones_folder, filename), "r") as f:
            data = json.load(f)
            flood_zones_geojson.append({
            "polygon": shape(data["geometry"]),
            "properties" : data["properties"]
            })

@app.route("/check", methods=["POST"])

def check_location():
    data = request.get_json()
    lat = data.get("lat")
    lon = data.get("lon")
    
    if lat is None or lon is None:
        return jsonify({"error": "Latitude and longitude are required"}), 400
    
    point = Point(lon, lat)
    
    for zone in flood_zones_geojson:
        if zone["polygon"].contains(point):
            return jsonify({
                "point" :[lat,lon],
                "inside_flood_zone": True,
                "zone_properties": zone["properties"]["name"],
                "risk_level": zone["properties"]["risk"]
            
            }), 200
    return jsonify({
        "point": [lat, lon],
        "inside_flood_zone": False,
        "zone" : None,
        "risk": None
    }), 200
    

if __name__ == "__main__":
    app.run(debug=True)
    