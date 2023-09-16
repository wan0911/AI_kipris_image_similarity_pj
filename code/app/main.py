from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path

# routers
from .routers import home
from .routers import home_main

# mongo
from .database import mongodb


app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent  # app
STATIC_DIR = Path(__file__).resolve().parent / "static"  # static


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)

templates = Jinja2Templates(directory=BASE_DIR / "pages")


# Routers
app.include_router(home.router)
app.include_router(home_main.router)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("./home.html", {"request": request, "title": "home"})


# mongo 이벤트
@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    mongodb.close()
