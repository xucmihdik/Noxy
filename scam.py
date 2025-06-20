import discord
import time
import os
from discord.ext import commands
from flask import Flask
import threading

# Uptime ping server
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive."

def run():
    app.run(host='0.0.0.0', port=8080)

threading.Thread(target=run).start()

# Discord bot setup
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

    embed = discord.Embed(
        title="🏓 Pong!",
        color=discord.Color.green()
    )
    embed.add_field(name="Latency", value=f"{latency}ms", inline=True)
    embed.add_field(name="Uptime", value=f"{uptime}s", inline=True)

    await interaction.response.send_message(embed=embed)

client.run(os.getenv("TOKEN"))
