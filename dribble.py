{\rtf1\ansi\ansicpg1252\cocoartf2865
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;\f1\fnil\fcharset0 AppleColorEmoji;\f2\fnil\fcharset0 STIXTwoMath-Regular;
}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import discord\
from discord.ext import commands\
import os\
import json\
import asyncio\
from discord.ext import tasks\
from datetime import datetime, timezone\
# ---------------- BOT SETUP ----------------\
intents = discord.Intents.default()\
intents.guilds = True\
intents.messages = True\
intents.message_content = True\
intents.members = True\
\
bot = commands.Bot(command_prefix="$", intents=intents)\
\
MAIN_COLOR = 0xB79BEB\
ICON_URL = "https://images-ext-1.discordapp.net/external/6Dtval-9vtswsuE-cWp67CwjvLRqCH5ZRbEQiEEFDj8/%3Fsize%3D1024/https/cdn.discordapp.com/icons/1437030353674965097/45a3aa89511f4e2fdc5f88a07a1b5296.png?format=webp&quality=lossless&width=387&height=387"\
PLACEHOLDER_ICON = "https://i.pinimg.com/originals/84/8c/34/848c342a56e7854dec45b9349c21dfe5.gif"\
\
if not os.path.exists("servers"):\
    os.mkdir("servers")\
\
\
def save_server_config(guild_id, data):\
    with open(f"servers/\{guild_id\}.json", "w") as f:\
        json.dump(data, f)\
\
\
def load_server_config(guild_id):\
    try:\
        with open(f"servers/\{guild_id\}.json", "r") as f:\
            return json.load(f)\
    except:\
        return None\
\
\
def is_admin():\
    async def predicate(ctx):\
        return ctx.author.guild_permissions.administrator\
    return commands.check(predicate)\
\
\
# ----------------- $mmrole set -----------------\
@bot.command()\
@is_admin()\
async def mmrole(ctx, action: str, role_id: int = None):\
    if action.lower() != "set" or not role_id:\
        await ctx.send("Usage: `$mmrole set (roleid)`")\
        return\
\
    guild_config = load_server_config(ctx.guild.id) or \{\}\
    guild_config["mm_role"] = role_id\
    save_server_config(ctx.guild.id, guild_config)\
    await ctx.send(f"Middleman role has been set to <@&\{role_id\}>")\
\
\
\
import random\
\
@bot.command()\
async def claim(ctx):\
    claimed_number = random.randint(1, 1000)\
    await ctx.send(f"\{ctx.author.mention\} that used the command claimed this ticket")\
    await ctx.channel.edit(name=f"\{claimed_number\}-claimed")\
\
# ----------------- $close -----------------\
@bot.command()\
@is_admin()\
async def close(ctx):\
    await ctx.send("Closing ticket in 5 seconds 
\f1 \uc0\u55357 \u56785 \u65039 
\f0 ")\
    await asyncio.sleep(5)\
    await ctx.channel.delete()\
\
\
@bot.command()\
@is_admin()\
async def setupmm(ctx):\
    def check(m):\
        return m.author == ctx.author and m.channel == ctx.channel\
\
    # ask for category id\
    await ctx.send("What is your desired category id for the tickets to be placed?")\
    category_msg = await bot.wait_for("message", check=check)\
    category_id = int(category_msg.content)\
\
    # ask for panel channel id\
    await ctx.send("Where would you like us to send the MM panel? (channel id)")\
    channel_msg = await bot.wait_for("message", check=check)\
    panel_channel_id = int(channel_msg.content)\
\
    # save config\
    save_server_config(ctx.guild.id, \{\
        "setup": True,\
        "category_id": category_id,\
        "panel_channel_id": panel_channel_id\
    \})\
\
    panel_channel = bot.get_channel(panel_channel_id)\
\
    # panel embed\
    panel_embed = discord.Embed(\
        title="Middleman Services",\
        description=(\
            "
\f2 \uc0\u11037 
\f0  Click the blue **Request Middleman** button below to create a ticket.\\n\\n"\
            "**How Middleman Works:**\\n"\
            "1. Trader #1 sends item to middleman.\\n"\
            "2. Trader #2 sends item to middleman.\\n"\
            "3. Middleman completes the trade.\\n\\n"\
            "__DISCLAIMER__\\n"\
            "Dribble is responsible for all trades and scams, dribble is not allowed to be inside fake servers.\\n"\
        ),\
        color=MAIN_COLOR\
    )\
    panel_embed.set_thumbnail(url=ICON_URL)\
