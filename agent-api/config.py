from dotenv import load_dotenv
import os

load_dotenv()

BIL_API_KEY = os.getenv("BIL_API_KEY")
BASE_URL = os.getenv("BASE_URL")
