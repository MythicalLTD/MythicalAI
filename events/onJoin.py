import colorama  # type: ignore
import helpers.ColorHelper as ColorHelper
import helpers.SettingsHelper as SettingsHelper

class onJoin:
    def __init__(self, client):
        self.client = client
        ColorHelper.ColorHelper.print_colored_message("Registering onJoin event...", "gray")
        try: 
            self.register_event()
            ColorHelper.ColorHelper.print_colored_message("onJoin event registered", "green")
        except Exception as e:
            ColorHelper.ColorHelper.print_colored_message(f"Error registering onJoin event: {e}", "red")
            exit()
    
    def register_event(self):
        @self.client.event
        async def on_guild_join(guild):
            ColorHelper.ColorHelper.print_colored_message(f"Joined new guild: {guild.name}", "blue")
            SettingsHelper.SettingsHelper.init_settings(guild.id, {"bot_enabled": True})
            print("--------------")
            ColorHelper.ColorHelper.print_colored_message(f'Server name: {guild.name}', "yellow")
            ColorHelper.ColorHelper.print_colored_message(f'Server ID: {guild.id}', "magenta")
            ColorHelper.ColorHelper.print_colored_message(f'Total Users: {guild.member_count}', "cyan")
            print("--------------")
            ColorHelper.ColorHelper.print_colored_message(f'Total Guilds: {len(self.client.guilds)}', "green")
            ColorHelper.ColorHelper.print_colored_message(f'Total Users: {len(self.client.users)}', "blue")
            print("--------------")
            # Additional logic for when the bot joins a new guild can be added here