# LiveScores
LiveScores is a discord bot that provides live data from the [CyberPatriot Scoreboard](https://scoreboard.uscyberpatriot.org).
LiveScores can also provide archived historical data.
<br>
CyberPatriot Discord: [https://discord.gg/5gwnW7sTwv](https://discord.gg/5gwnW7sTwv)
<br>
Invite: [https://discord.com/oauth2/authorize?client_id=1313965570068185118](https://discord.com/oauth2/authorize?client_id=1313965570068185118)

## Using the bot
* `/team <team id> [data source]`: Get score data for `<team id>` from `[data source]`. If no data source is specified, data is gotten live from the scoreboard
* `/leaderboard [page] [division] [location] [tier] [teams per page] [teams to highlight] [data source] [image]`: Gets leaderboard data with the options specified
* `/datasources`: Lists all valid historical data sources
* `/advancement [team] [season] [excluded teams]`: Gets team advancement data for `[team]` in CyberPatriot `[season]`, excluding `[excluded teams]`
* `/help`: Shows the help menu

## Running the bot
To run the bot, run `python3 main.py`
### Requirements
* `discord` python library (`pip3 install discord`)
* A discord bot token
### Settings
To set up the bot, create a file titled `secrets.json` with the following format:
```json
{
  "discord_secret": "FXRXEXEXSXTX3XWXAXRXTXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX (your bot token here)",
  "contact_info": "(any contact info here - this is not required for operation but is recommended, as it is required by CyberPatriot API documentation)"
}
```
### Archiving historical data
To archive historical data, run `python3 download_data.py <name>` where `<name>` is the name of the datasource.
After doing this, you will need to add `<name>` to `"valid_data_sources"` in settings to make the source usable.

<br>

[Privacy Policy](https://github.com/Matthiasclee/livescores/blob/master/docs/privacy_policy.md) | [Terms of Service](https://github.com/Matthiasclee/livescores/blob/master/docs/terms_of_service.md)
