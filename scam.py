TOKEN = "MTM4MzY5NjMwOTUxNjc2NzI5Mg.Go_pCu.2Zo3POYRA_5OSv9Wq6nQgZi0D8K6YB5gUL_G_Y"

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run).start()

import discord
from discord import CustomActivity
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = commands.Bot(command_prefix="+", intents=intents)

REQUIRED_ROLE_ID = 1383727498013048863
OWNER_ROLE_ID = 1383728003305050114
SCAM_ROLE_ID = 1383707834872758367

def is_authorized():
    async def predicate(ctx):
        return any(role.id in [REQUIRED_ROLE_ID, OWNER_ROLE_ID] for role in ctx.author.roles)
    return commands.check(predicate)

def is_owner():
    async def predicate(ctx):
        return any(role.id == OWNER_ROLE_ID for role in ctx.author.roles)
    return commands.check(predicate)

@client.event
async def on_ready():
    activity = CustomActivity(name="GrowStock Support")
    await client.change_presence(status=discord.Status.online, activity=activity)
    await client.tree.sync()
    print(f"Logged in as {client.user}")
    
@client.tree.command(name="ping", description="Check the bot's latency.")
async def ping(interaction: discord.Interaction):
    latency = round(client.latency * 1000)
    await interaction.response.send_message(
        embed=discord.Embed(
            title="🏓 Pong!",
            description=f"Latency: `{latency}ms`",
            color=discord.Color.blurple()
        )
    )

