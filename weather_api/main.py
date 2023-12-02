import asyncio
import json
from pathlib import Path
import fastapi
import uvicorn
from starlette.templating import Jinja2Templates
from starlette.requests import Request
from starlette.staticfiles import StaticFiles

from api import weather_api
from services import openweather_service
from services import lat_long
from services import report_service
from views import home
from models.location import Location

api = fastapi.FastAPI()


def configure():
    configure_routing()
    configure_api_keys()
    configure_fake_data()


def configure_api_keys():
    file = Path("settings.json").absolute()
    if not file.exists():
        print(
            f"WARNING: {file} file not found, you cannot continue, please see settings_template.json"
        )
        raise Exception(
            "settings.json file not found, you cannot continue, please see settings_template.json"
        )

    with open("settings.json") as fin:
        settings = json.load(fin)
        openweather_service.weather_api_key = settings.get("weather_api_key")
        lat_long.lat_long_api_key = settings.get("lat_long_api_key")


def configure_routing():
    api.mount("/static", StaticFiles(directory="static"), name="static")
    api.include_router(home.router)
    api.include_router(weather_api.router)


def configure_fake_data():
    # This was added to make it easier to test the weather event reporting
    # We have /api/reports but until you submit the new data each run, it's missing
    # So this will give us something to start from
    loc = Location(city="Denver", state="CO", country="US")
    asyncio.run(report_service.add_report("Blizzard this morning", location=loc))
    asyncio.run(report_service.add_report("Windy this afternoon", location=loc))


if __name__ == "__main__":
    configure()
    uvicorn.run(api, port=8000, host="127.0.0.1")
else:
    configure()
