DATA_SOURCE = 0 # 0: file, 1: website
WEBSITE_URL = "https://scoreboard.uscyberpatriot.org/team.php?team="

def get_data(team):
    if DATA_SOURCE == 0:
        file = open(f"score_archives/{team}.html")
        data = file.read()
        file.close()
    elif DATA_SOURCE == 1:
        data = urllib.request.urlopen(f"{WEBSITE_URL}{team}").read()

    return data
