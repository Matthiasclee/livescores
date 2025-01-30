import discord
import math
from datetime import datetime
from placement import *
from leaderboard import *

def make_team_embed(data, data_source):
    team_data = data["team"]
    image_data = data["image"]
    all_team_data = data["all_team_data"]

    if "score_1" in team_data and "score_2" in team_data and "score_3" in team_data:
        score_1_name = "Boeing"
        score_2_name = "Cisco"
        score_3_name = "Web"
    elif "score_1" in team_data and "score_2" in team_data:
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
                name=f"{image['image']}: {image['ccs_score']} point{'' if image['ccs_score'] in [1,'1'] else 's'}",
                value=f"Found: {image['found']}/{image['found']+image['remaining']}, \
{image['penalties']} penalt{'y' if image['penalties'] in [1,'1'] else 'ies'}, Total: {image['ccs_score']} point{'' if image['ccs_score'] in [1,'1'] else 's'}\nTime: {image['duration']}{(', Warnings: ' + image['code']) if image['code'] != '' else ''}",
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

    if "score_3" in team_data:
        embed.add_field(
                name=f"{score_3_name}: {team_data['score_3']} points",
                value="",
                inline=False
                )

    embed.set_footer(text=f"Data from {data_source} | {datetime.now().strftime('%b %d %Y %I:%M %p')}")

    return embed

def make_leaderboard_embed(data, data_source, division, location, tier, page, per_page, highlight_teams):
    highlight_teams = highlight_teams.split(" ")

    embed = discord.Embed(
        title = f"Leaderboard",
        description = f"Division: {division.title()}, Location: {location.upper()}, Tier: {tier.title()}",
        color=0
    )

    if division.lower() == "all":
        division = False
    if location.lower() == "all":
        location = False
    if tier.lower() == "all":
        tier = False

    start = per_page * (page - 1)
    end = start + per_page

    all_leaderboard_data = get_leaderboard(data["all_team_data"], division, location, tier)
    leaderboard_data = all_leaderboard_data[start:end]

    leaderboard_data_chunks = [[]]
    x = 0
    for i, team in enumerate(leaderboard_data):
        leaderboard_data_chunks[x].append(team)
        if (i+1) % 15 == 0:
            x += 1
            leaderboard_data_chunks.append([])

    initial_title = f"Page {page} of {math.ceil(len(all_leaderboard_data)/per_page)}, {per_page} teams per page"

    for j, leaderboard_data_chunk in enumerate(leaderboard_data_chunks):
        leaderboard_data_text = ""

        for i, team in enumerate(leaderboard_data_chunk):
            info, team_id, team_all_data = team
            score_inv, time = info.split("-")
            score = 2000 - float(score_inv)
            score = str(round(score, 2))

            team_location = team_all_data["location"]
            team_division = team_all_data["division"]
            team_warnings = team_all_data["code"]

            if "tier" in team_all_data and team_all_data["tier"] != "Middle School":
                tier_text = f" {team_all_data['tier']}"
            else:
                tier_text = ""

            if team_id in highlight_teams or team_id[3:7] in highlight_teams:
                t_id_mod_b = "__**"
                t_id_mod_e = ""
                ht_mod_e = "**__"
            else:
                t_id_mod_b = "**"
                t_id_mod_e = "**"
                ht_mod_e = ""

            leaderboard_data_text = leaderboard_data_text + f"{i + 1 + start + (j * 15)}. {t_id_mod_b}{team_id}{t_id_mod_e} ({team_location}{tier_text} {team_division}): {score}, {time}{ht_mod_e} **{team_warnings} **\n"

        embed.add_field(name=(initial_title if j == 0 else ""), value=leaderboard_data_text, inline=False)

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
