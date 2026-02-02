import json
from flask import Blueprint, request, jsonify
from services.llm import translate_text  # import function from llm.py

data = Blueprint("data", __name__)

# Load JSON
with open("data/countries+cities.json", encoding="utf-8") as f:
    CITIES = json.load(f)
with open("data/lang.json", "r", encoding="utf-8") as f:
    LANGUAGES = json.load(f)

# Countries
@data.route("/countries")
def countries():
    return jsonify([{"name": c["name"]} for c in CITIES])

# City search
@data.route("/search-city")
def search_city():
    q = request.args.get("q", "").lower()
    country = request.args.get("country")
    for c in CITIES:
        if c["name"] == country:
            return jsonify([x for x in c["cities"] if x.lower().startswith(q)][:8])
    return jsonify([])

# Languages
@data.route("/languages")
def get_languages():
    with open("data/lang.json", "r", encoding="utf-8") as f:
        languages = json.load(f)
    return jsonify(languages)

# Translate 
@data.route("/translate", methods=["POST"])
def translate():
    data_json = request.json
    text = data_json.get("text")
    language = data_json.get("language")
    if not text or not language:
        return jsonify({"error": "Text or language missing"}), 400

    translated = translate_text(text, language)
    return jsonify({"translated": translated})