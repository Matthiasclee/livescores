import discord
from discord import app_commands
from discord.ext import commands

from settings import *
from get_data import *
from embeds import *

intents = discord.Intents.default()
#intents.message_content = True
#intents.messages = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Bot ready event
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

# Slash command with arguments
@bot.tree.command(name="team", description="Gets live score data for a team")
@app_commands.describe(
    team_id = "Team ID"
)
async def team_command(interaction: discord.Interaction, team_id: str):
    await interaction.response.defer(ephemeral=False, thinking=True)

    data = get_data(team_id, "live")

    if data['error']:
        embed = make_error_embed("Error fetching data", data["error"])
    else:
        embed = make_team_embed(data, "live scoreboard")

    #await interaction.response.send_message(embed=embed, ephemeral=False)
    await interaction.followup.send(embed=embed, ephemeral=False)

@bot.tree.command(name="historical", description="Gets historical score data for a team")
@app_commands.describe(
    team_id = "Team ID",
    data_source = "Data Source"
)
async def team_command(interaction: discord.Interaction, team_id: str, data_source: str):
    await interaction.response.defer(ephemeral=False, thinking=True)

    data = get_data(team_id, data_source)

    if data['error']:
        embed = make_error_embed("Error fetching data", data["error"])
    else:
        embed = make_team_embed(data, data_source)

    #await interaction.response.send_message(embed=embed, ephemeral=False)
    await interaction.followup.send(embed=embed, ephemeral=False)

def start_bot():
    bot.run(get_setting("discord_secret"))
