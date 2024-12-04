from bs4 import BeautifulSoup
from table_parser import *

def extract_scores(html):
    parsed_data = BeautifulSoup(html, features="html.parser")
    team_data_headers = parsed_data.select_one("#table-teams_wrapper").find_all("thead")[0]
    team_data_body = parsed_data.select_one("#table-teams_wrapper").find_all("tbody")[0]

    team_data = parse_table_by_headers(team_data_headers, team_data_body)
    image_data = {}

    image_data_headers = parsed_data.select_one("#table-images_wrapper")

    return { "team_data": team_data, "image_data": image_data }
