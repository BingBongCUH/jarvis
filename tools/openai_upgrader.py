
import subprocess
import sys

def run(user_input=None):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "openai"])
        return "✅ Successfully upgraded openai"
    except Exception as e:
        return f"❌ Error upgrading openai: {e}"
