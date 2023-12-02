from datetime import datetime
from typing import Optional, Tuple
from models.validation_error import ValidationError
from services import lat_long
from infrastructure import weather_cache
import httpx

weather_api_key: Optional[str] = None


async def get_report_async(
    city: str, state: Optional[str], country: str = "US", units: str = "imperial"
) -> dict:
    city, state, country, units = validate_units(city, state, country, units)

    temps = weather_cache.get_weather(city, state, country, units)
    if temps:
        return temps
    if state:
        location_result = await lat_long.get_lat_long_async(city, state, country)
    else:
        location_result = await lat_long.get_lat_long_async(city, country)

    lat = location_result[0]["geometry"]["lat"]
    long = location_result[0]["geometry"]["lng"]

    current_date = datetime.now()
    date = current_date.strftime("%Y-%m-%d")

    url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={long}&date={date}&appid={weather_api_key}&units={units}"

    print(url)

    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        if resp.status_code != 200:
            raise ValidationError(resp.text, status_code=resp.status_code)

    data = resp.json()
    temps = data["temperature"]
    weather_cache.set_weather(city, state, country, units, temps)

    return temps


def validate_units(
    city: str, state: Optional[str], country: Optional[str], units: str
) -> Tuple[str, Optional[str], str, str]:
    city = city.lower().strip()
    if not country:
        country = "us"
    else:
        country = country.lower().strip()

    if len(country) != 2:
        error = f"Invalid country: {country}. It must be a two letter abbreviation such as US or GB."
        raise ValidationError(status_code=400, error_msg=error)

    if state:
        state = state.strip().lower()

    if state and len(state) != 2:
        error = f"Invalid state: {state}. It must be a two letter abbreviation such as CA or KS."
        raise ValidationError(status_code=400, error_msg=error)

    if units:
        units.strip().lower()

    valid_units = {"standard", "metric", "imperial"}
    if units not in valid_units:
        error = f"Invalid units '{units}, it must be one of {valid_units}."
        raise ValidationError(status_code=400, error_msg=error)

    return city, state, country, units
