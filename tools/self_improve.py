from jarvis_modules import self_guidance, openai_setup
from tools import tool_generator
import os
import json
import traceback
import re
from datetime import datetime

# === Generate a clean tool name using GPT ===
def generate_tool_filename(task_description):
    prompt = f"""
You are a helpful assistant. Based on the following task, return a clean Python filename.

Task:
"{task_description}"

Rules:
- Only return the file name, lowercase
- Use underscores instead of spaces
- Do NOT include ".py"
- Must be a valid Python identifier (no punctuation, numbers allowed)
- Return ONLY the filename, nothing else
"""
    client = openai_setup.client
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You convert task descriptions into valid Python filenames."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    filename = response.choices[0].message.content.strip().lower()
    filename = filename.replace(".py", "")
    filename = "".join(c for c in filename if c.isalnum() or c == "_")
    return filename

# === Generate a test script for the tool ===
def generate_test_script(tool_name, task_description):
    prompt = f"""
You are a Python test writer.

Write a basic test script for the tool '{tool_name}', which was created to: {task_description}

Requirements:
- Assume the tool has a run(user_input) function
- Import the tool by name
- Call run() safely
- Print the result
- Include 1–2 basic checks if appropriate
- No need for unittest or pytest frameworks
- Return ONLY the code
"""
    client = openai_setup.client
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You write simple Python test scripts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )
    code = response.choices[0].message.content
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]
    return code.strip()

# === Main self-improvement runner ===
def run(user_input=None):
    with open("core_vision.json", "r") as f:
        prime_directive = json.load(f)["prime_directive"]

    tool_files = [f[:-3] for f in os.listdir("tools") if f.endswith(".py") and f != "self_improve.py"]
    current_capabilities = [f"Tool: {name.replace('_', ' ')}" for name in tool_files]

    suggestions = self_guidance.evaluate_progress(current_capabilities, prime_directive)
    if not suggestions:
        return "🟢 No upgrades needed. Jarvis is fully aligned."

    upgrade_results = []

    for task in suggestions:
        print(f"[Self-Improve] Generating upgrade for: {task}")
        try:
            result = tool_generator.run(task)
            base_name = generate_tool_filename(task)
            dest_path = f"tools/{base_name}.py"

            if os.path.exists("tools/generated_tool.py"):
                if os.path.exists(dest_path):
                    os.remove("tools/generated_tool.py")
                    upgrade_results.append(f"⚠️ Skipped: Tool already exists → {dest_path}")
                    continue
                else:
                    os.rename("tools/generated_tool.py", dest_path)

                    # === Validate syntax ===
                    with open(dest_path, "r") as f:
                        code = f.read()
                        compile(code, dest_path, 'exec')

                    # === Generate and run test ===
                    test_code = generate_test_script(base_name, task)
                    test_path = f"tests/test_{base_name}.py"
                    os.makedirs("tests", exist_ok=True)
                    with open(test_path, "w") as tf:
                        tf.write(test_code)

                    print(f"[Test] Running test for {base_name}...")
                    test_result = os.system(f"python {test_path}")
                    if test_result != 0:
                        os.remove(dest_path)
                        os.remove(test_path)
                        upgrade_results.append(f"❌ Test failed. Tool removed → {dest_path}")
                        continue

                    # === Log to changelog ===
                    log_entry = f"{task} => {dest_path}\n"
                    with open("upgrade_changelog.txt", "a") as log_file:
                        log_file.write(log_entry)

                    # === Add to manifest ===
                    manifest_entry = {
                        "tool_name": base_name,
                        "task": task,
                        "fulfills": task.strip().lower(),
                        "path": dest_path,
                        "created_at": datetime.now().isoformat()
                    }

                    manifest_path = "tool_manifest.json"
                    try:
                        with open(manifest_path, "r") as f:
                            existing = json.load(f)
                    except:
                        existing = []

                    existing.append(manifest_entry)
                    print("[Manifest] Writing tool to manifest:", manifest_entry)
                    with open(manifest_path, "w") as f:
                        json.dump(existing, f, indent=4)

                    upgrade_results.append(f"✅ {task} → {dest_path}")
            else:
                upgrade_results.append(f"❌ Failed: No tool generated for '{task}'")
        except Exception as e:
            upgrade_results.append(f"⚠️ Error during upgrade '{task}': {str(e)}\n{traceback.format_exc()}")

    return "\n".join(upgrade_results)
