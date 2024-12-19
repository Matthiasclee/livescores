import discord
from discord import app_commands
from discord.ext import commands

from settings import *
from get_data import *
from embeds import *

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!livescores", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}, bot is in {len(bot.guilds)} guilds.")

    try:
        synced = await bot.tree.sync()

        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.tree.command(name="team", description="Gets score data for a team")

@app_commands.describe(
    team_id = "Team ID",
    data_source = "Data Source"
)

async def team_command(interaction: discord.Interaction, team_id: str, data_source: str = "live scoreboard"):
    await interaction.response.defer(ephemeral=False, thinking=True)

    data = get_data(team_id, data_source)

    if data['error']:
        embed = make_error_embed("Error fetching data", data["error"])
    else:
        embed = make_team_embed(data, data_source)

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="leaderboard", description="Gets leaderboard data")

@app_commands.describe(
    page = "Scoreboard page",
    division = "Division",
    location = "Location",
    tier = "Tier",
    per_page = "Teams per page",
    data_source = "Data Source"
)

async def leaderboard_command(interaction: discord.Interaction, page: int = 1, division: str = "all", location: str = "all", tier: str = "all", per_page: int = 15, data_source: str = "live scoreboard"):
    await interaction.response.defer(ephemeral=False, thinking=True)

    data = get_all_team_data(data_source)

    if data['error']:
        embed = make_error_embed("Error fetching data", data["error"])
    else:
        embed = make_leaderboard_embed(data, data_source, division, location, tier, page, per_page)

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="datasources", description="Show all data sources")

async def datasources_command(interaction: discord.Interaction):
    datasources = get_setting("valid_data_sources")

    embed = make_datasources_embed(datasources)

    await interaction.response.send_message(embed=embed, ephemeral=True)

def start_bot():
    bot.run(get_setting("discord_secret"))
