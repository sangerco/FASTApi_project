import fastapi
from starlette.templating import Jinja2Templates

templates = Jinja2Templates("templates")

router = fastapi.APIRouter()


@router.get("/api/weather")
def weather():
    return "Some report."
