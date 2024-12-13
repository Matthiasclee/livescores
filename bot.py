# Import discord library
import discord
from discord import app_commands
from discord.ext import commands

# Import settings, get_data, and embeds files
from settings import *
from get_data import *
from embeds import *

# Create the discord bot with default intents
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!livescores", intents=intents)

# Run when the bot is ready
@bot.event
async def on_ready():
    # Print the user the bot is logged in as
    print(f"Logged in as {bot.user}, bot is in {len(bot.guilds)} guilds.")

    # Try to sync the bot's commands with discord
    try:
        synced = await bot.tree.sync()

        # Print the amount of synced commands if successful
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        # Print the error if it can't sync commands
        print(f"Failed to sync commands: {e}")

# Initialize the "team" command
@bot.tree.command(name="team", description="Gets live score data for a team")

# Provide descriptions for the command's arguments
@app_commands.describe(
    team_id = "Team ID",
    data_source = "Data Source"
)

# Define the command
# Arguments: - interaction (provided by discord)
#            - team_id (provided by user)
#            - data_source (optionally provided by user) - default: "live scoreboard"
# Output: embed containing either team data or an error (send to the user)
async def team_command(interaction: discord.Interaction, team_id: str, data_source: str = "live scoreboard"):
    # Defer the interaction so that the bot is able to take longer than 3 seconds to respond
    # Uses ephemeral=False and thinking=True so the bot shows a "LiveScores is thinking..." prompt while the user is waiting.
    await interaction.response.defer(ephemeral=False, thinking=True)

    # Use the get_data function to get the team's score data with their ID and provided data source
    data = get_data(team_id, data_source)

    # Check if there was an error getting the data
    if data['error']:
        # Set the embed to an error embed with the error message if there was an error
        embed = make_error_embed("Error fetching data", data["error"])
    else:
        # If fetching data was successful, make an embed with the team's data 
        embed = make_team_embed(data, data_source)

    # Send whatever embed was created as a followup to the interaction.
    # Use ephemeral=False to make the response visible to everyone
    await interaction.followup.send(embed=embed, ephemeral=False)

# Initialize the "datasources" command
@bot.tree.command(name="datasources", description="Show all data sources")

# Define the datasources command
# Arguments: - interaction (provided by discord)
# Output: datasources as embed (sent to the user)
async def datasources_command(interaction: discord.Interaction):
    # Get valid data sources from the bot settings
    datasources = get_setting("valid_data_sources")

    # Make an embed of the data sources
    embed = make_datasources_embed(datasources)

    # Send the embed back as an intersction response. Uses ephemeral=True so the response is only visible to the user.
    await interaction.response.send_message(embed=embed, ephemeral=True)

# Start the bot
# No arguments, no returns
def start_bot():
    # Runs the bot with the discord token from the settings
    bot.run(get_setting("discord_secret"))
