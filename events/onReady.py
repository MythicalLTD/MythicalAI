import asyncio
import os
import json
import random
import discord  # type: ignore
import colorama  # type: ignore

class onReady:
    def __init__(self, client):
        self.client = client
        self.register_event()
    
    def register_event(self):
        def showColorOutput(text, color=None):
            if text is None:
                return "None"
            if color:
                return f'{getattr(colorama.Fore, color.upper(), colorama.Fore.RESET)}{text}{colorama.Style.RESET_ALL}'
            return text
        
        @self.client.event
        async def on_ready():
            print("--------------")
            print(showColorOutput(f'We have logged in as {self.client.user}', "green"))
            print(showColorOutput(f'Bot ID: {self.client.user.id}', "blue"))
            print(showColorOutput(f'Invite URL: https://discord.com/oauth2/authorize?client_id={self.client.user.id}&permissions=412317222976&integration_type=0&scope=bot+applications.commands', "cyan"))
            print("--------------")