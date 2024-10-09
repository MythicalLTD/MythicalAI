import os
import discord # type: ignore
import asyncio
import random
import re
from dotenv import load_dotenv # type: ignore
from commands.DatabaseCommand import DatabaseCommand
import json
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
    if message.author.bot:
        return
    if message.guild is None:
        return

    server_id = message.guild.id
    server_name = message.guild.name
    directory = "databases"
    filename = f"{directory}/wordsdb_{server_id}.json"
    if debug:
        print(showColorOutput(f'[{server_id}] Message from {message.author}: {message.content}', "magenta"))

    # create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # load existing data or initialize new data
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
    else:
        data = {
            "server_id": server_id,
            "server_name": server_name,
            "words": []
        }

    # store each word in a words database for this server
    if message.author != client.user:
        if message.content:
            words = message.content.split()
        else:
            words = []
        for word in words:
            if word != f"<@{bot_id}>" and message.author.id != int(bot_id):
                escaped_word = escape_string(word)
                data["words"].append(escaped_word)
                if debug:
                    print(showColorOutput(f'Saved word: {escaped_word}', "blue"))
            else:
                if debug:
                    print(showColorOutput(f'Ignored word: {word}', "yellow"))

    # save data back to the file
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    # increment the counter
    counter += 1

    # send an expression when the counter reaches 30
    if counter >= 30:
        if len(data["words"]) >= 100:
            num_words = min(random.randint(1, 5), len(data["words"]))
            expression = " ".join(random.sample(data["words"], num_words))
            await message.channel.send(expression)
            if debug:
                print(showColorOutput(f'Sent expression: {expression}', "green"))
        counter = 0

    # respond to mention
    if client.user in message.mentions:
        if len(data["words"]) >= 100:
            num_words = min(random.randint(1, 5), len(data["words"]))
            expression = " ".join(random.sample(data["words"], num_words))
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

DatabaseCommand(client)

client.run(discord_token)