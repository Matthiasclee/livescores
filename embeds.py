import discord
from datetime import datetime
from placement import *

def make_team_embed(data, data_source):
    team_data = data["team"]
    image_data = data["image"]
    all_team_data = data["all_team_data"]

    if "score_1" in team_data and "score_2" in team_data:
        score_1_name = "Quiz"
        score_2_name = "Packet Tracer"
    elif "score_1" in team_data:
        score_1_name = "Cisco"

    if "total" not in team_data:
        total_score = 0
        
        if "ccs_score" in team_data:
            total_score += int(team_data["ccs_score"])
        if "score_1" in team_data:
            total_score += int(team_data["score_1"])
        if "score_2" in team_data:
            total_score += int(team_data["score_2"])

        team_data["total"] = str(total_score)


    tier_text = ""
    if "tier" in team_data:
        tier_text = f", Tier: {team_data['tier']}"

    embed = discord.Embed(
        title = f"Team {team_data['team_number']}",
        description = f"Location: {team_data['location']}, Division: {team_data['division']}{tier_text}",
        color=0
    )

    if data_source == "live scoreboard":
        embed.url = f"https://scoreboard.uscyberpatriot.org/team.php?team={team_data['team_number']}"

    time_data = f"Play Time: {team_data['play_time']}\n\
Score Time: {team_data['score_time']}"

    score_data = f"Total: {team_data['total']}\n\
CCS Score: {team_data['ccs_score']}\n"

    if "score_1" in team_data:
        score_data = score_data + f"{score_1_name}: {team_data['score_1']}\n"

    if "score_2" in team_data:
        score_data = score_data + f"{score_2_name}: {team_data['score_2']}\n"

    if "adjustment" in team_data:
        score_data = score_data + f"Adjust: {team_data['adjustment']}"
    else:
        score_data = score_data + "Adjust: 0.00"

    warnings_data = []

    for warning in list(team_data["code"]):
        if warning == "T":
            warnings_data.append("* Time")
        elif warning == "M":
            warnings_data.append("* Multiple Instances")
        elif warning == "W":
            warnings_data.append("* Score Withdrawn")
        else:
            warnings_data.append(f"* `{warning}`")

    embed.add_field(name="Score", value=score_data)

    if team_data["code"] != "":
        embed.add_field(name="Warnings", value="\n".join(warnings_data))

    embed.add_field(name="Time", value=time_data)

    overall_placement = determine_team_placement(team_data, all_team_data, [])
    overall_division = determine_team_placement(team_data, all_team_data, ["division"])
    overall_tier = determine_team_placement(team_data, all_team_data, ["tier"])
    overall_division_tier = determine_team_placement(team_data, all_team_data, ["division", "tier"])

    state_placement = determine_team_placement(team_data, all_team_data, ["state"])
    state_division = determine_team_placement(team_data, all_team_data, ["division", "state"])
    state_tier = determine_team_placement(team_data, all_team_data, ["tier", "state"])
    state_division_tier = determine_team_placement(team_data, all_team_data, ["division", "tier", "state"])

    if "tier" in team_data: 
        overall_placement_text = f"Overall: {overall_placement[0]}/{overall_placement[1]}, {overall_placement[2]}%\n\
Div, Tier: {overall_division_tier[0]}/{overall_division_tier[1]}, {overall_division_tier[2]}%\n\
Division: {overall_division[0]}/{overall_division[1]}, {overall_division[2]}%\n\
Tier: {overall_tier[0]}/{overall_tier[1]}, {overall_tier[2]}%"

        state_placement_text = f"Overall: {state_placement[0]}/{state_placement[1]}, {state_placement[2]}%\n\
Div, Tier: {state_division_tier[0]}/{state_division_tier[1]}, {state_division_tier[2]}%\n\
Division: {state_division[0]}/{state_division[1]}, {state_division[2]}%\n\
Tier: {state_tier[0]}/{state_tier[1]}, {state_tier[2]}%"
    else:
        overall_placement_text = f"Overall: {overall_placement[0]}/{overall_placement[1]}, {overall_placement[2]}%\n\
Division: {overall_division[0]}/{overall_division[1]}, {overall_division[2]}%"

        state_placement_text = f"Overall: {state_placement[0]}/{state_placement[1]}, {state_placement[2]}%\n\
Division: {state_division[0]}/{state_division[1]}, {state_division[2]}%"


    embed.add_field(name="__Placement__", value="", inline=False)
    embed.add_field(name = "National", value = overall_placement_text)
    embed.add_field(name = "State", value = state_placement_text)

    embed.add_field(name=f"__Images ({team_data['images']})__", value="", inline=False)

    for image in image_data:
        embed.add_field(
                name=f"{image['image']}: {image['ccs_score']} points",
                value=f"Found: {image['found']}/{image['found']+image['remaining']}, \
{image['penalties']} penalties, Total: {image['ccs_score']} points\nTime: {image['duration']}{(', Warnings: ' + image['code']) if image['code'] != '' else ''}",
                inline=False
                )

    if "score_1"  in team_data or "score_2" in team_data:
        embed.add_field(name = "__Other__", value = "", inline = False)
    
    if "score_1" in team_data:
        embed.add_field(
                name=f"{score_1_name}: {team_data['score_1']} points",
                value="",
                inline=False
                )

    if "score_2" in team_data:
        embed.add_field(
                name=f"{score_2_name}: {team_data['score_2']} points",
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
