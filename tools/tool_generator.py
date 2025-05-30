from jarvis_modules import openai_setup

def run(task_description):
    prompt = f"""
You are a professional Python systems developer.

Write a single Python tool script that fulfills this task:
"{task_description}"

Requirements:
- The script must have a top-level function called `run(user_input)`
- It should perform the task described
- Use clear logic and be modular
- Only import packages if necessary
- Do not include explanations or comments
- Output ONLY valid Python code

Your script:
"""

    client = openai_setup.client
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a senior Python developer."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
    )

    code = response.choices[0].message.content

    # Extract code block if present
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].strip()

    # Save to a temp file
    with open("tools/generated_tool.py", "w", encoding="utf-8") as f:
        f.write(code)

    return code
