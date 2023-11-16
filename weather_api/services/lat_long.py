from typing import Optional
from secret import api_key


def get_lat_long(city: str, state: Optional[str], country: str = "US") -> dict:
    q = f"{city}, {state}, {country}"
    key = api_key

    url = f"https://api.opencagedata.com/geocode/v1/json?={q}"
