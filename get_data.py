import json
import urllib.request
from settings import *

TEAM_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/team/scores.php?team%5B%5D="
IMAGE_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/image/scores.php?team%5B%5D="

def get_data(team, data_source):
    if len(team) == 4:
        team = f"{get_setting('season')}-{team}"

    if data_source == "live scoreboard":
        team_json_data = urllib.request.urlopen(f"{TEAM_INFO_URL}{team}").read()
        image_json_data = urllib.request.urlopen(f"{IMAGE_INFO_URL}{team}").read()
    else:
        team_file = open(f"score_archives/{data_source}/{team}_team.json")
        team_json_data = team_file.read()
        team_file.close()

        image_file = open(f"score_archives/{data_source}/{team}_image.json")
        image_json_data = image_file.read()
        image_file.close()

    team_data = json.loads(team_json_data)["data"]
    image_data = json.loads(image_json_data)["data"]

    if len(team_data) != 1:
        return {"error": "Team Not Found"}

    data = { "team": team_data[0], "image": image_data, "error": False }

    return data
