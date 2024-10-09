import os
import discord # type: ignore
import asyncio
import random
import re
from dotenv import load_dotenv # type: ignore
import colorama # type: ignore

load_dotenv()
colorama.init()


def showColorOutput(text, color=None):
    if text is None:
        return "None"
    if color:
        return f'{getattr(colorama.Fore, color.upper(), colorama.Fore.RESET)}{text}{colorama.Style.RESET_ALL}'
    return text

discord_token = os.getenv("TOKEN")
activity_message = os.getenv("ACTIVITY")
if discord_token is None:
    print(showColorOutput("No token found", "red"))
    exit()

activity = discord.Game(name=activity_message)
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
client = discord.Bot(command_prefix=">", activity=activity, intents=intents)
bot_id = None
counter = 0

def escape_string(word):
    # escape double quotes in the word with a backslash
    return word.replace('"', r'\"')

@client.event
async def on_ready():
    global bot_id
    bot_id = client.user.id
    print("--------------")
    print(showColorOutput(f'We have logged in as {client.user}', "green"))
    print(showColorOutput(f'Bot ID: {bot_id}', "blue"))
    print(showColorOutput(f'Activity: {activity_message}', "yellow"))
    print(showColorOutput(f'Invite URL: https://discord.com/oauth2/authorize?client_id={bot_id}&permissions=412317222976&integration_type=0&scope=bot+applications.commands', "cyan"))
    print("--------------")

@client.event
async def on_message(message):
    global counter
    debug = os.getenv("DEBUG", "false").lower() == "true"

    server_id = message.guild.id
    directory = "databases"
    filename = f"{directory}/wordsdb_{server_id}.txt"
    if debug:
        print(showColorOutput(f'[{server_id}] Message from {message.author}: {message.content}', "magenta"))
    # create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # store each word in a words database for this server
    if message.author != client.user:
        if message.content:
            words = message.content.split()
        else:
            words = []
        with open(filename, "a") as f:
            for word in words:
                if word != f"<@{bot_id}>" and message.author.id != int(bot_id):
                    escaped_word = escape_string(word)
                    f.write(f'{escaped_word} ')
                    if debug:
                        print(showColorOutput(f'Saved word: {escaped_word}', "blue"))
                else: 
                    if debug:
                        print(showColorOutput(f'Ignored word: {word}', "yellow"))

    # increment the counter
    counter += 1

    # send an expression when the counter reaches 30
    if counter >= 30:
        with open(filename, "r") as f:
            words_str = f.read()
            words = words_str.split()
            if len(words) >= 100:
                num_words = min(random.randint(1, 5), len(words))
                expression = " ".join(random.sample(words, num_words))
                await message.channel.send(expression)
                if debug:
                    print(showColorOutput(f'Sent expression: {expression}', "green"))
            counter = 0

    # respond to mention
    if client.user in message.mentions:
        with open(filename, "r") as f:
            words_str = f.read()
            words = words_str.split()
            if len(words) >= 100:
                num_words = min(random.randint(1, 5), len(words))
                expression = " ".join(random.sample(words, num_words))
                await message.channel.send(expression)
                if debug:
                    print(showColorOutput(f'Responded to mention with expression: {expression}', "green"))
            counter = 0

@client.slash_command(name="hello", description="Say hello to the bot", guild_ids=[int(os.getenv("GUILD_ID"))])
async def hello(ctx: discord.ApplicationContext):
    await ctx.respond("Hey!")


@client.slash_command(name="ping", description="Show the bot's ping", guild_ids=[int(os.getenv("GUILD_ID"))])
async def ping(ctx: discord.ApplicationContext):
    latency = client.latency * 1000  # Convert to milliseconds
    await ctx.respond(f':ping_pong: Pong! {latency:.2f}ms')

database = client.create_group("database", "Manage the bot database")

@database.command(name="clear", description="Clear the bot database")
async def database_clear(ctx: discord.ApplicationContext):
    if ctx.author.guild_permissions.administrator:
        server_id = ctx.guild_id
        directory = "databases"
        filename = f"{directory}/wordsdb_{server_id}.txt"
        if os.path.exists(filename):
            os.remove(filename)
            await ctx.respond("Database has been cleared.", ephemeral=True)
        else:
            await ctx.respond("Database does not exist.", ephemeral=True)
    else:
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)

@database.command(name="download", description="Download the bot database")
async def database_download(ctx: discord.ApplicationContext):
    if ctx.author.guild_permissions.administrator:
        server_id = ctx.guild_id
        directory = "databases"
        filename = f"{directory}/wordsdb_{server_id}.txt"
        if os.path.exists(filename):
            await ctx.respond(file=discord.File(filename), ephemeral=True)
        else:
            await ctx.respond("Database does not exist.", ephemeral=True)
    else:
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)

@database.command(name="upload", description="Upload a new bot database")
async def database_upload(ctx: discord.ApplicationContext, attachment: discord.Attachment):
    if ctx.author.guild_permissions.administrator:
        server_id = ctx.guild_id
        directory = "databases"
        filename = f"{directory}/wordsdb_{server_id}.txt"
        if not os.path.exists(directory):
            os.makedirs(directory)
        await attachment.save(filename)
        await ctx.respond("Database has been uploaded.", ephemeral=True)
    else:
        await ctx.respond("You do not have permission to use this command.", ephemeral=True)

client.run(discord_token)