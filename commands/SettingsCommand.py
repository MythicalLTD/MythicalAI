import helpers.ColorHelper as ColorHelper
import discord # type: ignore
import os
import helpers.SettingsHelper as SettingsHelper

class SettingsCommand:
    def __init__(self, client):
        self.client = client
        ColorHelper.ColorHelper.print_colored_message("Registering Settings command...", "gray")
        try :
            self.register_commands()
            ColorHelper.ColorHelper.print_colored_message("Settings command registered", "green")
        except Exception as e:
            ColorHelper.ColorHelper.print_colored_message(f"Error registering Settings command: {e}", "red")
            exit()

    def register_commands(self):
        @self.client.slash_command(name="settings", description="Customize bot settings")
        async def settings(ctx: discord.ApplicationContext):
            embed = discord.Embed(title="Bot Settings", description="Select an option to customize:", color=discord.Color.blue())
            if not ctx.author.guild_permissions.administrator:
                await ctx.respond("You do not have permission to use this command.", ephemeral=True)
                return
            bot_enabled = SettingsHelper.SettingsHelper.get_setting(ctx.guild.id, "bot_enabled")
            if (bot_enabled == False):
                status_text = "Disabled"
                button1 = discord.ui.Button(label="Enable bot", style=discord.ButtonStyle.primary)
            else:
                status_text = "Enabled"
                button1 = discord.ui.Button(label="Disable bot", style=discord.ButtonStyle.primary)


            embed.add_field(name="Toggle Bot", value=f"Status: {status_text}", inline=False)
            embed.set_footer(text="Use the buttons below to navigate.")
            view = discord.ui.View()

            async def button1_callback(interaction):
                if (bot_enabled == False):
                    SettingsHelper.SettingsHelper.set_setting(ctx.guild.id, "bot_enabled", True)
                    await interaction.response.send_message("You enabled the bot", ephemeral=True)
                else:
                    SettingsHelper.SettingsHelper.set_setting(ctx.guild.id, "bot_enabled", False)
                    await interaction.response.send_message("You disabled the bot", ephemeral=True)

            button1.callback = button1_callback
            view.add_item(button1)

            await ctx.respond(embed=embed, view=view, ephemeral=True)