\
    class RequestMM(discord.ui.View):\
        @discord.ui.button(label="Request Middleman", style=discord.ButtonStyle.primary)\
        async def request(self, interaction: discord.Interaction, button: discord.ui.Button):\
            guild_config = load_server_config(ctx.guild.id)\
            if not guild_config:\
                await interaction.response.send_message("Server is not setup.", ephemeral=True)\
                return\
\
            category = discord.utils.get(ctx.guild.categories, id=guild_config["category_id"])\
            ticket_channel = await category.create_text_channel(f"mm-\{interaction.user.name.lower()\}")\
\
            # welcome embed\
            welcome_embed = discord.Embed(\
                title="Dribble Middleman System",\
                description="Ticket created successfully!\\nWelcome to Dribble Middleman system.",\
                color=MAIN_COLOR\
            )\
            welcome_embed.set_thumbnail(url=PLACEHOLDER_ICON)\
            await ticket_channel.send(embed=welcome_embed)\
\
            # security embed\
            security_embed = discord.Embed(\
                title="Security Notice",\
                description="Dribble is not responsible for lost items or robux. Report scams if needed.",\
                color=MAIN_COLOR\
            )\
            await ticket_channel.send(embed=security_embed)\
\
            # ask for other user\
            ask_embed = discord.Embed(\
                title="Who are you trading with?",\
                description="Mention the user or provide their ID.",\
                color=MAIN_COLOR\
            )\
            await ticket_channel.send(embed=ask_embed)\
\
            def user_check(m):\
                return m.channel == ticket_channel and m.author == interaction.user\
\
            user_msg = await bot.wait_for("message", check=user_check)\
            other_user = user_msg.content\
\
            user_added = discord.Embed(\
                title="User Added",\
                description=f"\{other_user\} added to the ticket.",\
                color=MAIN_COLOR\
            )\
            user_added.set_thumbnail(url=ICON_URL)\
            await ticket_channel.send(embed=user_added)\
\
            # role selection\
            class RoleSelection(discord.ui.View):\
                def __init__(self):\
                    super().__init__()\
                    self.selected_roles = \{\}\
\
                @discord.ui.button(label="Sending", style=discord.ButtonStyle.secondary)\
                async def sending(self, interaction: discord.Interaction, button: discord.ui.Button):\
                    if interaction.user.id in self.selected_roles:\
                        await interaction.response.send_message("You already selected a role.", ephemeral=True)\
                        return\
                    self.selected_roles[interaction.user.id] = "Sending"\
                    button.disabled = True\
                    await self.update_role_embed(interaction)\
\
                @discord.ui.button(label="Giving Item", style=discord.ButtonStyle.secondary)\
                async def giving(self, interaction: discord.Interaction, button: discord.ui.Button):\
                    if interaction.user.id in self.selected_roles:\
                        await interaction.response.send_message("You already selected a role.", ephemeral=True)\
                        return\
                    self.selected_roles[interaction.user.id] = "Giving Item"\
                    button.disabled = True\
                    await self.update_role_embed(interaction)\
\
                async def update_role_embed(self, interaction):\
                    embed = discord.Embed(\
                        title="Role Selection",\
                        description="\\n".join([f"**\{interaction.guild.get_member(uid).name\}** selected **\{role\}**"\
                                               for uid, role in self.selected_roles.items()]),\
                        color=MAIN_COLOR\
                    )\
                    await interaction.response.edit_message(embed=embed, view=self)\
                    if len(self.selected_roles) >= 2:\
                        await self.start_deal(interaction)\
\
                async def start_deal(self, interaction):\
                    deal_embed = discord.Embed(\
                        title="Deal",\
                        description=(\
                            "State the deal (be precise):\\n"\
                            "eg. 500 robux for Grow a garden (item)\\n"\
                            "eg. $5 Paypal for MM2 (item)\\n\\n"\
                            "**VERY IMPORTANT:**\\n"\
                            "Include one of the keywords: robux, paypal, crypto (solana, litecoin, bitcoin, ethereum)"\
                        ),\
                        color=MAIN_COLOR\
                    )\
                    await interaction.followup.send(embed=deal_embed)\
