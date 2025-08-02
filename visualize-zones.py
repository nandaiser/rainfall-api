import json, folium, os
from shapely.geometry import Point, shape



zones_folder = "zones"
files = [f for f in os.listdir(zones_folder) if f.endswith('.geojson')]

center = [6.22, 106.85]  # Center of the map (Jakarta, Indonesia)

if files:
    with open(os.path.join(zones_folder,files[0]),"r") as f:
        data = json.load(f)
        polygon = shape(data["geometry"])
        center = [polygon.centroid.y,polygon.centroid.x]
        
m = folium.Map(location=center, zoom_start=13)

for filename in files:
    with open(os.path.join(zones_folder, filename), "r") as f:
        data = json.load(f)
        
        folium.GeoJson(
            data,
            name=data["properties"]["name"],
            tooltip = data["properties"]["name"],
            style_function=lambda x: {
                "fillColor": "red" if x["properties"]["risk"] == "high" else "orange" if x["properties"]["risk"] == "medium" else "green",
                "color": "black",
                "weight": 1,
                "fillOpacity": 0.5
            }
        ).add_to(m)
        
folium.LayerControl().add_to(m)
m.save("flood_zones_map.html")
print(f"Map saved as 'flood_zones_map.html")
