from leaderboard import *

def determine_team_placement(team_info, all_team_data, scopes):
    if "division" in scopes:
        division = team_info["division"]
    else:
        division = False

    if "state" in scopes:
        location = team_info["location"]
    else:
        location = False

    if "tier" in scopes and "tier" in team_info:
        tier = team_info["tier"]
    else:
        tier = False

    team_data = get_leaderboard(all_team_data, division, location, tier)

    for i, score_data in enumerate(team_data):
        if score_data[1] == team_info["team_number"]:
            place = i+1
            length = len(team_data)
            percentile = int( ( (length - (place-1)) / length ) * 100)
            return (place, length, percentile)
    return (0, len(team_data), 0)