\
                    def deal_check(m):\
                        return m.channel == interaction.channel and m.author.id in self.selected_roles\
\
                    deal_msg = await bot.wait_for("message", check=deal_check)\
                    deal_text = deal_msg.content.lower()\
\
                    # detect payment type and auto-confirm\
                    if "robux" in deal_text:\
                        payment_type = "robux"\
                        instructions = "Robux fee is free. Proceed with the deal."\
                    elif "paypal" in deal_text:\
                        payment_type = "paypal"\
                        instructions = "Fee automatically confirmed. Send $0.20 to holderkristen89@gmail.com and proceed."\
                    elif any(crypto in deal_text for crypto in ["solana","litecoin","bitcoin","ethereum"]):\
                        payment_type = "crypto"\
                        detected = next((c for c in ["solana","litecoin","bitcoin","ethereum"] if c in deal_text), None)\
                        instructions = f"Send \{detected\} to the placeholder address. Payment automatically confirmed."\
                    else:\
                        payment_type = None\
                        instructions = "No valid payment type detected. Include robux, paypal, or crypto."\
\
                    payment_embed = discord.Embed(\
                        title="Payment Instructions",\
                        description=instructions,\
                        color=MAIN_COLOR\
                    )\
                    await interaction.channel.send(embed=payment_embed)\
\
                    # confirm deal embed\
                    confirm_embed = discord.Embed(\
                        title="Deal Confirmed",\
                        description=(\
                            f"Deal stated:\\n\{deal_msg.content\}\\n\\n"\
                            "Payment type detected: **\{payment_type\}**\\n"\
                            "All payments automatically confirmed where applicable.\\n\\n"\
                            "**Middleman can now attend the ticket.**"\
                        ),\
                        color=MAIN_COLOR\
                    )\
                    await interaction.channel.send(embed=confirm_embed)\
\
            role_embed = discord.Embed(\
                title="Role Selection",\
                description="Select your role. Each participant can click one button.",\
                color=MAIN_COLOR\
            )\
            role_embed.set_thumbnail(url=ICON_URL)\
            await ticket_channel.send(embed=role_embed, view=RoleSelection())\
            await interaction.response.send_message(f"Ticket created: \{ticket_channel.mention\}", ephemeral=True)\
\
    await panel_channel.send(embed=panel_embed, view=RequestMM())\
    await ctx.send("MM Panel setup completed.")\
\
\
\
\
# ----------------- $setupstaff -----------------\
@bot.command()\
@is_admin()\
async def setupstaff(ctx):\
    def check(m):\
        return m.author == ctx.author and m.channel == ctx.channel\
\
    await ctx.send("What is your staff role id:")\
    msg = await bot.wait_for("message", check=check)\
    staff_role_id = int(msg.content)\
\
    guild_config = load_server_config(ctx.guild.id) or \{\}\
    guild_config["staff_role"] = staff_role_id\
    save_server_config(ctx.guild.id, guild_config)\
\
    # Create Staff category\
    overwrites = \{\
        ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),\
        ctx.guild.get_role(staff_role_id): discord.PermissionOverwrite(view_channel=True)\
    \}\
    staff_category = await ctx.guild.create_category("Staff - category", overwrites=overwrites)\
\
    # Create channels\
    channels = ["announcements", "help", "staff chat", "hits", "updates"]\
    for ch_name in channels:\
        await staff_category.create_text_channel(ch_name)\
\
    await ctx.send(f"Staff category and channels created. Role <@&\{staff_role_id\}> has access.")\
