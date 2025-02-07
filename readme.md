# LiveScores
LiveScores is a discord bot that provides live data from the [CyberPatriot Scoreboard](https://scoreboard.uscyberpatriot.org).
LiveScores can also provide archived historical data.
<br>
Discord: [https://discord.gg/KQYF72KmWz](https://discord.gg/KQYF72KmWz)
<br>
Invite: [https://discord.com/oauth2/authorize?client_id=1313965570068185118](https://discord.com/oauth2/authorize?client_id=1313965570068185118)

## Using the bot
* `/team <team id> [data source]`: Get score data for `<team id>` from `[data source]`. If no data source is specified, data is gotten live from the scoreboard
* `/leaderboard [page] [division] [location] [tier] [teams per page] [teams to highlight] [data source]`: Gets leaderboard data with the options specified
* `/datasources`: Lists all valid historical data sources
* `/advancement [season] [excluded teams]`: Gets team advancement data for CyberPatriot `[season]`, excluding `[excluded teams]`

## Running the bot
To run the bot, run `python3 main.py`
### Requirements
* `discord` python library (`pip3 install discord`)
* A discord bot token
### Settings
To run the bot, copy `settings_template.json` to `settings.json`. Put your discord bot token in the `"discord_secret"` field. The following settings are available:
* `"valid_data_sources"`: Array of acceptable data sources
* `"season"`: Default season if user doesn't specify it in the team ID (`1984` becomes `17-1984`)
* `"discord_secret"`: Discord bot token
### Archiving historical data
To archive historical data, run `python3 download_data.py <name>` where `<name>` is the name of the datasource.
After doing this, you will need to add `<name>` to `"valid_data_sources"` in settings to make the source usable.
