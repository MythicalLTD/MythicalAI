import os
import discord # type: ignore
from dotenv import load_dotenv # type: ignore
from commands.DatabaseCommand import DatabaseCommand
from commands.PingCommand import PingCommand
from events.MessageEvent import MessageEvent
from events.onReady import onReady

load_dotenv()

discord_token = os.getenv("TOKEN")
activity_message = os.getenv("ACTIVITY")
register_commands = os.getenv("REGISTER_COMMANDS_ONLY_GUILD")

# Intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Initialize the bot
client = discord.Bot(
    command_prefix=">", 
    activity=discord.Game(name=activity_message), 
    intents=intents
)

# Register events
onReady(client)
MessageEvent(client)

# Register commands
DatabaseCommand(client)
PingCommand(client)

client.run(discord_token)