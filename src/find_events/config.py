# INFO: Loads environment variables and exposes them as module constants.
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("SOURCE_BASE_URL")
USER_AGENT = os.getenv("USER_AGENT")
TIMEOUT = int(os.getenv("TIMEOUT", "15"))

if not BASE_URL or not USER_AGENT:
    raise RuntimeError("Missing required environment variables. Check your .env file.")