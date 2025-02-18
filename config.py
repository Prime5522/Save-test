# devgagan
# Note if you are trying to deploy on vps then directly fill values in ("")

from os import getenv

# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
# wtite up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = int(getenv("API_ID", "21257327"))
API_HASH = getenv("API_HASH", "1235c1fe45ebc4968d9e23bc93440549")
BOT_TOKEN = getenv("BOT_TOKEN", "7769318103:AAEoS83gl9cU5y7mSD4-ZtBkf5FUcy3EnKY")
OWNER_ID = list(map(int, getenv("OWNER_ID", "5192808332").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://mhsm:mhsm@cluster0.j9figvh.mongodb.net/?retryWrites=true&w=majority")
LOG_GROUP = getenv("LOG_GROUP", "-1002412068232")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002013750265"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "10"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "500"))
WEBSITE_URL = getenv("WEBSITE_URL", "")
AD_API = getenv("AD_API", "")
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", YTUB_COOKIES)
DEFAULT_SESSION = getenv("DEFAUL_SESSION", None)  # added old method of invite link joining
INSTA_COOKIES = getenv("INSTA_COOKIES", INST_COOKIES)
