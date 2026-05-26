from flask import Blueprint, jsonify
import json
import os

crime_data_bp = Blueprint('crime_data_bp', __name__)

@crime_data_bp.route("/api/crime-data", methods=["GET"])
def get_crime_data():
    json_path = os.path.join(os.path.dirname(__file__), "data/crime_clusters.geojson")
    with open(json_path, encoding="utf-8") as f:
        geojson = json.load(f)
    records = []
    for feature in geojson["features"]:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        # GeoJSON: [longitude, latitude]
        record = {
            "Longitude": coords[0],
            "Latitude": coords[1],
            "attack type": props.get("attack type", ""),
            "city": props.get("city", ""),
            "day": props.get("day", ""),
            "location": props.get("location", ""),
            "month": props.get("month", ""),
            "state": props.get("state", ""),
            "summary": props.get("summary", ""),
            "year": props.get("year", "")
        }
        records.append(record)
    return jsonify(records)