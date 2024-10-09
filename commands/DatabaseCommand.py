import asyncio
import os
import json
import discord # type: ignore

class DatabaseCommand:
    def __init__(self, client):
        self.client = client
        self.database = client.create_group("database", "Manage the bot database")
        self.register_commands()

    def register_commands(self):
        @self.database.command(name="clear", description="Clear the bot database")
        async def database_clear(ctx: discord.ApplicationContext):
            if ctx.author.guild_permissions.administrator:
                server_id = ctx.guild_id
                directory = "databases"
                filename = f"{directory}/wordsdb_{server_id}.json"
                if os.path.exists(filename):
                    os.remove(filename)
                    await ctx.respond("Database has been cleared.", ephemeral=True)
                else:
                    await ctx.respond("Database does not exist.", ephemeral=True)
            else:
                await ctx.respond("You do not have permission to use this command.", ephemeral=True)

        @self.database.command(name="download", description="Download the bot database")
        async def database_download(ctx: discord.ApplicationContext):
            if ctx.author.guild_permissions.administrator:
                server_id = ctx.guild_id
                directory = "databases"
                filename = f"{directory}/wordsdb_{server_id}.json"
                if os.path.exists(filename):
                    await ctx.respond(file=discord.File(filename), ephemeral=True)
                else:
                    await ctx.respond("Database does not exist.", ephemeral=True)
            else:
                await ctx.respond("You do not have permission to use this command.", ephemeral=True)

        @self.database.command(name="upload", description="Upload a new bot database")
        async def database_upload(ctx: discord.ApplicationContext, attachment: discord.Attachment):
            if ctx.author.guild_permissions.administrator:
                server_id = ctx.guild_id
                directory = "databases"
                filename = f"{directory}/wordsdb_{server_id}.json"
                temp_filename = f"{directory}/temp_{server_id}.json"
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                if not os.path.exists(directory):
                    os.makedirs(directory)
                await attachment.save(temp_filename)
                with open(temp_filename, 'r') as temp_file:
                    temp_data = json.load(temp_file)
                if temp_data.get("server_id") == server_id:
                    if os.path.exists(filename):
                        await ctx.respond("A database already exists. Are you sure you want to overwrite it? Respond with 'yes' or 'no'.", ephemeral=True)
                    def check(m):
                        return m.author == ctx.author and m.content.lower() in ["yes", "no"]
                    try:
                        msg = await self.client.wait_for('message', check=check, timeout=30)
                        if msg.content.lower() == "yes":
                            os.rename(temp_filename, filename)
                            await ctx.respond("Database has been uploaded.", ephemeral=True)
                        else:
                            os.remove(temp_filename)
                            await ctx.respond("Upload cancelled.", ephemeral=True)
                    except asyncio.TimeoutError:
                        os.remove(temp_filename)
                        await ctx.respond("You took too long to respond. Upload cancelled.", ephemeral=True)
                    else:
                        os.rename(temp_filename, filename)
                        await ctx.respond("Database has been uploaded.", ephemeral=True)
                else:                    
                    embed = discord.Embed(
                        title="Overwrite Database",
                        description="The uploaded database does not match this server. Do you still want to overwrite the existing database?",
                        color=discord.Color.red()
                    )
                    view = discord.ui.View()
                    yes_button = discord.ui.Button(label="Yes", style=discord.ButtonStyle.green)
                    no_button = discord.ui.Button(label="No", style=discord.ButtonStyle.red)

                    async def yes_button_callback(interaction):
                        if interaction.user == ctx.author:
                            if os.path.exists(filename):
                                os.remove(filename)
                            os.rename(temp_filename, filename)
                            await interaction.response.edit_message(content="Database has been uploaded.", embed=None, view=None)
                        else:
                            await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)

                    async def no_button_callback(interaction):
                        if interaction.user == ctx.author:
                            os.remove(temp_filename)
                            await interaction.response.edit_message(content="Upload cancelled.", embed=None, view=None)
                        else:
                            await interaction.response.send_message("You cannot interact with this button.", ephemeral=True)

                    yes_button.callback = yes_button_callback
                    no_button.callback = no_button_callback

                    view.add_item(yes_button)
                    view.add_item(no_button)

                    await ctx.respond(embed=embed, view=view, ephemeral=True)
            else:
                await ctx.respond("You do not have permission to use this command.", ephemeral=True)
