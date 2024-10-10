from colorama import Fore, Style, init # type: ignore

class ColorHelper:
    init(autoreset=True)

    @staticmethod
    def print_colored_message(message, color):
        """Create a colored message in the console.

        Args:
            message (str): The message to be printed.
            color (str): The color name for the message. Supported colors are: 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'. If an unsupported color is provided, the message will be printed in white.
        Returns:
            None
        """
        color_dict = {
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE
        }
        color_code = color_dict.get(color.lower(), Fore.WHITE)
        print(f"{color_code}{message}{Style.RESET_ALL}")
        return None