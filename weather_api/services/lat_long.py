from typing import Optional


def get_lat_long(city: str, state: Optional[str], country: str = "US") -> dict:
    q = f"{city}, {state}, {country}"
    key = "c3478b985b67412db8f6ee7de66c7228"

    url = f"https://api.opencagedata.com/geocode/v1/json?={q}"
