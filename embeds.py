# Import the discord and datetime modules
import discord
from datetime import datetime

# Makes an embed with provided team data
# Arguments: - data: team score data - dict
#            - data_source: data source - str
# Returns: - embed: embed containing the scores
def make_team_embed(data, data_source):
    # Separate the team and image data from `data`
    team_data = data["team"]
    image_data = data["image"]

    # Create an embed where the title is the team number and the description is the location and division of the team, and the color is black (#000000)
    embed = discord.Embed(
        title = f"Team {team_data['team_number']}",
        description = f"Location: {team_data['location']}, Division: {team_data['division']}",
        color=0
    )

    # Format the team's play time and score time into a string for later
    time_data = f"Play Time: {team_data['play_time']}\n\
    Score Time: {team_data['score_time']}"

    # Format the team's score data into a string
    score_data = f"Total: {team_data['total']}\n\
    CCS Score: {team_data['ccs_score']}\n"

    # Add the cisco score to score_data if the team has a cisco score
    if "score_1" in team_data:
        score_data = score_data + f"Cisco Score: {team_data['score_1']}\n"

    # Add the team's adjustment to score_data
    score_data = score_data + f"Adjust: {team_data['adjustment']}"

    # Create a list for the team's warnings
    warnings_data = []

    # Iterate over each letter in the team's 'code' field, which contains its warnings
    for warning in list(team_data["code"]):
        # Add a time warning to warnings data if the warning is 'T'
        if warning == "T":
            warnings_data.append("* Time")
        # Add a multiple instances warning if the warning is 'M'
        elif warning == "M":
            warnings_data.append("* Multiple Instances")
        # If the warning is something else, just add the letter to the warnings data
        else:
            warnings_data.append(f"* `{warning}`")
        # Commented out code to add a cheating warning if there is a 'W'. This is commented because I don't know if the 'W' is actually a cheating warning.
        #elif warning == "W":
        #    warnings_data.append("* Cheaing warning")

    # Add a score field to the embed containing the score data string from earlier 
    embed.add_field(name="Score", value=score_data)

    # If the team's code field isn't empty (they have warnings), add a warnings field to the embed containing the elements in the
    # warnings_data list, joined by a newline to put them on separate lines.
    if team_data["code"] != "":
        embed.add_field(name="Warnings", value="\n".join(warnings_data))

    # Add a time field to the embed with the time data from earlier
    embed.add_field(name="Time", value=time_data)

    # Add a field titled Images (<images number>) to create a divider
    embed.add_field(name=f"__Images ({team_data['images']})__", value="", inline=False)

    # For each image, add an embed field containing the image name, score, found vulnerabilities, penalties, time, and warnings.
    for image in image_data:
        embed.add_field(
                name=f"{image['image']}: {image['ccs_score']} points",
                value=f"Found: {image['found']}/{image['found']+image['remaining']}, \
                        {image['penalties']} penalties, Total: {image['ccs_score']} points\nTime: {image['duration']}{(', Warnings: ' + image['code']) if image['code'] != '' else ''}",
                inline=False
                )
    
    # Add an embed field for the cisco score if present
    if "score_1" in team_data:
        embed.add_field(
                name=f"Cisco: {team_data['score_1']} points",
                value="",
                inline=False
                )

    # Add an embed footer containing the data source and current time
    embed.set_footer(text=f"Data from {data_source} | {datetime.now().strftime('%b %d %Y %I:%M %p')}")

    # Return the final embed
    return embed

# Make an embed for the datasource
# Arguments: - datasources (data sources list)
# Returns: embed containing formatted datasources
def make_datasources_embed(datasources):
    # Make an embed with the title "Data Sources" and no description
    embed = discord.Embed(
        title = f"Data Sources",
        description = f"",
        color=0
    )

    # For each data source, add an embed field containing the data source as the name, and no value
    for s in datasources:
        embed.add_field(name=s, value="", inline=False)

    # Return the embed
    return embed

# Make an error embed
# Arguments: - title: title - error name
#            - message: error message
# Returns: embed containing formatted error message
def make_error_embed(title, message):
    # Make an embed with the given title and message 
    embed = discord.Embed(
        title = title,
        description = message,
        color=0xea1c15
    )

    # Return the embed
    return embed
