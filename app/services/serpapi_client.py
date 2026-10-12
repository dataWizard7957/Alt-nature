import requests
from app.config import settings

def fetch_local_weather(location: str) -> dict:
    if not settings.SERPAPI_API_KEY:
        return {
            "temperature": "18°C",
            "condition": "Crisp Autumn Breeze",
            "uv_index": "Low (2)",
            "foliage_status": "Peak Autumn Color"
        }
    
    url = "https://serpapi.com/search.json"
    params = {
        "engine": "google",
        "q": f"weather in {location}",
        "api_key": settings.SERPAPI_API_KEY
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        weather = data.get("weather", {})
        return {
            "temperature": weather.get("temperature", "18°C"),
            "condition": weather.get("condition", "Clear"),
            "uv_index": "Low (2)",
            "foliage_status": "Peak Autumn Color"
        }
    except Exception as e:
        print(f"SerpApi fetch error: {e}")
        return {
            "temperature": "18°C",
            "condition": "Outdoor Fall Conditions",
            "uv_index": "2",
            "foliage_status": "Vibrant foliage active"
        }
