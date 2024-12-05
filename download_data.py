import json
import os
import sys
import urllib.request

if not os.path.exists(f"score_archives/{sys.argv[1]}"):
    os.makedirs(f"score_archives/{sys.argv[1]}")

PATH = f"score_archives/{sys.argv[1]}"

TEAM_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/team/scores.php?team%5B%5D="
IMAGE_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/image/scores.php?team%5B%5D="

team_json_data = urllib.request.urlopen(TEAM_INFO_URL).read()
image_json_data = urllib.request.urlopen(IMAGE_INFO_URL).read()

teams_image_info = {}

team_data = json.loads(team_json_data)["data"]
image_data = json.loads(image_json_data)["data"]

for team in team_data:
    file = open(f"{PATH}/{team['team_number']}_team.json", "w")
    file.write(json.dumps({"data": [team]}))
    file.close()

    # Make a blank image file for the team so the bot doesn't error if the team had to images
    file = open(f"{PATH}/{team['team_number']}_image.json", "w")
    file.write(json.dumps({"data": []}))
    file.close()

for image in image_data:
    team_id = image["team_number"]

    if not team_id in teams_image_info:
        teams_image_info[team_id] = []

    teams_image_info[team_id].append(image)

for team_id, images in teams_image_info.items():
    file = open(f"{PATH}/{team_id}_image.json", "w")
    file.write(json.dumps({"data": images}))
    file.close()