\
# ----------------- $howto -----------------\
@bot.command()\
async def howto(ctx):\
    embed = discord.Embed(\
        title="How to become a hitter",\
        description=(\
            "- First find targets inside of trading servers \\n"\
            "- Dm them and ask them to use a Middleman to avoid any scams\\n"\
            "- Create a middleman ticket and act as if it was normal\\n"\
            "- Our trained middleman will take the items and split 50/50 with you\\n"\
            "- If you have any questions feel free to ask inside our staff chat."\
        ),\
        color=MAIN_COLOR\
    )\
    embed.set_thumbnail(url="https://images-ext-1.discordapp.net/external/S-ZMbRm7QIaDWnEiuN5ZPNQrXOz0vBAIeXIIZitNfC8/%3Fformat%3Dwebp%26quality%3Dlossless%26width%3D387%26height%3D387/https/images-ext-1.discordapp.net/external/6Dtval-9vtswsuE-cWp67CwjvLRqCH5ZRbEQiEEFDj8/%253Fsize%253D1024/https/cdn.discordapp.com/icons/1437030353674965097/45a3aa89511f4e2fdc5f88a07a1b5296.png?format=webp&quality=lossless&width=387&height=387") \
    await ctx.send(embed=embed)\
\
from discord import ui, ButtonStyle, Interaction\
\
@bot.command()\
async def invite(ctx):\
    # First embed: scam warning\
    scam_embed = discord.Embed(\
        title="We are so sorry that you have been scammed",\
        description=(\
            "You are now invited to become a hitter for our team\\n"\
            "If you accept you will be given access to our staff chat\\n"\
            "You can make thousands of dollars a day by hitting\\n"\
            "You can also earn hundreds of roblox valuables\\n"\
            "Join us now to become rich"\
        ),\
        color=MAIN_COLOR\
    )\
    scam_embed.set_thumbnail(url="https://tr.rbxcdn.com/180DAY-b83def7a95453c80e50a0ecb30adb62d/420/420/Hat/Png/noFilter")\
\
    # Buttons for accept/decline\
    class InviteButtons(ui.View):\
        def __init__(self):\
            super().__init__(timeout=None)  # buttons never expire\
\
        @ui.button(label="Accept", style=ButtonStyle.success)\
        async def accept(self, interaction: Interaction, button: ui.Button):\
            await interaction.response.send_message("Welcome to the team!", ephemeral=True)\
\
            welcome_embed = discord.Embed(\
                title="Welcome to our team",\
                description="Type `$howto` in the chat to learn how to hit\\nYou are now an official hitter for our team.",\
                color=MAIN_COLOR\
            )\
            welcome_embed.set_thumbnail(url=PLACEHOLDER_ICON)\
            await interaction.channel.send(embed=welcome_embed)\
\
            self.stop()\
\
        @ui.button(label="Decline", style=ButtonStyle.danger)\
        async def decline(self, interaction: Interaction, button: ui.Button):\
            await interaction.response.send_message("You have declined and will be banned.", ephemeral=True)\
            try:\
                await interaction.user.ban(reason="Declined invite")\
            except Exception:\
                await interaction.followup.send("Failed to ban user.", ephemeral=True)\
            self.stop()\
\
    # send the embed with the buttons\
    await ctx.send(embed=scam_embed, view=InviteButtons())\
\
\
\
IMAGE_URL = "https://images-ext-1.discordapp.net/external/S-ZMbRm7QIaDWnEiuN5ZPNQrXOz0vBAIeXIIZitNfC8/%3Fformat%3Dwebp%26quality%3Dlossless%26width%3D387%26height%3D387/https/images-ext-1.discordapp.net/external/6Dtval-9vtswsuE-cWp67CwjvLRqCH5ZRbEQiEEFDj8/%253Fsize%253D1024/https/cdn.discordapp.com/icons/1437030353674965097/45a3aa89511f4e2fdc5f88a07a1b5296.png?format=webp&quality=lossless&width=387&height=387"\
\
# store channel ids per server\
server_channels = \{\}\
\
def random_robux():\
    return random.randint(50, 5000)\
\
def robux_to_usd(robux):\
    return round((robux / 1000) * 4, 2)\
\
def random_user_id():\
    return random.randint(100000000, 999999999)\
\
def random_transaction_id():\
    return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=12))\
