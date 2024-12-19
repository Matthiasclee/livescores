def get_leaderboard(all_team_data, division, location, tier):
    team_data = []
    for team in all_team_data["data"]:
        if division != False and team["division"] != division:
            continue

        if location != False and team["location"] != location:
            continue

        if tier != False and "tier" in team and team["tier"] != tier:
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

        team_data.append((f"{score_inverse}-{time}", team_id))

    team_data.sort()
    
    return team_data
