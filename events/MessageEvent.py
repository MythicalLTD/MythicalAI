import asyncio
import os
import json
import random
import discord  # type: ignore
import colorama  # type: ignore
import helpers.ColorHelper as ColorHelper

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
            server_name = message.guild.name
            directory = "databases"
            filename = f"{directory}/wordsdb_{server_id}.json"
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

            if self.client.user in message.mentions:
                if len(data["words"]) >= 100:
                    num_words = min(random.randint(1, 5), len(data["words"]))
                    expression = " ".join(random.sample(data["words"], num_words))
                    await message.channel.send(expression)
                    if debug:
                        print(showColorOutput(f'Responded to mention with expression: {expression}', "green"))
                counter = 0
