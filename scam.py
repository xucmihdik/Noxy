import discord

from discord.ext import commands

from discord import app_commands

intents = discord.Intents.default()

intents.message_content = True

client = commands.Bot(command_prefix="!", intents=intents)

tree = client.tree

@tree.command(name="ping", description="Check latency")

async def ping(interaction: discord.Interaction):

    latency = round(client.latency * 1000)

    embed = discord.Embed(

        title="ðŸ“ Pong!",

        description=f"**Latency:** `{latency}ms`",

        color=discord.Color.green()

    )

    await interaction.response.send_message(embed=embed)

@client.event

async def on_ready():

    await tree.sync()

    print(f"Logged in as {client.user}")

client.run("MTM4NDkxODYxOTU4MTg0NTUyNA.GjyXVl.b4oRitDmI1bTD_VE-VsQ4zrmLC53LeEYYrGlPo")
