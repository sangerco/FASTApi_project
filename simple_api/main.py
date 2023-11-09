from typing import Optional
import fastapi
import uvicorn

api = fastapi.FastAPI()


@api.get("/")
def index():
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to the API</h1>"
        "<div>"
        "Try it: <a href='/api/calculate?x=7&y=4'>/api/calculate?x=7&y=4</a>"
        "</div>"
        "</body>"
        "</html>"
    )

    return fastapi.responses.HTMLResponse(content=body)


@api.get("/api/calculate")
def calculate(x: int, y: int, z: Optional[int] = None):
    if z == 0:
        return fastapi.responses.JSONResponse(
            content={"error": "Error: z cannot be 0"}, status_code=400
        )

    value = x + y

    if z is not None:
        value /= z

    return {"x": x, "y": y, "z": z, "value": value}


uvicorn.run(api)
