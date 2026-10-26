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

def _score_names_for(data_source):
    score_names = get_setting("score_names")
    if data_source in score_names:
        return score_names[data_source]
    return ["Quiz", "Packet Tracer", "Web", ""]

def _field_for_named_component(data_source, component_name):
    """Return score_N for a named component (e.g. 'quiz' -> 'score_1'), or None."""
    names = _score_names_for(data_source)
    target = component_name.lower()
    for i, n in enumerate(names[:3]):
        if n and n.lower() == target:
            return f"score_{i + 1}"
    # Hard-coded fallbacks
    fallbacks = {
        "packet tracer": "score_2",
        "quiz": "score_1",
        "web": "score_3",
        "boeing": "score_1",
    }
    return fallbacks.get(target)

def resolve_score_component(name, data_source):
    """
    If name is a known competition-score alias (PT, cisco, quiz, ...), return
    (score_spec, display_name).

    score_spec is either:
      - a string like "score_2" for a single field
      - a list of fields like ["score_1", "score_2"] for a combined total (cisco = quiz + PT)

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

    # cisco = Quiz + Packet Tracer combined
    if target == "cisco":
        quiz_f = _field_for_named_component(data_source, "quiz")
        pt_f = _field_for_named_component(data_source, "packet tracer")
        fields = [f for f in (quiz_f, pt_f) if f]
        if not fields:
            # Very old seasons where the single field is literally named Cisco
            cisco_f = None
            names = _score_names_for(data_source)
            for i, n in enumerate(names[:3]):
                if n and n.lower() == "cisco":
                    cisco_f = f"score_{i + 1}"
                    break
            if cisco_f:
                return (cisco_f, "Cisco")
            fields = ["score_1", "score_2"]
        return (fields, "Cisco (Quiz + PT)")

    # Single component: quiz, packet tracer, web, boeing
    field = _field_for_named_component(data_source, target)
    if field:
        # Use official score_names label only when it matches what the user asked for
        names = _score_names_for(data_source)
        idx = int(field[-1]) - 1
        if idx < len(names) and names[idx] and names[idx].lower() == target:
            display = names[idx]
        else:
            display = {
                "packet tracer": "Packet Tracer",
                "quiz": "Quiz",
                "web": "Web",
                "boeing": "Boeing",
            }.get(target, target.title())
        return (field, display)

    return None


def _team_component_score(team, score_spec):
    """
    score_spec: "score_1" or ["score_1", "score_2"]
    Returns float score or None if the team has no usable value.
    """
    fields = score_spec if isinstance(score_spec, (list, tuple)) else [score_spec]
    total = 0.0
    any_present = False
    for f in fields:
        if f not in team or team[f] == "":
            continue
        try:
            total += float(team[f])
            any_present = True
        except (TypeError, ValueError):
            continue
    if not any_present:
        return None
    return total


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
            # Rank by a competition component (or cisco = quiz + PT)
            score = _team_component_score(team, score_field)
            if score is None:
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
