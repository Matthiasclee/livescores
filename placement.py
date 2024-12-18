def determine_team_placement(team_info, all_team_data, scopes):
    team_info = team_info["data"][0]
    team_data = []
    for team in all_team_data["data"]:
        if "division" in scopes and team["division"] != team_info["division"]:
            next

        if "state" in scopes and team["location"] != team_info["location"]:
            next

        if "tier" in scopes and "tier" in team and "tier" in team_info and team["tier"] != team_info["tier"]:
            next

        if "total" in team and team["total"] == "":
            score = 0.00
        elif "total" in team:
            print(team["team_number"])
            score = float(team["total"])
        else:
            score = int(team["ccs_score"])
        score_inverse = 2000 - score
        time = team["play_time"]
        team_id = team["team_number"]

        team_data.append((f"{score_inverse}-{time}", team_id))

    team_data.sort()

    for i, score_data in enumerate(team_data):
        if score_data[1] == team_info["team_number"]:
            return (i+1)
    return 0
