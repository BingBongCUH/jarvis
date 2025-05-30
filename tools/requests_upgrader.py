
import subprocess
import sys

def run(user_input=None):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "requests"])
        return "✅ Successfully upgraded requests"
    except Exception as e:
        return f"❌ Error upgrading requests: {e}"
