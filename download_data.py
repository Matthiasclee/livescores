# Import json, os, sys, and urllib libraries
import json
import os
import sys
import urllib.request

# Make an HTTP request with a User-Agent header
def make_request(url):
    req = Request(url)
    req.add_header("User-Agent", "LiveScores Discord bot scoreboard archive script - Contact: matthias@matthiasclee.com - https://github.com/Matthiasclee/livescores")
    return urlopen(req, timeout=5).read()

# Check if there is already a score archive path with the name passed in the first command line argument
if not os.path.exists(f"score_archives/{sys.argv[1]}"):
    # Make the directory for the score archive if there isn't
    os.makedirs(f"score_archives/{sys.argv[1]}")

# Define the score archive path
PATH = f"score_archives/{sys.argv[1]}"

# Define the scoreboard API URLs
TEAM_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/team/scores.php?team%5B%5D="
IMAGE_INFO_URL = "https://scoreboard.uscyberpatriot.org/api/image/scores.php?team%5B%5D="

# Get data from both URLs
# If the request is sent without a specified team, it just returns all the teams.
team_json_data = make_request(TEAM_INFO_URL)
image_json_data = make_request(IMAGE_INFO_URL)

# Write the entire teams and images JSON data to a file for calculating placement
# Open the file
file = open(f"{PATH}/teams_all.json", "wb")

# Write the data
file.write(team_json_data)

# Close the file
file.close()

# Open the file
file = open(f"{PATH}/images_all.json", "wb")

# Write the data
file.write(image_json_data)

# Close the file
file.close()

# Define an empty dictionary to store the team image information in
teams_image_info = {}

# Parse the JSON data from the scoreboard
team_data = json.loads(team_json_data)["data"]
image_data = json.loads(image_json_data)["data"]

# Makes a team JSON file for each team returned from the team info url
for team in team_data:
    # Open a file to write the JSON to
    file = open(f"{PATH}/{team['team_number']}_team.json", "w")

    # Convert the team information back to JSON, and write it to the file
    file.write(json.dumps({"data": [team]}))

    # Close the file
    file.close()

    # Make a blank image file for the team so the bot doesn't error if the team had no images
    file = open(f"{PATH}/{team['team_number']}_image.json", "w")

    # Write blank image data to the file
    file.write(json.dumps({"data": []}))

    # Close the file
    file.close()

# Sort the image data by team ID in the empty dictionary from earlier
for image in image_data:
    # Extract the team ID from the image data
    team_id = image["team_number"]

    # Create a blank list in the dictionary for the team if they're not already in the dict
    if not team_id in teams_image_info:
        teams_image_info[team_id] = []

    # Add the image data to the team's list in the dict
    teams_image_info[team_id].append(image)

# Write the image information from the dict to a file
for team_id, images in teams_image_info.items():
    # Open a JSON file
    file = open(f"{PATH}/{team_id}_image.json", "w")

    # Covnert the image data back to JSON and write it to the file, overwriting the blank file from earlier
    file.write(json.dumps({"data": images}))

    # Close the file
    file.close()
