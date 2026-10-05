import requests
from typing import List, Dict, Any

class OddsAPIService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.the-odds-api.com/v4/sports"

    def get_basketball_leagues(self) -> List[Dict[str, Any]]:
        """Fetches active basketball leagues from The Odds API."""
        url = f"{self.base_url}?apiKey={self.api_key}"
        res = requests.get(url)
        if res.status_code != 200:
            return []
        sports = res.json()
        return [s for s in sports if "basketball" in s.get("group", "").lower()]

    def get_odds(self, sport_key: str, regions: str = "eu,us", markets: str = "h2h,totals") -> List[Dict[str, Any]]:
        """Fetches pre-match and live odds for a specific league."""
        url = f"{self.base_url}/{sport_key}/odds/?apiKey={self.api_key}&regions={regions}&markets={markets}"
        res = requests.get(url)
        if res.status_code == 200:
            return res.json()
        return []