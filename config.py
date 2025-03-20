
import re
from os import getenv, environ

id_pattern = re.compile(r'^.\d+$')

AUTH_CHANNEL = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('AUTH_CHANNEL', '-1002245813234 -1002043502363').split()] 
# give channel id with separate space. Ex: ('-10073828 -102782829 -1007282828')


# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
# wtite up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = int(getenv("API_ID", "21257327"))
API_HASH = getenv("API_HASH", "1235c1fe45ebc4968d9e23bc93440549")
BOT_TOKEN = getenv("BOT_TOKEN", "8155332374:AAEffXJw_XUWCxrgDeFA12QV1fFwB5e0I4c")
OWNER_ID = list(map(int, getenv("OWNER_ID", "5192808332 7059303929").split()))
MONGO_DB = getenv("MONGO_DB", "mongodb+srv://susantamusic:susantabhan@cluster0.5pwi1py.mongodb.net/?retryWrites=true&w=majority")
LOG_GROUP = getenv("LOG_GROUP", "-1002219917861")
CHANNEL_ID = int(getenv("CHANNEL_ID", "-1002013750265"))
FREEMIUM_LIMIT = int(getenv("FREEMIUM_LIMIT", "10"))
PREMIUM_LIMIT = int(getenv("PREMIUM_LIMIT", "50000"))
WEBSITE_URL = getenv("WEBSITE_URL", "")
AD_API = getenv("AD_API", "")
STRING = getenv("STRING", None)
YT_COOKIES = getenv("YT_COOKIES", YTUB_COOKIES)
DEFAULT_SESSION = getenv("DEFAUL_SESSION", None)  # added old method of invite link joining
INSTA_COOKIES = getenv("INSTA_COOKIES", INST_COOKIES)
