import asyncio
import os
import json
import discord # type: ignore
import helpers.ColorHelper as ColorHelper


class PingCommand:
    def __init__(self, client):
        self.client = client
        ColorHelper.ColorHelper.print_colored_message("Registering Ping command...", "gray")
        try :
            self.register_commands()
            ColorHelper.ColorHelper.print_colored_message("Ping command registered", "green")
        except Exception as e:
            ColorHelper.ColorHelper.print_colored_message(f"Error registering Ping command: {e}", "red")
            exit()

    def register_commands(self):
        @self.client.slash_command(name="ping", description="Check the bot's latency")
        async def ping(ctx: discord.ApplicationContext):
            latency = round(self.client.latency * 1000)  # Convert to milliseconds
            await ctx.respond(f"Pong! Latency is {latency}ms", ephemeral=True)