
import os
import subprocess
import sys

def upgrade_tool():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
    except Exception as e:
        print(f"Error occurred while upgrading pip: {e}")
        sys.exit(1)

def generate_self_upgrading_tool(tool_name):
    tool_code = f"""
import os
import subprocess
import sys

def upgrade_{tool_name}():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "{tool_name}"])
    except Exception as e:
        print(f"Error occurred while upgrading {tool_name}: {{e}}")
        sys.exit(1)

if __name__ == "__main__":
    upgrade_{tool_name}()
"""
    with open(f"{tool_name}_upgrader.py", "w") as f:
        f.write(tool_code)

if __name__ == "__main__":
    upgrade_tool()
    generate_self_upgrading_tool("your_tool_name")
