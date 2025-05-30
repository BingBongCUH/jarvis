import os
import subprocess
import sys
import io

# Make stdout UTF-8 safe for some terminals
try:
    sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
except Exception:
    pass  # Some environments don't support this

def upgrade_pip():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        return "[Success] pip upgraded successfully."
    except Exception as e:
        return f"[Error] Failed to upgrade pip: {e}"

def generate_self_upgrading_tool(tool_name):
    try:
        tool_code = f'''
import subprocess
import sys

def run(user_input=None):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "{tool_name}"])
        return "✅ Successfully upgraded {tool_name}"
    except Exception as e:
        return f"❌ Error upgrading {tool_name}: {{e}}"
'''
        os.makedirs("tools", exist_ok=True)
        filename = f"tools/{tool_name}_upgrader.py"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(tool_code)
        return f"🛠️ Generated upgrader script: {filename}"
    except Exception as e:
        return f"❌ Failed to generate upgrader for {tool_name}: {e}"


def run(user_input=None):
    output = []

    # Step 1: Upgrade pip
    output.append(upgrade_pip())

    # Step 2: Generate upgrade tools for these packages
    packages = ["requests", "openai", "nltk", "beautifulsoup4"]
    for pkg in packages:
        output.append(generate_self_upgrading_tool(pkg))

    return "\n".join(output)
