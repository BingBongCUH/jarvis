from jarvis_modules import openai_setup
import os

def run(task_description):
    prompt = f"""
You are a Python expert AI developer.

Create a Python tool that fulfills the following task:
"{task_description}"

Requirements:
- Save as a single Python script
- Define a run(user_input) function
- Focus on fulfilling the task description
- Avoid unnecessary comments or print statements
- Return ONLY the code
"""

    client = openai_setup.client
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You generate Python tools with a run() function."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    code = response.choices[0].message.content.strip()
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0]

    os.makedirs("tools", exist_ok=True)
    output_path = "tools/generated_tool.py"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)

    return output_path