\
@bot.command()\
async def completed(ctx, action=None, channel: discord.TextChannel=None):\
    if action == "set" and channel:\
        server_channels[ctx.guild.id] = channel.id\
        await ctx.send(f"
\f1 \uc0\u9989 
\f0  completed logs will now send to \{channel.mention\}")\
    else:\
        await ctx.send("usage: `$completed set #channel`")\
\
@bot.event\
async def on_ready():\
    print(f"logged in as \{bot.user\}")\
    send_fake_embed.start()\
\
@tasks.loop(seconds=60)\
async def send_fake_embed():\
    await asyncio.sleep(random.randint(60, 300))  # wait 1-5 min before posting\
\
    for guild_id, channel_id in server_channels.items():\
        channel = bot.get_channel(channel_id)\
        if not channel:\
            continue\
\
        robux_amount = random_robux()\
        usd_value = robux_to_usd(robux_amount)\
        sender = random_user_id()\
        receiver = random_user_id()\
        transaction_id = random_transaction_id()\
\
        embed = discord.Embed(\
            title=" Roblox Deal Completed ",\
            color=MAIN_COLOR,\
            timestamp=datetime.now(timezone.utc)\
        )\
        embed.set_thumbnail(url=IMAGE_URL)\
        embed.add_field(\
            name="
\f1 \uc0\u55357 \u56496 
\f0  Amount",\
            value=f"`\{robux_amount\}` Rbx ($\{usd_value\} USD)",\
            inline=False\
        )\
        embed.add_field(\
            name="
\f1 \uc0\u55357 \u56420 
\f0  Sender",\
            value=f"`\{sender\}`",\
            inline=True\
        )\
        embed.add_field(\
            name="
\f1 \uc0\u55357 \u56421 
\f0  Receiver",\
            value=f"`\{receiver\}`",\
            inline=True\
        )\
        embed.add_field(\
            name="
\f1 \uc0\u55356 \u56724 
\f0  Transaction ID",\
            value=f"`\{transaction_id\}`",\
            inline=False\
        )\
        embed.set_footer(text="Roblox Transaction Logger")\
        embed.set_author(name="System")\
\
        await channel.send(embed=embed)\
\
@bot.command()\
async def rs(ctx):\
    await ctx.message.delete()  # delete the user command message\
\
    robux_amount = random_robux()\
    usd_value = robux_to_usd(robux_amount)\
    sender = random_user_id()\
    receiver = random_user_id()\
    transaction_id = random_transaction_id()\
\
    embed = discord.Embed(\
        title=" Roblox Deal Completed ",\
        color=MAIN_COLOR,\
        timestamp=datetime.now(timezone.utc)\
    )\
    embed.set_thumbnail(url=IMAGE_URL)\
    embed.add_field(\
        name="
\f1 \uc0\u55357 \u56496 
\f0  Amount",\
        value=f"`\{robux_amount\}` Rbx ($\{usd_value\} USD)",\
        inline=False\
    )\
    embed.add_field(\
        name="
\f1 \uc0\u55357 \u56420 
\f0  Sender",\
        value=f"`\{sender\}`",\
        inline=True\
    )\
    embed.add_field(\
        name="
\f1 \uc0\u55357 \u56421 
\f0  Receiver",\
        value=f"`\{receiver\}`",\
        inline=True\
    )\
    embed.add_field(\
        name="
\f1 \uc0\u55356 \u56724 
\f0  Transaction ID",\
        value=f"`\{transaction_id\}`",\
        inline=False\
    )\
    embed.set_footer(text="Roblox Transaction Logger")\
    embed.set_author(name="System")\
\
    await ctx.send(embed=embed)\
\
\
\
@bot.command()\
async def invitebot(ctx):\
    invite_url = "https://discord.com/oauth2/authorize?client_id=1437033327570849974&permissions=8&integration_type=0&scope=bot"\
\
    embed = discord.Embed(\
        title="Invite Dribble Bot",\
        description=f"[Click here to invite me to your server](\{invite_url\})",\
        color=MAIN_COLOR\
    )\
    embed.set_footer(text="Dribble Bot Service")\
    embed.set_thumbnail(url=IMAGE_URL)\
\
    await ctx.send(embed=embed)\
\
\
\
from dotenv import load_dotenv\
import os\
\
load_dotenv("token.env")  # loads your token.env file\
BOT_TOKEN = os.getenv("BOT_TOKEN")\
\
bot.run(BOT_TOKEN)\
\
\
\
}