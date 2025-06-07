
import os
import importlib
import traceback
from jarvis_modules import openai_setup

def run_tool_with_repair(tool_name, user_input=""):
    try:
        module = importlib.import_module(f"tools.{tool_name}")
        return module.run(user_input)
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"[Supervisor] ❌ Tool '{tool_name}' crashed. Attempting auto-repair...")
        return auto_fix_tool(tool_name, error_trace)

def auto_fix_tool(tool_name, error_trace):
    tool_path = f"tools/{tool_name}.py"
    try:
        with open(tool_path, "r") as f:
            broken_code = f.read()
    except Exception as e:
        return f"[Auto-Fix Error] Couldn't read {tool_path}: {e}"

    prompt = f"""
You are a Python expert. The following tool code crashed with this traceback:

Traceback:
{error_trace}

Code:
```python
{broken_code}
```

Please return the corrected full script. Do NOT add comments or explanations. Only return the corrected code inside one Python code block.
"""

    client = openai_setup.client
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful Python code fixer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )

    content = response.choices[0].message.content
    if "```python" in content:
        content = content.split("```python")[1].split("```")[0].strip()

    with open(tool_path, "w", encoding="utf-8") as f:
        f.write(content)

    return f"[✅ Auto-Fix] Tool '{tool_name}' has been repaired and saved."
