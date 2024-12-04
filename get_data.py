import json
import urllib.request

DATA_SOURCE = 1 # 0: file, 1: website
TEAM_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/team/scores.php?team%5B%5D="
IMAGE_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/image/scores.php?team%5B%5D="

def get_data(team):
    if DATA_SOURCE == 0:
        team_file = open(f"score_archives/{team}_team.json")
        team_json_data = team_file.read()
        team_file.close()

        image_file = open(f"score_archives/{team}_image.json")
        image_json_data = image_file.read()
        image_file.close()
    elif DATA_SOURCE == 1:
        team_json_data = urllib.request.urlopen(f"{TEAM_INFO_URL}{team}").read()
        image_json_data = urllib.request.urlopen(f"{IMAGE_INFO_URL}{team}").read()

    team_data = json.loads(team_json_data)["data"][0]
    image_data = json.loads(image_json_data)["data"]

    data = { "team": team_data, "image": image_data }

    return data
