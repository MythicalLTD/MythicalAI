import os
import json
import shutil
import helpers.ColorHelper as ColorHelper

class DatabaseChecker:
    @staticmethod
    def checkAll():
        base_dir = '/databases/words'
        corrupted_dir = os.path.join(base_dir, 'corrupted_words_db')
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
                        #print(f"Corrupted file found and copied: {file_path}")
                        ColorHelper.ColorHelper.print_colored_message(f"Corrupted file found and copied: {file_path}", "red")