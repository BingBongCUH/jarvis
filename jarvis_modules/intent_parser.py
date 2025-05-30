from jarvis_modules import openai_setup
import os

# Load tools dynamically
def get_tool_names():
    return [
        f[:-3] for f in os.listdir("tools")
        if f.endswith(".py") and not f.startswith("__") and f != "self_improve.py"
    ]

def interpret_user_input(user_input):
    tool_names = get_tool_names()
    tool_list_str = "\n".join(tool_names)

    prompt = f"""
You are an AI assistant. Based on the user's message, select the best matching tool from the list below.
Only return the tool name and the updated prompt for that tool.

Available tools:
{tool_list_str}

User said:
\"\"\"{user_input}\"\"\"

Respond in this format:
TOOL:<tool_name>
PROMPT:<rephrased prompt to send to that tool>
"""

    try:
        client = openai_setup.client
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful command router."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )

        content = response.choices[0].message.content.strip()

        tool_line = next(line for line in content.splitlines() if line.startswith("TOOL:"))
        prompt_line = next(line for line in content.splitlines() if line.startswith("PROMPT:"))

        tool = tool_line.split("TOOL:")[1].strip()
        new_prompt = prompt_line.split("PROMPT:")[1].strip()

        return tool, new_prompt

    except Exception as e:
        print(f"[Intent Parser Error] Failed to parse OpenAI response.\n{e}")
        return None, None
