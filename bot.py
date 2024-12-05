import discord
from discord import app_commands
from discord.ext import commands

from settings import *
from get_data import *

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
@bot.tree.command(name="team", description="Gets image data for a team")
@app_commands.describe(
    team_id = "Team ID"
)
async def team_command(interaction: discord.Interaction, team_id: str):
    data = get_data(team_id)
    team_data = data["team"]
    image_data = data["image"]

    embed = discord.Embed(
        title = f"Team {team_data['team_number']}",
        description = f"Location: {team_data['location']}, Division: {team_data['division']}",
        color=0
    )

    embed.add_field(name="Play Time", value=team_data["play_time"])
    embed.add_field(name="Score Time", value=team_data["score_time"])

    embed.add_field(name="CCS Score", value=team_data["ccs_score"])
    embed.add_field(name="Cisco Score", value=team_data["score_1"])
    embed.add_field(name="Adjust", value=team_data["adjustment"])
    embed.add_field(name="Total Score", value=f"**{team_data['total']}**")

    await interaction.response.send_message(embed=embed, ephemeral=False)

def start_bot():
    bot.run(get_setting("discord_secret"))
