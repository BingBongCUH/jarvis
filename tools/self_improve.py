import os
import json
import traceback
from datetime import datetime
from jarvis_modules import self_guidance, openai_setup
from tools import tool_generator


def generate_tool_filename(task_description):
    client = openai_setup.client
    prompt = f"""
You are a helpful assistant. Convert the task below into a clean Python filename.
Task: "{task_description}"
Rules:
- Only return the filename (no quotes, no .py)
- Use only lowercase and underscores
- Valid Python identifier
"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Filename generator"},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    filename = response.choices[0].message.content.strip().replace(".py", "")
    print(f"[DEBUG] Generated filename: {filename}")
    return "".join(c for c in filename if c.isalnum() or c == "_")


def run(user_input=None):
    print("[DEBUG] Starting self-improvement run")

    with open("core_vision.json", "r") as f:
        prime_directive = json.load(f)["prime_directive"]

    existing_tools = [
        f[:-3] for f in os.listdir("tools")
        if f.endswith(".py") and f != "self_improve.py"
    ]
    current_capabilities = [f"Tool: {t}" for t in existing_tools]
    print(f"[DEBUG] Current tools: {existing_tools}")

    suggestions = self_guidance.evaluate_progress(current_capabilities, prime_directive)
    print(f"[DEBUG] Suggestions: {suggestions}")

    if not suggestions:
        return "🟢 No upgrades needed."

    results = []
    for suggestion in suggestions:
        try:
            print(f"[🔧] Attempting: {suggestion}")
            result = tool_generator.run(suggestion)

            if not os.path.exists("tools/generated_tool.py"):
                print("[DEBUG] tools/generated_tool.py does NOT exist.")
                results.append(f"❌ No tool generated for '{suggestion}'")
                continue

            filename = generate_tool_filename(suggestion)
            filepath = f"tools/{filename}.py"

            if os.path.exists(filepath):
                print("[DEBUG] Tool already exists. Skipping.")
                os.remove("tools/generated_tool.py")
                results.append(f"⚠️ Tool already exists: {filepath}")
                continue

            os.rename("tools/generated_tool.py", filepath)
            print(f"[DEBUG] Tool moved to: {filepath}")

            # === Write to tool_manifest.json ===
            entry = {
                "tool_name": filename,
                "task": suggestion,
                "fulfills": suggestion.lower(),
                "path": filepath,
                "created_at": datetime.now().isoformat()
            }

            manifest_path = "tool_manifest.json"
            try:
                with open(manifest_path, "r") as mf:
                    manifest_data = json.load(mf)
            except Exception:
                manifest_data = []

            print(f"[DEBUG] Writing entry to manifest: {entry}")
            manifest_data.append(entry)
            with open(manifest_path, "w") as mf:
                json.dump(manifest_data, mf, indent=4)

            results.append(f"✅ Tool saved: {filepath}")

        except Exception as e:
            results.append(f"❌ Error for '{suggestion}': {e}\n{traceback.format_exc()}")

    return "\n".join(results)
