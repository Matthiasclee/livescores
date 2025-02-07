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
    data_source = "Data source"
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
    data_source = "Data source",
    highlight_teams = "Team IDs to highlight (space separated)"
)

async def leaderboard_command(interaction: discord.Interaction, page: int = 1, division: str = "all", location: str = "all", tier: str = "all", per_page: int = 15, highlight_teams: str = "", data_source: str = "live scoreboard"):
    await interaction.response.defer(ephemeral=False, thinking=True)

    data = get_all_team_data(data_source)

    if data['error']:
        embed = make_error_embed("Error fetching data", data["error"])
    else:
        embed = make_leaderboard_embed(data, data_source, division, location, tier, page, per_page, highlight_teams)

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="advancement", description="Show team advancement data")

@app_commands.describe(
    team_id = "Team ID",
    season = "CyberPatriot season"
)

async def leaderboard_command(interaction: discord.Interaction, team_id: str, season: str = "current"):
    await interaction.response.defer(ephemeral=False, thinking=True)

    season_is_current = False
    if season == "current":
        season = get_setting("season")

    if len(team_id) == 4:
        team_id = f"{season}-{team_id}"

    if get_setting("season") == season:
        season_is_current = True

    valid_data_sources = get_setting("valid_data_sources")

    semifinals_advancement_datasource = False
    nationals_advancement_datasource = False

    if f"cp{season}_r3" in valid_data_sources:
        semifinals_advancement_datasource = f"cp{season}_r3"
    if f"cp{season}_r4" in valid_data_sources:
        nationals_advancement_datasource = f"cp{season}_r4"

    state_data = get_all_team_data(semifinals_advancement_datasource) if semifinals_advancement_datasource else None
    nationals_data = get_all_team_data(nationals_advancement_datasource) if nationals_advancement_datasource else None

    team_state_data = get_data(team_id, semifinals_advancement_datasource)

    errors = (state_data['error'] if state_data else None) or (nationals_data['error'] if nationals_data else None) or team_state_data['error']

    if not state_data and not nationals_data:
        embed = make_error_embed("Error", f"No advancement data available for CyberPatriot {season}")
    elif errors:
        embed = make_error_embed("Error fetching data", errors)
    else:
        embed = make_advancement_embed(season, team_state_data['team'], state_data, nationals_data)

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="datasources", description="Show all data sources")

async def datasources_command(interaction: discord.Interaction):
    datasources = get_setting("valid_data_sources")

    embed = make_datasources_embed(datasources)

    await interaction.response.send_message(embed=embed, ephemeral=True)

def start_bot():
    bot.run(get_setting("discord_secret"))
