import os
import discord # type: ignore
from dotenv import load_dotenv # type: ignore
from commands.DatabaseCommand import DatabaseCommand
from commands.PingCommand import PingCommand
from events.MessageEvent import MessageEvent
from events.onReady import onReady
from events.onJoin import onJoin
from helpers.ColorHelper import ColorHelper
from helpers.AsciiArt import AsciiArt
import helpers.SettingsHelper as SettingsHelper
from commands.SettingsCommand import SettingsCommand
from events.onLeave import onLeave
from commands.OwnerCommand import OwnerCommand # type: ignore

AsciiArt.print_logo()

ColorHelper.print_colored_message("Starting the bot...", "gray")
ColorHelper.print_colored_message("Loading env...", "gray")
load_dotenv()
ColorHelper.print_colored_message("Env loaded", "green")


discord_token = os.getenv("TOKEN")
activity_message = os.getenv("ACTIVITY")
register_commands = os.getenv("REGISTER_COMMANDS_ONLY_GUILD")

# Intents
ColorHelper.print_colored_message("Setting up intents...", "gray")
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
ColorHelper.print_colored_message("Intents set up", "green")

ColorHelper.print_colored_message("Initializing the bot...", "gray")
# Initialize the bot
client = discord.Bot(
    command_prefix=">", 
    activity=discord.Game(name=activity_message), 
    intents=intents
)

ColorHelper.print_colored_message("Bot initialized", "green")


# Register events
onReady(client)
MessageEvent(client)
onJoin(client)
onLeave(client)

# Register commands
DatabaseCommand(client)
PingCommand(client)
SettingsCommand(client)
OwnerCommand(client)

client.run(discord_token)