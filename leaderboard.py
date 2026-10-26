from get_data import extract_team_image_data
from settings import get_setting

# Aliases users can type in the image parameter to rank by a competition score component
_COMPONENT_ALIASES = {
    "pt": "packet tracer",
    "packet tracer": "packet tracer",
    "packettracer": "packet tracer",
    "packet-tracer": "packet tracer",
    "cisco": "cisco",
    "quiz": "quiz",
    "web": "web",
    "boeing": "boeing",
    "score_1": "score_1",
    "score_2": "score_2",
    "score_3": "score_3",
    "score1": "score_1",
    "score2": "score_2",
    "score3": "score_3",
}

def resolve_score_component(name, data_source):
    """
    If name is a known competition-score alias (PT, cisco, quiz, ...), return
    (score_field, display_name) e.g. ("score_2", "Packet Tracer").
    Otherwise return None (treat name as an image name).
    """
    if not name:
        return None

    key = name.lower().strip()
    if key not in _COMPONENT_ALIASES:
        return None

    target = _COMPONENT_ALIASES[key]

    # Direct score_N request
    if target in ("score_1", "score_2", "score_3"):
        return (target, target.replace("_", " ").title())

    # Match against score_names for this data source when available
    score_names = get_setting("score_names")
    names = None
    if data_source in score_names:
        names = score_names[data_source]
    else:
        # Fallbacks used by make_team_embed when source is unknown
        names = ["Quiz", "Packet Tracer", "Web", ""]

    target_l = target.lower()
    for i, n in enumerate(names[:3]):
        if n and n.lower() == target_l:
            return (f"score_{i + 1}", n)

    # Common hard-coded fallbacks when the name isn't in score_names
    # Packet Tracer is almost always score_2; Quiz/Boeing often score_1; Web score_3
    fallbacks = {
        "packet tracer": ("score_2", "Packet Tracer"),
        "quiz": ("score_1", "Quiz"),
        "web": ("score_3", "Web"),
        "cisco": ("score_1", "Cisco"),   # often score_1; cp17_r4 uses score_2 — score_names handles that
        "boeing": ("score_1", "Boeing"),
    }
    if target_l in fallbacks:
        return fallbacks[target_l]

    return None


def get_leaderboard(all_team_data, division, location, tier, as_together: bool = False, excluded_teams: list = [], all_image_data: list = {}, image: str = "", score_field: str = ""):
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

        if score_field:
            # Rank by a competition component (Quiz / Packet Tracer / Cisco / Web / ...)
            if score_field not in team or team[score_field] == "":
                continue
            try:
                score = float(team[score_field])
            except (TypeError, ValueError):
                continue
            score_inverse = 2000 - score
            time = team.get("score_time") or "99:99:99"
            warnings = team.get("code") or ""
        elif image != "":
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
            if team["ccs_score"] == "":
                continue

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