class MMInfoView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.user_interactions = {}

    @discord.ui.button(label="I Understand", style=discord.ButtonStyle.success)
    async def understand(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        decision = self.user_interactions.get(user_id)

        if decision == "yes":
            await interaction.response.send_message(embed=discord.Embed(
                title="⚠️ Already Agreed",
                description="You already agreed. No more changes allowed.",
                color=discord.Color.orange()
            ), ephemeral=True)
        elif decision == "no":
            self.user_interactions[user_id] = "changed"
            await interaction.response.send_message(embed=discord.Embed(
                title="✅ Changed to Agree",
                description=f"{interaction.user.mention} changed their mind and now agrees.",
                color=discord.Color.green()
            ))
        elif decision == "changed":
            await interaction.response.send_message(embed=discord.Embed(
                title="⚠️ Already Changed",
                description="You already changed your decision once. No more changes allowed.",
                color=discord.Color.orange()
            ), ephemeral=True)
        else:
            self.user_interactions[user_id] = "yes"
            await interaction.response.send_message(embed=discord.Embed(
                title="✅ Agreed",
                description=f"{interaction.user.mention} understands how a middle man works.",
                color=discord.Color.green()
            ))

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        decision = self.user_interactions.get(user_id)

        if decision == "no":
            await interaction.response.send_message(embed=discord.Embed(
                title="⚠️ Already Disagreed",
                description="You already said no. No more changes allowed.",
                color=discord.Color.orange()
            ), ephemeral=True)
        elif decision == "yes":
            self.user_interactions[user_id] = "changed"
            await interaction.response.send_message(embed=discord.Embed(
                title="❌ Change Disagree",
                description=f"{interaction.user.mention} changed their mind and disagrees now.",
                color=discord.Color.red()
            ))
        elif decision == "changed":
            await interaction.response.send_message(embed=discord.Embed(
                title="⚠️ Already Changed",
                description="You already changed your decision once. No more changes allowed.",
                color=discord.Color.orange()
            ), ephemeral=True)
        else:
            self.user_interactions[user_id] = "no"
            await interaction.response.send_message(embed=discord.Embed(
                title="❌ Disagreed",
                description=f"{interaction.user.mention} does not understand how a middle man works.",
                color=discord.Color.red()
            ))
            
class ConfirmTradeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.user_interactions = {}  # user_id: {"choice": "yes"/"no", "changes": 0}

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.success)
    async def yes(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        data = self.user_interactions.get(user_id, {"choice": None, "changes": 0})

        if data["choice"] == "yes":
            await interaction.response.send_message(embed=discord.Embed(
                title="⚠️ Already Confirmed",
                description="You already confirmed the trade.",
                color=discord.Color.orange()
            ), ephemeral=True)
            return

        if data["choice"] == "no":
            if data["changes"] >= 1:
                await interaction.response.send_message(embed=discord.Embed(
                    title="🚫 Change Blocked",
                    description="You've already changed your decision once. No more changes allowed.",
                    color=discord.Color.red()
                ), ephemeral=True)
                return
            else:
                data["choice"] = "yes"
                data["changes"] += 1
                self.user_interactions[user_id] = data
                await interaction.response.send_message(embed=discord.Embed(
                    title="✅ Changed to Confirm",
                    description=f"{interaction.user.mention} changed their mind and confirmed the trade.",
                    color=discord.Color.green()
                ))
                return

        data["choice"] = "yes"
        self.user_interactions[user_id] = data
        await interaction.response.send_message(embed=discord.Embed(
            title="✅ Trade Confirmed",
            description=f"{interaction.user.mention} confirmed the trade.",
            color=discord.Color.green()
        ))

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def no(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        data = self.user_interactions.get(user_id, {"choice": None, "changes": 0})

        if data["choice"] == "no":
            await interaction.response.send_message(embed=discord.Embed(
                title="⚠️ Already Declined",
                description="You already declined the trade.",
                color=discord.Color.orange()
            ), ephemeral=True)
            return

        if data["choice"] == "yes":
            if data["changes"] >= 1:
                await interaction.response.send_message(embed=discord.Embed(
                    title="🚫 Change Blocked",
                    description="You've already changed your decision once. No more changes allowed.",
                    color=discord.Color.red()
                ), ephemeral=True)
                return
            else:
                data["choice"] = "no"
                data["changes"] += 1
                self.user_interactions[user_id] = data
                await interaction.response.send_message(embed=discord.Embed(
                    title="❌ Changed to Decline",
                    description=f"{interaction.user.mention} changed their mind and declined the trade.",
                    color=discord.Color.red()
                ))
                return

        data["choice"] = "no"
        self.user_interactions[user_id] = data
        await interaction.response.send_message(embed=discord.Embed(
            title="❌ Trade Declined",
            description=f"{interaction.user.mention} declined the trade.",
            color=discord.Color.red()
        ))            

class ScamJoinView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.user_clicked = set()

    @discord.ui.button(label="Info", style=discord.ButtonStyle.secondary)
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        if user_id in self.user_clicked:
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="⚠️ Already Viewed",
                    description="You’ve already clicked **Info**. No need to press it again.",
                    color=discord.Color.orange()
                ),
                ephemeral=True
            )
            return

        self.user_clicked.add(user_id)

        embed = discord.Embed(
            title="📘 Quick Start Guide",
            description=(
                "1. Find potential targets in trading servers for your game.\n"
                "2. Once you agree on a deal, suggest using our trusted MM team.\n"
                "3. After they agree, open a ticket and wait for a staff to finalize the setup.\n"
                "4. Profits are shared 50/50 or sometimes fully yours.\n"
                "5. When you're ready, press **'Yes, I'm Ready'** to get your role and start!"
            ),
            color=discord.Color.blurple()
        )
        await interaction.response.send_message(embed=embed, view=ReadyView(), ephemeral=False)


