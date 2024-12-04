class TeamScore:
    def __init__(html_data):
        self.html_data = html_data

    def parse():
        parsed_data = BeautifulSoup(self.html_data)
        team_data_headers = parsed_data.select_one("#table-teams_wrapper").find_all("thead")[0]
        team_data_body = parsed_data.select_one("#table-teams_wrapper").find_all("tbody")[0]

        image_data = parsed_data.select_one("#table-images_wrapper")
