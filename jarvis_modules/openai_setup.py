# jarvis_modules/openai_setup.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in environment variables or .env file.")

openai.api_key = api_key
client = openai
