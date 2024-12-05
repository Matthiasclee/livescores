# Import the json library
import json

# Get a setting
# Arguments: - setting: setting name to get
# Returns: setting value
def get_setting(setting):
    # Open the settings file
    settings_file = open("settings.json")

    # Parse the file with json
    settings = json.load(settings_file)

    # Close the file
    settings_file.close()

    # Return the setting's value
    return settings[setting]
