import datetime
from typing import Optional
from services import lat_long


def get_report(
    city: str, state: Optional[str], country: str = "US", units: str = "metric"
) -> dict:
    lat_long = lat_long.get_lat_long(city, state, country)

    lat = lat_long.results[0].geometry.lat
    long = lat_long.results[0].geometry.long

    current_date = datetime.now()
    date = current_date.strftime("%Y-%m-%d")
    key = "d9c6c158c8a553dd5f516ff9c9a75498"

    url = f"https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={long}&date={date}&appid={key}&units={units}"
