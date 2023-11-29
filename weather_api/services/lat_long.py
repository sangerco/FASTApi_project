from typing import Optional

import httpx

lat_long_api_key: Optional[str] = None


async def get_lat_long_async(
    city: str, state: Optional[str], country: str = "US"
) -> dict:
    if state:
        q = f"{city}, {state}, {country}"
    else:
        q = f"{city}, {country}"
    key = lat_long_api_key

    url = f"https://api.opencagedata.com/geocode/v1/json?q={q}&key={key}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

    data = resp.json()
    location = data["results"]
    # print(location)
    return location
