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

    def get_leagues_by_country(self) -> Dict[str, List[Dict[str, Any]]]:
        """Groups basketball leagues by country."""
        leagues = self.get_basketball_leagues()
        
        country_mapping = {
            "USA": ["nba", "wnba", "ncaab", "ncaaw"],
            "Europe": ["euroleague", "eurocup"],
            "Spain": ["acb"],
            "Germany": ["bbl"],
            "France": ["lnb"],
            "Italy": ["lega-basket-serie-a"],
            "Greece": ["greek-basket-league"],
            "Turkey": ["bsl"],
            "Russia": ["vbl"],
            "China": ["cba"],
            "Australia": ["nbl"],
            "Argentina": ["lnb"],
            "Brazil": ["nbb"],
            "Lithuania": ["lkl"],
            "Israel": ["winner-league"],
            "Poland": ["plk"],
            "Serbia": ["kls"],
            "Croatia": ["aba-liga"],
            "International": ["fiba-world-cup", "fiba-olympic-qualifying"]
        }
        
        grouped = {}
        for league in leagues:
            key = league.get('key', '')
            title = league.get('title', '')
            
            matched_country = None
            for country, keywords in country_mapping.items():
                if any(kw in key.lower() for kw in keywords):
                    matched_country = country
                    break
            
            if not matched_country:
                if "NBA" in title:
                    matched_country = "USA"
                elif "Euro" in title:
                    matched_country = "Europe"
                else:
                    matched_country = "Other"
            
            if matched_country not in grouped:
                grouped[matched_country] = []
            grouped[matched_country].append(league)
        
        return grouped