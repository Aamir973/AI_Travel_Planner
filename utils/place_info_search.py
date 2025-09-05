import requests
from langchain_tavily import TavilySearch

class GeoapifyPlaceSearchTool:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.places_url = "https://api.geoapify.com/v2/places"
        self.geocode_url = "https://api.geoapify.com/v1/geocode/search"

    def _geocode_place(self, place: str):
        """Convert place name into lat/lon using Geoapify Geocoding API"""
        params = {"text": place, "apiKey": self.api_key}
        try:
            response = requests.get(self.geocode_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            if data.get("features"):
                coords = data["features"][0]["geometry"]["coordinates"]  # [lon, lat]
                return coords[1], coords[0]  # return (lat, lon)
        except Exception as e:
            return None
        return None

    def _make_request(self, place: str, categories: str, radius: int = 5000, limit: int = 10):
        """Query Geoapify Places API with lat/lon + category"""
        coords = self._geocode_place(place)
        if not coords:
            return f"Could not geocode {place}"

        lat, lon = coords
        params = {
            "categories": categories,
            "filter": f"circle:{lon},{lat},{radius}",
            "limit": limit,
            "apiKey": self.api_key
        }
        try:
            response = requests.get(self.places_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = []
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                name = props.get("name", "Unnamed")
                address = props.get("formatted", "No address")
                results.append(f"{name} ({address})")
            return results if results else "No results found."
        except Exception as e:
            return f"Geoapify API error: {str(e)}"

    # ----------- Public methods -----------

    def geoapify_search_attractions(self, place: str):
        return self._make_request(place, categories="tourism.sights")

    def geoapify_search_restaurants(self, place: str):
        return self._make_request(place, categories="catering.restaurant")

    def geoapify_search_activity(self, place: str):
        return self._make_request(place, categories="entertainment")

    def geoapify_search_transportation(self, place: str):
        return self._make_request(place, categories="transport")

class TavilyPlaceSearchTool:
    def __init__(self):
        pass

    def tavily_search_attractions(self, place: str) -> dict:
        """
        Searches for attractions in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"top attractive places in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
    def tavily_search_restaurants(self, place: str) -> dict:
        """
        Searches for available restaurants in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"what are the top 10 restaurants and eateries in and around {place}."})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    
    def tavily_search_activity(self, place: str) -> dict:
        """
        Searches for popular activities in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"activities in and around {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result

    def tavily_search_transportation(self, place: str) -> dict:
        """
        Searches for available modes of transportation in the specified place using TavilySearch.
        """
        tavily_tool = TavilySearch(topic="general", include_answer="advanced")
        result = tavily_tool.invoke({"query": f"What are the different modes of transportations available in {place}"})
        if isinstance(result, dict) and result.get("answer"):
            return result["answer"]
        return result
    