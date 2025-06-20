import discord
import time
import os

from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="!", intents=intents)
tree = client.tree

start_time = time.time()

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} command(s).")
    except Exception as e:
        print(f"Sync error: {e}")

@tree.command(name="ping", description="Check bot's latency")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    uptime = round(time.time() - start_time)
    await interaction.response.send_message(f"🏓 Pong! Latency: {latency}ms | Uptime: {uptime}s")

if __name__ == "__main__":
    client.run(os.getenv("TOKEN"))
