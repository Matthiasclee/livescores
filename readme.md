# LiveScores

## Using the bot
* `/team <team id> [data source]`: Get score data for `<team id>` from `[data source]`. If no data source is specified, data is gotten live from the scoreboard
* `/datasources`: Lists all valid historical data source

## Running the bot
### Requirements
* `discord` python library (`pip3 install discord`)
* A discord bot token
### Settings
To run the bot, copy `settings_template.json` to `settings.json`. Put your discord bot token in the `"discord_secret"` field. The following settings are available:
* `"valid_data_sources"`: Array of acceptable data sources
* `"season"`: Default season if user doesn't specify it in the team ID (`1369` becomes `17-1369`)
* `"discord_secret"`: Discord bot token
### Archiving historical data
To archive historical data, run `python3 download_data.py <name>` where `<name>` is the name of the datasource.
After doing this, you will need to add `<name>` to `"valid_data_sources"` in settings to make the source usable.
