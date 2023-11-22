from datetime import datetime
from typing import Optional
from services import lat_long
import httpx

weather_api_key: Optional[str] = None


async def get_report_async(
    city: str, state: Optional[str], country: str = "US", units: str = "metric"
) -> dict:
    if state:
        location_result = await lat_long.get_lat_long_async(city, state, country)
    else:
        location_result = await lat_long.get_lat_long_async(city, country)

    lat = location_result[0]["geometry"]["lat"]
    long = location_result[0]["geometry"]["lng"]

    current_date = datetime.now()
    date = current_date.strftime("%Y-%m-%d")

    url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={long}&date={date}&appid={weather_api_key}&units={units}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()

    data = resp.json()

    return data
