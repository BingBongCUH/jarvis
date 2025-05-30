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
    tool_code = f"""
import subprocess
import sys

def upgrade_{tool_name}():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "{tool_name}"])
        print("[Success] {tool_name} upgraded successfully.")
    except Exception as e:
        print(f"[Error] Failed to upgrade {tool_name}: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    upgrade_{tool_name}()
"""

    filename = f"{tool_name}_upgrader.py"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(tool_code)
    return f"[Generated] {filename}"

def run(user_input=None):
    output = []

    # Step 1: Upgrade pip
    output.append(upgrade_pip())

    # Step 2: Generate upgrade tools for these packages
    packages = ["requests", "openai", "nltk", "beautifulsoup4"]
    for pkg in packages:
        output.append(generate_self_upgrading_tool(pkg))

    return "\n".join(output)
