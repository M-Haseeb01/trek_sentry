import asyncio
from flask import Blueprint, request, jsonify, send_file
from io import BytesIO
from services.weather import fetch_city_data
from services.llm import generate_summary
from services.tts import synthesize

api = Blueprint("api", __name__)
CACHE = {}

@api.route("/analyze", methods=["POST"])
def analyze():
    city = request.json.get("city")
    country = request.json.get("country")
    key = f"{city}|{country}"

    if key not in CACHE:
        data = asyncio.run(fetch_city_data(city, country))
        if not data:
            return jsonify({"error": "City not found"}), 404

        summary = generate_summary(data)
        s1 = summary.split("@")

        text_to_speak = " ".join(part.strip() for part in s1 if part.strip())

        audio = synthesize(text_to_speak)

        CACHE[key] = {"summary": summary, "audio": audio}

    return jsonify({"summary": CACHE[key]["summary"]})

@api.route("/audio")
def audio():
    city = request.args.get("city")
    country = request.args.get("country")
    key = f"{city}|{country}"

    return send_file(
        BytesIO(CACHE[key]["audio"]),
        mimetype="audio/wav"
    )
