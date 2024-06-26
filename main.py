# Built-ins

# Downloaded
import requests

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse

# Project
from stats_gather import data_pickup

# Disabling the default routes
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, swagger_ui_oauth2_redirect_url=None)

app.mount("/style", StaticFiles(directory="./assets/stylesheet"), name="style")
app.mount("/images", StaticFiles(directory="./assets/images"), name="images")
app.mount("/font", StaticFiles(directory="./assets/font"), name="font")
app.mount("/video", StaticFiles(directory="./assets/video"), name="video")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/{name}")
async def wrong_scheme(request: Request, name: str):
    return templates.TemplateResponse("home.html",
                                      {"request": request,
                                       "message": f"To view a player's profile, use the search bar or go to /p/{name}"})


@app.get("/p/{name}")
async def stats(request: Request, name: str):
    player_data = requests.get(f"https://playerdb.co/api/player/minecraft/{name}")
    # If this Minecraft account doesn't exist → 404 Not Found
    if not player_data.ok:
        return RedirectResponse(url="/")

    player_data = player_data.json()
    _uuid: str = player_data["data"]["player"]["id"]

    skin_link: str = f"https://crafthead.net/avatar/{_uuid}/256"

    p = data_pickup.Profile(uuid=_uuid)
    result = p.gather_stats()  # Send API request to Hypixel to fetch the player's stats

    if not result:
        return RedirectResponse(url="/")

    try:
        slayer_data = p.get_slayer_data()
    except Exception:
        slayer_data = None
    try:
        leveling_data = p.get_leveling_data()
    except Exception:
        leveling_data = None
    try:
        rift_data = p.get_rift_data()
    except Exception:
        rift_data = None
    try:
        misc_data = p.get_misc_stats()
    except Exception:
        misc_data = None

    trophy_data = p.get_trophy_stats()

    return templates.TemplateResponse("stats.html",
                                      {"request": request,
                                       "player_name": name, "player_uuid": _uuid, "skin_link": skin_link,
                                       "leveling_data": leveling_data,
                                       "slayer_data": slayer_data,
                                       "rift_data": rift_data,
                                       "misc_data": misc_data,
                                       "trophy_data": trophy_data
                                       })
