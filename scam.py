TOKEN = "MTM4MzY5NjMwOTUxNjc2NzI5Mg.GQV84A.x73E-Vo56JoySygGhk58c3pZAYBkDN3WpGZgts"

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
    activity = CustomActivity(name="BEST SCAM BOT")
    await client.change_presence(status=discord.Status.online, activity=activity)
    print(f"Logged in as {client.user}")

class ScamJoinView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.user_decisions = {}

    @discord.ui.button(label="Start", style=discord.ButtonStyle.success)
    async def join(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        prev = self.user_decisions.get(user_id)

        if prev == "no":
            await interaction.response.send_message(embed=discord.Embed(
                title="⚠️ Denied",
                description="You changed your mind, but once you back out, you're out. No re-entry.",
                color=discord.Color.orange()
            ), ephemeral=True)
            return
        elif prev == "yes":
            await interaction.response.send_message(embed=discord.Embed(
                title="⚠️ Already Joined",
                description="You already joined the profiting crew.",
                color=discord.Color.orange()
            ), ephemeral=True)
            return

        self.user_decisions[user_id] = "yes"
        role = interaction.guild.get_role(SCAM_ROLE_ID)
        if role:
            await interaction.user.add_roles(role)
            await interaction.response.send_message(embed=discord.Embed(
                title="You're In!",
                description=f"{interaction.user.mention} you are now joined the profiting crew.",
                color=discord.Color.green()
            ), ephemeral=True)
        else:
            await interaction.response.send_message("❌ Scam role not found.", ephemeral=True)

    @discord.ui.button(label="No", style=discord.ButtonStyle.danger)
    async def not_now(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        prev = self.user_decisions.get(user_id)

        if prev == "no":
            await interaction.response.send_message(embed=discord.Embed(
                title="⚠️ Already Decided",
                description="You've already walked away.",
                color=discord.Color.orange()
            ), ephemeral=True)
            return
        elif prev == "yes":
            self.user_decisions[user_id] = "no"
            role = interaction.guild.get_role(SCAM_ROLE_ID)
            if role:
                await interaction.user.remove_roles(role)
            await interaction.response.send_message(embed=discord.Embed(
                title="❌ Left the Crew",
                description="POOR FOREVER XDXD",
                color=discord.Color.red()
            ), ephemeral=True)
            return

        self.user_decisions[user_id] = "no"
        await interaction.response.send_message(embed=discord.Embed(
            title="You Rejected The Offer",
            description="BE POOR FOREVER XDDD",
            color=discord.Color.red()
        ), ephemeral=True)

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

@client.command()
@is_authorized()
async def gag(ctx):
    embed = discord.Embed(
        title="Unfortunately You Got Scammed",
        description=(
            "You want your stuff back? Take it.\n\n"
            "Use the same method. Same fake trust. If they fall for it, that’s your payday.\n\n"
            "This isn’t about being fair — it’s about not being the one who gets played. Flip it. Scam back. Profit fast.\n\n"
            "If you’re done being the victim and ready to start, choose below."
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
async def give_role(ctx, role: discord.Role, member: discord.Member):
    try:
        await member.add_roles(role)
        await ctx.send(f"✅ Gave `{role.name}` to {member.mention}")
    except discord.Forbidden:
        await ctx.send("❌ I don't have permission to give that role.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")
        
@client.command(name="remove")
@is_owner()
async def remove_role(ctx, role: discord.Role, member: discord.Member):
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
                description="You must specify **both** the role and the user.\n\nExample:\n`+give @role @user`\n`+remove @role @user`",
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

    elif isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title="❌ Unknown Command",
            description="That command doesn't exist. Please check your spelling or use a valid command.",
            color=discord.Color.dark_red()
        )
        await ctx.send(embed=embed)

    else:
        raise error

client.run(TOKEN)