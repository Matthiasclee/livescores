from get_data import *
from extract_scores import *

def get_team_info(team):
    html_data = get_data(team)
    scores = extract_scores(html_data)
    return scores
