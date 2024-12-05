import discord
from datetime import datetime

def make_team_embed(data, data_source):
    team_data = data["team"]
    image_data = data["image"]

    embed = discord.Embed(
        title = f"Team {team_data['team_number']}",
        description = f"Location: {team_data['location']}, Division: {team_data['division']}",
        color=0
    )

    time_data = f"Play Time: {team_data['play_time']}\n\
    Score Time: {team_data['score_time']}"

    score_data = f"Total: {team_data['total']}\n\
    CCS Score: {team_data['ccs_score']}\n"

    if "score_1" in team_data:
        score_data = score_data + f"Cisco Score: {team_data['score_1']}\n"

    score_data = score_data + f"Adjust: {team_data['adjustment']}"

    warnings_data = []
    for warning in list(team_data["code"]):
        if warning == "T":
            warnings_data.append("* Time")
        elif warning == "M":
            warnings_data.append("* Multiple Instances")
        else:
            warnings_data.append(f"* `{warning}`")
        #elif warning == "W":
        #    warnings_data.append("* Cheaing warning")

    embed.add_field(name="Score", value=score_data)
    if team_data["code"] != "":
        embed.add_field(name="Warnings", value="\n".join(warnings_data))
    embed.add_field(name="Time", value=time_data)

    embed.add_field(name=f"__Images ({team_data['images']})__", value="", inline=False)

    for image in image_data:
        embed.add_field(
                name=f"{image['image']}: {image['ccs_score']} points",
                value=f"Found: {image['found']}/{image['found']+image['remaining']}, \
                        {image['penalties']} penalties, Total: {image['ccs_score']} **{image['code']} **",
                inline=False
                )
    if "score_1" in team_data:
        embed.add_field(
                name=f"Cisco: {team_data['score_1']} points",
                value="",
                inline=False
                )

    embed.set_footer(text=f"Data from {data_source} | {datetime.now().strftime('%b %d %Y %I:%M %p')}")

    return embed

def make_datasources_embed(datasources):
    embed = discord.Embed(
        title = f"Data Sources",
        description = f"",
        color=0
    )

    for s in datasources:
        embed.add_field(name=s, value="", inline=False)

    return embed


def make_error_embed(title, message):
    embed = discord.Embed(
        title = title,
        description = message,
        color=0xea1c15
    )

    return embed
