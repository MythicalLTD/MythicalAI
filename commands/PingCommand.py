import asyncio
import os
import json
import discord # type: ignore

class PingCommand:
    def __init__(self, client):
        self.client = client
        self.register_commands()

    def register_commands(self):
        @self.client.slash_command(name="ping", description="Check the bot's latency")
        async def ping(ctx: discord.ApplicationContext):
            latency = round(self.client.latency * 1000)  # Convert to milliseconds
            await ctx.respond(f"Pong! Latency is {latency}ms", ephemeral=True)