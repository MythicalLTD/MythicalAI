import asyncio
import os
import json
import discord # type: ignore
import helpers.BannedGuilds as BannedGuilds
import helpers.ColorHelper as ColorHelper


class OwnerCommand:
    def __init__(self, client):
        self.client = client
        ColorHelper.ColorHelper.print_colored_message(
            "Registering Owner command...", "gray"
        )
        try:
            self.ownerCommand = client.create_group("owner", "Manage the bot behavior!", guild_ids=[1276929020835008603])
            self.register_commands()
            ColorHelper.ColorHelper.print_colored_message(
                "Owner command registered", "green"
            )
        except Exception as e:
            ColorHelper.ColorHelper.print_colored_message(
                f"Error registering owner command: {e}", "red"
            )
            exit()

    def register_commands(self):
        @self.ownerCommand.command(name="reboot", description="Reboot the bot", guild_ids=[1276929020835008603])
        async def owner_reboot(ctx: discord.ApplicationContext):
            owner_id = os.getenv("OWNER_ID")
            if ctx.author.id == int(owner_id):
                await ctx.respond("Rebooting...", ephemeral=True)
                await self.client.close()
            else:
                await ctx.respond("You are not the owner of the bot!", ephemeral=True)
                ColorHelper.ColorHelper.print_colored_message(f"The user {ctx.author.id} tried to use a owner command!", "red")

        @self.ownerCommand.command(name="shutdown", description="Shutdown the bot", guild_ids=[1276929020835008603])
        async def owner_shutdown(ctx: discord.ApplicationContext):
            owner_id = os.getenv("OWNER_ID")
            if ctx.author.id == int(owner_id):
                await ctx.respond("Shutting down...", ephemeral=True)
                await self.client.close()
            else:
                await ctx.respond("You are not the owner of the bot!", ephemeral=True)
                ColorHelper.ColorHelper.print_colored_message(f"The user {ctx.author.id} tried to use a owner command!", "red")

        @self.ownerCommand.command(name="update_activity", description="Update the bot's activity", guild_ids=[1276929020835008603])
        async def owner_update(ctx: discord.ApplicationContext, activity: str):
            owner_id = os.getenv("OWNER_ID")
            if ctx.author.id == int(owner_id):
                await ctx.respond("Updating...", ephemeral=True)
                await self.client.change_presence(activity=discord.Game(name=activity))
            else:
                await ctx.respond("You are not the owner of the bot!", ephemeral=True)
                ColorHelper.ColorHelper.print_colored_message(f"The user {ctx.author.id} tried to use a owner command!", "red")

        @self.ownerCommand.command(name="eval", description="Run a script", guild_ids=[1276929020835008603])
        async def owner_eval(ctx: discord.ApplicationContext, script: str):
            owner_id = os.getenv("OWNER_ID")
            if ctx.author.id == int(owner_id):
                try:
                    result = eval(script)
                    await ctx.respond(f"Result: {result}", ephemeral=True)
                except Exception as e:
                    await ctx.respond(f"Error: {e}", ephemeral=True)
            else:
                await ctx.respond("You are not the owner of the bot!", ephemeral=True)
                ColorHelper.ColorHelper.print_colored_message(f"The user {ctx.author.id} tried to use a owner command!", "red")

        @self.ownerCommand.command(name="update_username", description="Set the bot's username", guild_ids=[1276929020835008603])
        async def owner_username(ctx: discord.ApplicationContext, username: str):
            owner_id = os.getenv("OWNER_ID")
            if ctx.author.id == int(owner_id):
                try:
                    await ctx.respond("Updating...", ephemeral=True)
                    await self.client.user.edit(username=username)
                    ColorHelper.ColorHelper.print_colored_message(f"Username updated to {username}", "green")
                except discord.HTTPException as e:
                    await ctx.respond(f"Failed to update username: {e}", ephemeral=True)
                    ColorHelper.ColorHelper.print_colored_message(f"Failed to update username: {e}", "red")
            else:
                await ctx.respond("You are not the owner of the bot!", ephemeral=True)
                ColorHelper.ColorHelper.print_colored_message(f"The user {ctx.author.id} tried to use a owner command!", "red")

        @self.ownerCommand.command(name="guild_ban", description="Ban a guild from using the bot", guild_ids=[1276929020835008603])
        async def owner_ban_guild(ctx: discord.ApplicationContext, guild_id: str, reason: str = "No reason provided"):
            owner_id = os.getenv("OWNER_ID")
            if owner_id and ctx.author.id == int(owner_id):
                try:
                    guild_id = int(guild_id)
                    guild = self.client.get_guild(guild_id)
                    if guild:
                        ColorHelper.ColorHelper.print_colored_message(f"Banned guild: {guild.name}", "green")
    
                        # Create the directory if it doesn't exist
                        os.makedirs("databases", exist_ok=True)
                        
                        if (BannedGuilds.BannedGuilds.is_banned(guild_id) == True):
                            await ctx.respond("Guild already banned", ephemeral=True)
                            ColorHelper.ColorHelper.print_colored_message("Guild already banned", "yellow")
                            return
                        else:
                            BannedGuilds.BannedGuilds.ban_guild(guild_id, reason)
                            await ctx.respond(f"Banned guild: {guild.name}", ephemeral=True)
                    else:
                        await ctx.respond("Guild not found", ephemeral=True)
                        ColorHelper.ColorHelper.print_colored_message("Guild not found", "red")
                except discord.HTTPException as e:
                    await ctx.respond(f"Failed to ban guild: {e}", ephemeral=True)
                    ColorHelper.ColorHelper.print_colored_message(f"Failed to ban guild: {e}", "red")
            else:
                await ctx.respond("You are not the owner of the bot!", ephemeral=True)
                ColorHelper.ColorHelper.print_colored_message(f"The user {ctx.author.id} tried to use a owner command!", "red")
        @self.ownerCommand.command(name="guild_unban", description="Unban a guild from using the bot", guild_ids=[1276929020835008603])
        async def owner_unban_guild(ctx: discord.ApplicationContext, guild_id: str):
            owner_id = os.getenv("OWNER_ID")
            if owner_id and ctx.author.id == int(owner_id):
                try:
                    guild_id = int(guild_id)
                    guild = self.client.get_guild(guild_id)
                    if guild:
                        ColorHelper.ColorHelper.print_colored_message(f"Unbanned guild: {guild.name}", "green")
    
                        # Create the directory if it doesn't exist
                        os.makedirs("databases", exist_ok=True)
                        
                        if (BannedGuilds.BannedGuilds.is_banned(guild_id) == False):
                            await ctx.respond("Guild already unbanned", ephemeral=True)
                            ColorHelper.ColorHelper.print_colored_message("Guild already unbanned", "yellow")
                            return
                        else:
                            BannedGuilds.BannedGuilds.unban_guild(guild_id)
                            await ctx.respond(f"Unbanned guild: {guild.name}", ephemeral=True)
                    else:
                        await ctx.respond("Guild not found", ephemeral=True)
                        ColorHelper.ColorHelper.print_colored_message("Guild not found", "red")
                except discord.HTTPException as e:
                    await ctx.respond(f"Failed to unban guild: {e}", ephemeral=True)
                    ColorHelper.ColorHelper.print_colored_message(f"Failed to unban guild: {e}", "red")
            else:
                await ctx.respond("You are not the owner of the bot!", ephemeral=True)
                ColorHelper.ColorHelper.print_colored_message(f"The user {ctx.author.id} tried to use a owner command!", "red")
