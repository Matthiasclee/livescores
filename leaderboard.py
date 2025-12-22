from get_data import extract_team_image_data

def get_leaderboard(all_team_data, division, location, tier, as_together: bool = False, excluded_teams: list = [], all_image_data: list = {}, image: str = ""):
    excluded_teams_noseason = []
    for team in excluded_teams:
        excluded_teams_noseason.append(team.split("-")[-1])

    team_data = []
    for i, team in enumerate(all_team_data["data"]):
        if team['team_number'].split("-")[-1] in excluded_teams_noseason:
            continue

        if as_together and division == "ALL_AS":
            if team["division"].lower() in ["open", "middle school"]:
                continue
        else:
            if division != False and team["division"].lower() != division.lower():
                continue

        if location != False and team["location"].lower() != location.lower():
            continue

        if tier != False and "tier" in team and team["tier"].lower() != tier.lower():
            continue

        team_id = team["team_number"]

        if image != "":
            team_image = extract_team_image_data(team_id, image, all_image_data["all_image_data"])

            if team_image["error"]:
                continue

            team_image = team_image["image"]

            if team_image["ccs_score"] == "":
                continue

            score_inverse = 2000 - team_image["ccs_score"]
            time = team_image["duration"]
            warnings = team_image["code"]
        else:
            if "total" in team and team["total"] == "":
                score = 0.00
            elif "total" in team:
                score = float(team["total"])
            else:
                score = int(team["ccs_score"])

            score_inverse = 2000 - score
            time = team["score_time"]
            warnings = team["code"]

        team_data.append((f"{score_inverse}-{time}", team_id, i, team, warnings))

    team_data.sort()
    
    return team_data
