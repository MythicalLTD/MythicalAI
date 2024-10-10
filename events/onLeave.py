import colorama  # type: ignore
import helpers.ColorHelper as ColorHelper
import helpers.SettingsHelper as SettingsHelper
import os

class onLeave:
    def __init__(self, client):
        self.client = client
        ColorHelper.ColorHelper.print_colored_message("Registering OnLeave event...", "gray")
        try: 
            self.register_event()
            ColorHelper.ColorHelper.print_colored_message("OnLeave event registered", "green")
        except Exception as e:
            ColorHelper.ColorHelper.print_colored_message(f"Error registering OnLeave event: {e}", "red")
            exit()
    
    def register_event(self):
        @self.client.event
        async def on_guild_remove(guild):
            ColorHelper.ColorHelper.print_colored_message(f"Left guild: {guild.name}", "blue")
            print("--------------")
            ColorHelper.ColorHelper.print_colored_message(f'Server name: {guild.name}', "yellow")
            ColorHelper.ColorHelper.print_colored_message(f'Server ID: {guild.id}', "magenta")
            ColorHelper.ColorHelper.print_colored_message(f'Total Users: {guild.member_count}', "cyan")
            print("--------------")
            ColorHelper.ColorHelper.print_colored_message(f'Total Guilds: {len(self.client.guilds)}', "green")
            ColorHelper.ColorHelper.print_colored_message(f'Total Users: {len(self.client.users)}', "blue")
            print("--------------")
            directory = "databases/words"
            filename = f"{directory}/{guild.id}.json"
            if os.path.exists(filename):
                os.remove(filename)
                ColorHelper.ColorHelper.print_colored_message(f"Deleted word database for guild {guild.name}", "red")
            else:
                ColorHelper.ColorHelper.print_colored_message(f"Word database for guild {guild.name} does not exist", "yellow")
            
            directory = "databases/settings"
            filename = f"{directory}/{guild.id}.json"
            if os.path.exists(filename):
                os.remove(filename)
                ColorHelper.ColorHelper.print_colored_message(f"Deleted settings database for guild {guild.name}", "red")
            else:
                ColorHelper.ColorHelper.print_colored_message(f"Settings database for guild {guild.name} does not exist", "yellow")
