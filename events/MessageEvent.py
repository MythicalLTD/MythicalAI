import asyncio
import os
import json
import random
import discord  # type: ignore
import colorama  # type: ignore
import helpers.ColorHelper as ColorHelper
import helpers.BannedGuilds as BannedGuilds
import helpers.SettingsHelper as SettingsHelper

class MessageEvent:
    def __init__(self, client):
        self.client = client
        ColorHelper.ColorHelper.print_colored_message("Registering Message event...", "gray")
        try :
            self.register_event()
            ColorHelper.ColorHelper.print_colored_message("Message event registered", "green")
        except Exception as e:
            ColorHelper.ColorHelper.print_colored_message(f"Error registering Message event: {e}", "red")
            exit()
    
    def register_event(self):
        def escape_string(word):
            # escape double quotes in the word with a backslash
            return word.replace('"', r'\"')
        def showColorOutput(text, color=None):
            if text is None:
                return "None"
            if color:
                return f'{getattr(colorama.Fore, color.upper(), colorama.Fore.RESET)}{text}{colorama.Style.RESET_ALL}'
            return text
        
        

        @self.client.event
        async def on_message(message):
            counter = 0
            
            bot_id = self.client.user.id

            if message.author.bot:
                return
            if message.guild is None:
                return
            server_id = message.guild.id
            isEnabled = SettingsHelper.SettingsHelper.get_setting(server_id, "bot_enabled")
            if not isEnabled:
                return
            
            if not message.channel.permissions_for(message.guild.me).send_messages:
                owner = message.guild.owner
                if owner:
                    # Check if the bot has already sent a message to the owner about this channel
                    already_notified_key = f"notified_{message.guild.id}_{message.channel.id}"
                    if not hasattr(self.client, 'already_notified'):
                        self.client.already_notified = set()
                    
                    if already_notified_key not in self.client.already_notified:
                        try:
                            await owner.send(f"Hi {owner.name}, I don't have permission to send messages in <#{message.channel.id}> on your server `{message.guild.name}`. Please update my permissions.")
                            self.client.already_notified.add(already_notified_key)
                        except discord.Forbidden:
                            print(showColorOutput(f"Could not send a message to the server owner about missing permissions in {message.channel.name}.", "red"))
                return
            server_id = message.guild.id
            server_name = message.guild.name
            directory = "databases/words"
            filename = f"{directory}/{server_id}.json"
            debug = os.getenv("DEBUG") == "true"
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

            if message.author != self.client.user:
                if message.content:
                    words = message.content.split()
                else:
                    words = []
                for word in words:
                    if word not in ["@everyone", "@here"] and not word.startswith("<@&") and word != f"<@{bot_id}>" and message.author.id != int(bot_id):
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
                    async with message.channel.typing():
                        await asyncio.sleep(random.randint(1, 4))
                    if (BannedGuilds.BannedGuilds.is_banned(server_id)):
                        reason = BannedGuilds.BannedGuilds.getBanReason(server_id)
                        await message.channel.send(f"Sorry, This guild is banned form using this bot: {reason}")
                        return
                    await message.channel.send(expression)
                    if debug:
                        print(showColorOutput(f'Sent expression: {expression}', "green"))
                else:
                    if debug:
                        print(showColorOutput(f'Not enough words to send an expression', "yellow"))
                    await message.add_reaction("🕒")
                    try:
                        await message.author.send("There are not enough words to respond with an expression at the moment. Please try again later.")
                        if debug:
                            print(showColorOutput(f'Sent DM to {message.author} about not enough words', "green"))
                    except discord.Forbidden:
                        if debug:
                            print(showColorOutput(f'Could not send a DM to {message.author}', "red"))
                counter = 0

            if self.client.user in message.mentions:
                if len(data["words"]) >= 100:
                    num_words = min(random.randint(1, 5), len(data["words"]))
                    expression = " ".join(random.sample(data["words"], num_words))
                    async with message.channel.typing():
                        await asyncio.sleep(random.randint(1, 4))
                    if (BannedGuilds.BannedGuilds.is_banned(server_id)):
                        reason = BannedGuilds.BannedGuilds.getBanReason(server_id)
                        await message.channel.send(f"Sorry, This guild is banned form using this bot: {reason}")
                        return
                    await message.channel.send(expression)
                    if debug:
                        print(showColorOutput(f'Responded to mention with expression: {expression}', "green"))
                else:
                    if debug:
                        print(showColorOutput(f'Not enough words to send an expression', "yellow"))
                    await message.add_reaction("🕒")
                    try:
                        await message.author.send("There are not enough words to respond with an expression at the moment. Please try again later.")
                        if debug:
                            print(showColorOutput(f'Sent DM to {message.author} about not enough words', "green"))
                    except discord.Forbidden:
                        if debug:
                            print(showColorOutput(f'Could not send a DM to {message.author}', "red"))
                counter = 0
