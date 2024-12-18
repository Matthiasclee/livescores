import json
import os
import urllib.request
from settings import *

TEAM_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/team/scores.php?team%5B%5D="
IMAGE_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/image/scores.php?team%5B%5D="

def get_data(team, data_source):
    if len(team) == 4:
        team = f"{get_setting('season')}-{team}"

    if data_source == "live scoreboard":
        try:
            team_json_data = urllib.request.urlopen(f"{TEAM_INFO_URL}{team}").read()
            all_team_json_data = urllib.request.urlopen(f"{TEAM_INFO_URL}").read()
            image_json_data = urllib.request.urlopen(f"{IMAGE_INFO_URL}{team}").read()
        except:
            return {"error": "Something went wrong getting data from the scoreboard"}

        if len(team_json_data + image_json_data) < 4:
            return {"error": "Scoreboard is not live at this time"}
    else:
        if not os.path.exists(f"score_archives/{data_source}") or not data_source in get_setting("valid_data_sources"):
            return {"error": "Invalid data source"}

        team_path = f"score_archives/{data_source}/{team}_team.json"
        all_teams_path = f"score_archives/{data_source}/teams_all.json"
        image_path = f"score_archives/{data_source}/{team}_image.json"

        if not os.path.exists(team_path) or not os.path.exists(image_path):
            return {"error": f"Team not found in data source {data_source}"}

        team_file = open(team_path)
        team_json_data = team_file.read()
        team_file.close()

        all_teams_file = open(all_teams_path)
        all_team_json_data = all_teams_file.read()
        all_teams_file.close()

        image_file = open(image_path)
        image_json_data = image_file.read()
        image_file.close()

    team_data = json.loads(team_json_data)["data"]
    all_team_data = json.loads(all_team_json_data)
    image_data = json.loads(image_json_data)["data"]

    if len(team_data) != 1:
        return {"error": "Team not found"}

    data = { "team": team_data[0], "image": image_data, "all_team_data": all_team_data, "error": False }

    return data
