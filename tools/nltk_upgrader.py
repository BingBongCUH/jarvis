
import subprocess
import sys

def run(user_input=None):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "nltk"])
        return "✅ Successfully upgraded nltk"
    except Exception as e:
        return f"❌ Error upgrading nltk: {e}"
