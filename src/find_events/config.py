# INFO: Loads environment variables and exposes them as module constants.
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SOURCE_BASE_URL")
USER_AGENT = os.getenv("USER_AGENT")
TIMEOUT = int(os.getenv("TIMEOUT", "15"))
CACHE_TTL_SECONDS = 60 * 60
TOP_CHART_URL = os.getenv("TOP_CHART_URL")
TOP_ARTISTS_LIMIT = 15
API_URL = os.getenv("API_URL")
API_KEY = os.getenv("API_KEY")

if not all([BASE_URL, USER_AGENT, TOP_CHART_URL, API_URL, API_KEY]):
    raise RuntimeError("Missing required environment variables. Check your .env file.")