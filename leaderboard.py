def get_leaderboard(all_team_data, division, location, tier, as_together: bool = False, excluded_teams: list = []):
    excluded_teams_noseason = []
    for team in excluded_teams:
        excluded_teams_noseason.append(team.split("-")[-1])

    team_data = []
    for team in all_team_data["data"]:
        if team['team_number'].split("-")[-1] in excluded_teams_noseason:
            continue

        if as_together and division == "ALL_AS":
            if not team["division"].lower() in ["open", "middle school"]:
                continue
        else:
            if division != False and team["division"].lower() != division.lower():
                continue

        if location != False and team["location"].lower() != location.lower():
            continue

        if tier != False and "tier" in team and team["tier"].lower() != tier.lower():
            continue

        if "total" in team and team["total"] == "":
            score = 0.00
        elif "total" in team:
            score = float(team["total"])
        else:
            score = int(team["ccs_score"])
        score_inverse = 2000 - score
        time = team["play_time"]
        team_id = team["team_number"]

        team_data.append((f"{score_inverse}-{time}", team_id, team))

    team_data.sort()
    
    return team_data
