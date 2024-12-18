def determine_team_placement(team_info, all_team_data, scopes):
    #team_info = team_info["data"][0]
    team_data = []
    for team in all_team_data["data"]:
        if "division" in scopes and team["division"] != team_info["division"]:
            continue

        if "state" in scopes and team["location"] != team_info["location"]:
            continue

        if "tier" in scopes and "tier" in team and "tier" in team_info and team["tier"] != team_info["tier"]:
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

    for i, score_data in enumerate(team_data):
        if score_data[1] == team_info["team_number"]:
            place = i+1
            length = len(team_data)
            percentile = int(((length - place) / length) * 100)

            percentile = int( ( (length - (place-1)) / length ) * 100)
            return (place, length, percentile)
    return (0, len(team_data), 0)
