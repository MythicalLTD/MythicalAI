import json
import os
import shutil 
import helpers.ColorHelper as ColorHelper

class SettingsHelper:
    @staticmethod
    def check_all():
        base_dir = './databases/settings'
        corrupted_dir = os.path.join(base_dir, 'corrupted_settings_db')
        os.makedirs(corrupted_dir, exist_ok=True)

        for root, dirs, files in os.walk(base_dir):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r') as f:
                            json.load(f)
                    except (json.JSONDecodeError, IOError):
                        corrupted_path = os.path.join(corrupted_dir, file)
                        shutil.copy(file_path, corrupted_path)
                        ColorHelper.print_colored_message(f"Corrupted file found and copied: {file_path}", "red")

    @staticmethod
    def _ensure_file_exists(file_path):
        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as file:
                json.dump({"bot_status": True}, file)

    @staticmethod
    def get_setting(server_id, key):
        file_path = f"./databases/settings/{server_id}.json"
        SettingsHelper._ensure_file_exists(file_path)
        with open(file_path, 'r') as file:
            settings = json.load(file)
        return settings.get(key)

    @staticmethod
    def set_setting(server_id, key, value):
        file_path = f"./databases/settings/{server_id}.json"
        SettingsHelper._ensure_file_exists(file_path)
        with open(file_path, 'r') as file:
            settings = json.load(file)
        settings[key] = value
        with open(file_path, 'w') as file:
            json.dump(settings, file, indent=4)

    @staticmethod
    def init_settings(server_id, initial_settings):
        file_path = f"./databases/settings/{server_id}.json"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump(initial_settings, file, indent=4)
