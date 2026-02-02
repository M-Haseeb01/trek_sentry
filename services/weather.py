import aiohttp

async def fetch_city_data(city, country):
    """
    Fetches weather, AQI, earthquake, and basic traffic info for a city.
    Returns a dict with all relevant data.
    """
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:

        # ---------------- GEOLOCATION ----------------
        geo_resp = await session.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "country": country, "count": 1}
        )
        geo_data = await geo_resp.json()
        if not geo_data.get("results"):
            return None

        loc = geo_data["results"][0]
        lat, lon = loc["latitude"], loc["longitude"]

        # ---------------- WEATHER ----------------
        weather_resp = await session.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current_weather": "true",
                "hourly": "precipitation,weathercode"
            }
        )
        weather_data = await weather_resp.json()
        current_weather = weather_data.get("current_weather", {})

        hourly_precip = weather_data.get("hourly", {}).get("precipitation", [])
        hourly_codes = weather_data.get("hourly", {}).get("weathercode", [])

        storm_alert = "No severe storm expected"
        flood_alert = "No flood risk detected"

        if hourly_precip and max(hourly_precip) > 10:
            storm_alert = "Heavy rain / possible storm soon"
        if hourly_precip and any(p > 20 for p in hourly_precip[:12]):
            flood_alert = "Flood risk possible in next hours"
        if hourly_codes and any(code >= 80 for code in hourly_codes[:12]):
            storm_alert = "Severe weather warning: storm / thunderstorm"

        # ---------------- AIR QUALITY ----------------
        aqi_resp = await session.get(
            "https://air-quality-api.open-meteo.com/v1/air-quality",
            params={"latitude": lat, "longitude": lon, "current": "us_aqi"}
        )
        aqi_data = await aqi_resp.json()
        aqi_value = aqi_data.get("current", {}).get("us_aqi", "N/A")

        # ---------------- EARTHQUAKES ----------------
        eq_resp = await session.get(
            "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
        )
        eq_data = await eq_resp.json()
        earthquakes = [f["properties"]["place"] for f in eq_data.get("features", [])[:3]]

        # ---------------- TRAFFIC ----------------
        try:
            from services.traffic import get_live_traffic
            traffic_info = get_live_traffic(city)
        except:
            traffic_info = "Traffic info not available"

        return {
            "location": f"{city}, {country}",
            "weather": current_weather,
            "storm_alert": storm_alert,
            "flood_alert": flood_alert,
            "aqi": aqi_value,
            "recent_earthquakes": earthquakes,
            "traffic": traffic_info
        }
