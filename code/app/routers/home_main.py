from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

router = APIRouter()
templates = Jinja2Templates(directory=BASE_DIR / "pages")


@router.post("/main", response_class=HTMLResponse)
async def read_home(request: Request):
    return templates.TemplateResponse("./main.html", {"request": request, "title": "main"})
