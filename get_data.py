import json
import os
from urllib.request import Request, urlopen
from settings import *

TEAM_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/team/scores.php?team%5B%5D="
IMAGE_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/image/scores.php?team%5B%5D="

def make_request(url):
    req = Request(url)
    req.add_header("User-Agent", "LiveScores Discord bot - https://github.com/Matthiasclee/livescores - Contact: " + get_secret("contact_info"))
    return urlopen(req, timeout=5).read()

def get_all_team_data(data_source):
    if data_source == "live scoreboard":
        try:
            all_team_json_data = make_request(f"{TEAM_INFO_URL}")
        except:
            return {"error": "Something went wrong getting data from the scoreboard"}

        if len(all_team_json_data) < 4:
            return {"error": "Scoreboard is not live at this time. Try specifying a historical data source from `/datasources`."}
    else:
        if not os.path.exists(f"score_archives/{data_source}") or not (data_source in get_setting("valid_data_sources") or data_source in get_setting("additional_data_sources")):
            return {"error": "Invalid data source"}

        all_teams_path = f"score_archives/{data_source}/teams_all.json"

        all_teams_file = open(all_teams_path)
        all_team_json_data = all_teams_file.read()
        all_teams_file.close()

    all_team_data = json.loads(all_team_json_data)

    return { "all_team_data": all_team_data, "error": False }

def get_all_image_data(data_source):
    if data_source == "live scoreboard":
        try:
            all_image_json_data = make_request(f"{IMAGE_INFO_URL}")
        except:
            return {"error": "Something went wrong getting data from the scoreboard"}

        if len(all_image_json_data) < 4:
            return {"error": "Scoreboard is not live at this time. Try specifying a historical data source from `/datasources`."}
    else:
        if not os.path.exists(f"score_archives/{data_source}") or not (data_source in get_setting("valid_data_sources") or data_source in get_setting("additional_data_sources")):
            return {"error": "Invalid data source"}

        all_images_path = f"score_archives/{data_source}/images_all.json"

        all_images_file = open(all_images_path)
        all_image_json_data = all_images_file.read()
        all_images_file.close()

    all_image_data = json.loads(all_image_json_data)

    return { "all_image_data": all_image_data, "error": False }

def extract_team_image_data(team, image, all_image_data):
    if len(team) == 4 and not data_source == "live scoreboard":
        team = f"{data_source[2:4]}-{team}"
    elif len(team) == 4:
        team = f"{get_setting('season')}-{team}"

    image = [d for d in all_image_data["data"] if d['team_number'] == team and d['image'] == image]

    if len(image) == 0:
        return {"error": f"Team and image not found in specified data source"}
    else:
        return {"image": image[0], "error": False}

def get_data(team, data_source):
    if len(team) == 4 and not data_source == "live scoreboard":
        team = f"{data_source[2:4]}-{team}"
    elif len(team) == 4:
        team = f"{get_setting('season')}-{team}"

    if data_source == "live scoreboard":
        try:
            team_json_data = make_request(f"{TEAM_INFO_URL}{team}")
            image_json_data = make_request(f"{IMAGE_INFO_URL}{team}")
        except:
            return {"error": "Something went wrong getting data from the scoreboard"}

        if len(team_json_data + image_json_data) < 4:
            return {"error": "Scoreboard is not live at this time. Try specifying a historical data source from `/datasources`."}
    else:
        if not os.path.exists(f"score_archives/{data_source}") or not (data_source in get_setting("valid_data_sources") or data_source in get_setting("additional_data_sources")):
            return {"error": "Invalid data source"}

        team_path = f"score_archives/{data_source}/{team}_team.json"
        image_path = f"score_archives/{data_source}/{team}_image.json"

        if not os.path.exists(team_path) or not os.path.exists(image_path):
            return {"error": f"Team not found in data source {data_source}"}

        team_file = open(team_path)
        team_json_data = team_file.read()
        team_file.close()

        image_file = open(image_path)
        image_json_data = image_file.read()
        image_file.close()

    team_data = json.loads(team_json_data)["data"]
    image_data = json.loads(image_json_data)["data"]

    if len(team_data) != 1:
        return {"error": "Team not found. Try specifying a data source from `/datasources`."}

    if "location" not in team_data[0]:
        team_data[0]["location"] = "N/A"

    if "division" not in team_data[0]:
        team_data[0]["division"] = "N/A"

    all_team_data = get_all_team_data(data_source)
    if all_team_data["error"]:
        return { "error": all_team_data["error"] }

    data = { "team": team_data[0], "image": image_data, "all_team_data": all_team_data["all_team_data"], "error": False }

    return data
