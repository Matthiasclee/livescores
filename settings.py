import json

def get_setting(setting):
    settings_file = open("settings.json")

    settings = json.load(settings_file)

    settings_file.close()

    return settings[setting]

def get_secret(setting):
    settings_file = open("secrets.json")

    settings = json.load(settings_file)

    settings_file.close()

    return settings[setting]
