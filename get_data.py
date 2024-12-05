# Import the json, os, urllib, and settings
import json
import os
import urllib.request
from settings import *

# Define the URLs for getting team info and image info from the API
TEAM_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/team/scores.php?team%5B%5D="
IMAGE_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/image/scores.php?team%5B%5D="

# Get team data from a source
# Arguments: - team: team ID
#            - data_source: source to get data from, set to "live scoreboard" to get live data from the API
# Returns: dictionary of team and image data, or any errors that may have occured
def get_data(team, data_source):
    # Automatically add the season from settings if the user only send the 4 digit team number
    if len(team) == 4:
        team = f"{get_setting('season')}-{team}"

    # Get live data if the data source is "live scoreboard"
    if data_source == "live scoreboard":
        # Get team info from the team info API
        team_json_data = urllib.request.urlopen(f"{TEAM_INFO_URL}{team}").read()
        # Get image info from the image info API
        image_json_data = urllib.request.urlopen(f"{IMAGE_INFO_URL}{team}").read()
    # Get historical data
    else:
        # Check if the data source exists and is valid according to the "valid_data_sources" setting
        if not os.path.exists(f"score_archives/{data_source}") or not data_source in get_setting("valid_data_sources"):
            # Return an error if so
            return {"error": "Invalid data source"}

        # Set the file paths of the team and image json files
        team_path = f"score_archives/{data_source}/{team}_team.json"
        image_path = f"score_archives/{data_source}/{team}_image.json"

        # Check if the team exists (if both of the files above exist)
        if not os.path.exists(team_path) or not os.path.exists(image_path):
            # Return an error if not
            return {"error": f"Team not found in data source {data_source}"}

        # Read the files
        team_file = open(team_path)
        team_json_data = team_file.read()
        team_file.close()

        image_file = open(image_path)
        image_json_data = image_file.read()
        image_file.close()

    # Use json to parse the data and extract the "data" element
    team_data = json.loads(team_json_data)["data"]
    image_data = json.loads(image_json_data)["data"]

    # Check if team_data contains more than one element (it will if the team doesn't exist on the live scoreboard)
    if len(team_data) != 1:
        # Return an error if so
        return {"error": "Team not found"}

    # Put all the data in a dict to return
    data = { "team": team_data[0], "image": image_data, "error": False }

    # Return the data
    return data
