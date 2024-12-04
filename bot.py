import discord
from discord import app_commands
from discord.ext import commands

from settings import *
from get_data import *

intents = discord.Intents.default()
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
@bot.tree.command(name="greet", description="Greets a user with a custom message.")
@app_commands.describe(
    name="The name of the person to greet.",
    age="The age of the person."
)
async def greet_command(interaction: discord.Interaction, name: str, age: int):
    embed = discord.Embed(
        title="Greeting!",
        description=f"Hello, **{name}**! 🎉 You are **{age}** years old!",
        color=discord.Color.green(),
    )
    embed.set_footer(text="Thanks for using the bot!")
    await interaction.response.send_message(embed=embed, ephemeral=False)

def start_bot():
    bot.run(get_setting("discord_secret"))