class ReadyView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.user_data = {}  # user_id: {"choice": "yes"/"no"}

    @discord.ui.button(label="Yes, I'm Ready", style=discord.ButtonStyle.success)
    async def ready(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        data = self.user_data.get(user_id, {"choice": None})

        if data["choice"] == "yes":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="⚠️ Already Ready",
                    description="You've already selected **'Yes, I'm Ready'**.",
                    color=discord.Color.orange()
                ),
                ephemeral=True
            )
            return

        if data["choice"] == "no":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="🚫 Can't Proceed",
                    description="You already selected **'Never mind'** first. You can't change to 'Yes, I'm Ready'.",
                    color=discord.Color.red()
                ),
                ephemeral=True
            )
            return

        self.user_data[user_id] = {"choice": "yes"}
        await interaction.response.defer()
        await self._give_role(interaction)

    @discord.ui.button(label="Never mind", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        data = self.user_data.get(user_id, {"choice": None})

        if data["choice"] == "no":
            await interaction.response.send_message(
                embed=discord.Embed(
                    title="⚠️ Already Cancelled",
                    description="You've already selected **'Never mind'**.",
                    color=discord.Color.orange()
                ),
                ephemeral=True
            )
            return

        self.user_data[user_id] = {"choice": "no"}
        await interaction.response.defer()
        await self._remove_role(interaction)
        await interaction.followup.send(
            embed=discord.Embed(
                title="❌ Never mind",
                description="You've changed your decision and chose not to proceed.",
                color=discord.Color.red()
            )
        )

    async def _give_role(self, interaction):
        scam_role = discord.utils.get(interaction.guild.roles, id=SCAM_ROLE_ID)
        if scam_role:
            try:
                await interaction.user.add_roles(scam_role)
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="✅ You're In",
                        description=f"{interaction.user.mention} is now a Hitter! Role assigned.",
                        color=discord.Color.green()
                    )
                )
            except discord.Forbidden:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="❌ Permission Error",
                        description="I don't have permission to give the role. Please fix my role settings.",
                        color=discord.Color.red()
                    )
                )

    async def _remove_role(self, interaction):
        scam_role = discord.utils.get(interaction.guild.roles, id=SCAM_ROLE_ID)
        if scam_role in interaction.user.roles:
            try:
                await interaction.user.remove_roles(scam_role)
            except discord.Forbidden:
                await interaction.followup.send(
                    embed=discord.Embed(
                        title="❌ Permission Error",
                        description="I can't remove the role. Please check my role permissions.",
                        color=discord.Color.red()
                    )
                )

@client.command()
@is_authorized()
async def gag(ctx):
    embed = discord.Embed(
        title="Unfortunately you’ve been scammed!",
        description=(
            "But there’s still a way to turn this situation around.\n"
            "Join as a Hitter!\n"
            "Tap the info button to learn more about how hitting works."
        ),
        color=discord.Color.orange()
    )
    await ctx.send(embed=embed, view=ScamJoinView())

@client.command()
@is_authorized()
async def mminfo(ctx):
    embed = discord.Embed(
        title="Who is a MM (Middle man)?",
        description="A middleman is an intermediary who helps handle transactions between two parties, usually a buyer and a seller.",
        color=discord.Color.from_rgb(240, 240, 240)  # Light gray, close to white
    )
    embed.set_image(url="https://files.catbox.moe/tbg221.png")
    await ctx.send(embed=embed, view=MMInfoView())

@client.command()
@is_authorized()
async def confirm(ctx):
    embed = discord.Embed(
        title="Trade Confirmation",
        description="Do both parties confirm the trade? Press a button below.",
        color=discord.Color.green()
    )
    await ctx.send(embed=embed, view=ConfirmTradeView())

@client.command(name="give")
@is_owner()
async def give_role(ctx, member: discord.Member, role: discord.Role):
    try:
        await member.add_roles(role)
        await ctx.send(f"✅ Gave `{role.name}` to {member.mention}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to give that role.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")

@client.command(name="remove")
@is_owner()
async def remove_role(ctx, member: discord.Member, role: discord.Role):
    try:
        await member.remove_roles(role)
        await ctx.send(f"✅ Removed `{role.name}` from {member.mention}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to remove that role.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        embed = discord.Embed(
            title="🚫 Permission Denied",
            description="You don’t have permission to use this command.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    elif isinstance(error, commands.MissingRequiredArgument):
        if ctx.command.name in ["give", "remove"]:
            embed = discord.Embed(
                title="⚠️ Missing Required Info",
                description="You must specify both the user and the role.\n\nCorrect format:\n`+give @user @role`\n`+remove @user @role`",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="⚠️ Missing Argument",
                description="You missed a required argument for this command.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    elif isinstance(error, commands.BadArgument) and ctx.command.name == "give":
        embed = discord.Embed(
            title="❌ Wrong Argument Order",
            description="It looks like you used `+give @role @user`, but the correct order is:\n\n`+give @user @role`",
            color=discord.Color.blurple()
        )
        await ctx.send(embed=embed)

    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❌ Unknown Command",
            description="That command doesn't exist. Please check your spelling.",
            color=discord.Color.dark_red()
        )
        await ctx.send(embed=embed)

    else:
        raise error

client.run(TOKEN)
