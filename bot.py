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
    if len(bot.guilds) == 1:
        s_text = ""
    else:
        s_text = "s"
    print(f"Logged in as {bot.user}, bot is in {len(bot.guilds)} guild{s_text}.")

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
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)

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
    highlight_teams = "Team IDs to highlight (space separated)",
    image = "Filter by image"
)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)

async def leaderboard_command(interaction: discord.Interaction, page: int = 1, division: str = "all", location: str = "all", tier: str = "all", per_page: int = 15, highlight_teams: str = "", data_source: str = "live scoreboard", image: str = ""):
    await interaction.response.defer(ephemeral=False, thinking=True)

    data = get_all_team_data(data_source)
    
    if image != "":
        image_data = get_all_image_data(data_source)
    else:
        image_data = {"error": False}

    if per_page > 90:
        embed = make_error_embed("Error", "Maximum of 90 teams per page")
    elif data['error']:
        embed = make_error_embed("Error fetching data", data["error"])
    elif image_data['error']:
        embed = make_error_embed("Error fetching image data", image_data["error"])
    else:
        embed = make_leaderboard_embed(data, data_source, division, location, tier, page, per_page, highlight_teams, image_data, image)

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="advancement", description="Show team advancement data")

@app_commands.describe(
    team_id = "Team ID",
    season = "CyberPatriot season",
    excluded_teams = "Teams to exclude for nationals advancement (space separated)"
)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)

async def advancement_command(interaction: discord.Interaction, team_id: str, season: str = "current", excluded_teams: str = ""):
    await interaction.response.defer(ephemeral=False, thinking=True)

    season_is_current = False
    if season == "current":
        season = get_setting("season")

    if len(team_id) == 4:
        team_id = f"{season}-{team_id}"

    if get_setting("season") == season:
        season_is_current = True

    valid_data_sources = get_setting("valid_data_sources")

    round_2_data_source = False
    semifinals_advancement_datasource = False
    nationals_advancement_datasource = False

    if f"cp{season}_r2" in valid_data_sources:
        round_2_data_source = f"cp{season}_r2"
    if f"cp{season}_r3" in valid_data_sources:
        semifinals_advancement_datasource = f"cp{season}_r3"
    if f"cp{season}_r4" in valid_data_sources:
        nationals_advancement_datasource = f"cp{season}_r4"

    r2_data = get_all_team_data(round_2_data_source) if round_2_data_source else None
    state_data = get_all_team_data(semifinals_advancement_datasource) if semifinals_advancement_datasource else None
    nationals_data = get_all_team_data(nationals_advancement_datasource) if nationals_advancement_datasource else None

    if not (state_data and nationals_data):
        live_team_data = get_all_team_data("live scoreboard")
        if (not live_team_data['error']) and season_is_current and r2_data and not r2_data['error']:
            if live_team_data != r2_data and not state_data:
                semifinals_advancement_datasource = "live scoreboard"
                state_data = live_team_data
            elif state_data and not state_data['error'] and live_team_data != state_data and not nationals_data:
                nationals_advancement_datasource = "live scoreboard"
                nationals_data = live_team_data

    team_state_data = get_data(team_id, semifinals_advancement_datasource)

    if get_data(team_id, nationals_advancement_datasource)['error']:
        nationals_data = None

    errors = (state_data['error'] if state_data else None) or (nationals_data['error'] if nationals_data else None) or team_state_data['error']

    if not state_data and not nationals_data:
        embed = make_error_embed("Error", f"No advancement data available for CyberPatriot {season}")
    elif errors:
        embed = make_error_embed("Error fetching data", errors)
    else:
        embed = make_advancement_embed(season, team_state_data['team'], state_data, nationals_data, excluded_teams, semifinals_advancement_datasource, nationals_advancement_datasource)

    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="datasources", description="Show all data sources")
@app_commands.describe(
    extra_sources = "Show extra sources (true/false)"
)
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)

async def datasources_command(interaction: discord.Interaction, extra_sources: str = "false"):
    datasources = get_setting("valid_data_sources")

    if extra_sources == "true":
        datasources = get_setting("additional_data_sources")

    embed = make_datasources_embed(datasources)

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name="help", description="LiveScores Help")
@app_commands.allowed_installs(guilds=True, users=True)
@app_commands.allowed_contexts(guilds=True, dms=True, private_channels=True)

async def help_command(interaction: discord.Interaction):
    embed = make_help_embed()

    await interaction.response.send_message(embed=embed, ephemeral=True)

def start_bot():
    bot.run(get_secret("discord_secret"))
