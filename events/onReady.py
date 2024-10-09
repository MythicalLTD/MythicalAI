import colorama  # type: ignore
import helpers.ColorHelper as ColorHelper

class onReady:
    def __init__(self, client):
        self.client = client
        ColorHelper.ColorHelper.print_colored_message("Registering onReady event...", "gray")
        try: 
            self.register_event()
            ColorHelper.ColorHelper.print_colored_message("onReady event registered", "green")
        except Exception as e:
            ColorHelper.ColorHelper.print_colored_message(f"Error registering onReady event: {e}", "red")
            exit()
    
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