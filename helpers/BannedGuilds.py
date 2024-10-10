import json
import os
class BannedGuilds:
    _file_path = "databases/bannedGuilds.json"

    @staticmethod
    def _load_banned_guilds():
        if os.path.exists(BannedGuilds._file_path):
            with open(BannedGuilds._file_path, "r") as f:
                return json.load(f)
        return {}

    @staticmethod
    def _save_banned_guilds(banned_guilds):
        with open(BannedGuilds._file_path, "w") as f:
            json.dump(banned_guilds, f, indent=4)

    @staticmethod
    def ban_guild(guild_id, reason="No reason provided"):
        banned_guilds = BannedGuilds._load_banned_guilds()
        banned_guilds[guild_id] = {"reason": reason}
        BannedGuilds._save_banned_guilds(banned_guilds)

    @staticmethod
    def unban_guild(guild_id):
        banned_guilds = BannedGuilds._load_banned_guilds()
        if str(guild_id) in banned_guilds:
            del banned_guilds[str(guild_id)]
            BannedGuilds._save_banned_guilds(banned_guilds)

    @staticmethod
    def is_banned(guild_id):
        banned_guilds = BannedGuilds._load_banned_guilds()
        is_banned = str(guild_id) in banned_guilds
        return is_banned
    
    @staticmethod
    def getBanReason(guild_id):
        if (BannedGuilds.is_banned(guild_id)):
            banned_guilds = BannedGuilds._load_banned_guilds()
            if str(guild_id) in banned_guilds:
                return banned_guilds[str(guild_id)]["reason"]
            return None
        else:
            return None

    @staticmethod
    def doSyntaxCheck():
        with open(BannedGuilds._file_path, "r") as f:
            json.load(f)
        return True