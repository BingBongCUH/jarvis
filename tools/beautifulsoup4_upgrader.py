
import subprocess
import sys

def run(user_input=None):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "beautifulsoup4"])
        return "✅ Successfully upgraded beautifulsoup4"
    except Exception as e:
        return f"❌ Error upgrading beautifulsoup4: {e}"
