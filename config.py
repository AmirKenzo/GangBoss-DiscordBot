import json
from decouple import config


TOKEN = config("TOKEN")
SERVER_GUILD_ID = config("SERVER_GUILD_ID", cast=int)
CHANNEL_XP_REPORT = config("CHANNEL_XP_REPORT", cast=int)
CHANNEL_ANNOUNCEMENT = config("CHANNEL_ANNOUNCEMENT", cast=int)
CHANNEL_STATUS_ROB = config("CHANNEL_STATUS_ROB", cast=int)
ACTIVITY_BOT = json.loads(config("ACTIVITY_BOT"))
BANNER_LINK = config("BANNER_LINK")
GANG_NAME = config("GANG_NAME")

ROLE_XP_MANAGER = config("ROLE_XP_MANAGER").split(",")
ROLE_FAMILY = config("ROLE_FAMILY").split(",")
