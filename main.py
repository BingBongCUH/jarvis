import os
import importlib
import json
from jarvis_modules import self_guidance, intent_parser  # Intent parser added

# === Load the Prime Directive ===
def load_prime_directive():
    with open("core_vision.json", "r") as f:
        data = json.load(f)
    return data["prime_directive"]

prime_directive = load_prime_directive()
print(f"[Jarvis Vision] Prime Directive loaded:\n> {prime_directive}\n")

# === Define Current Capabilities ===
current_capabilities = [
    "Basic input/output",
    "Weather tool",
    "Crypto price checker",
    "Memory storage and recall",
    "Can load and execute tools"
]

# === Self-Guidance: Evaluate Progress ===
recommendations = self_guidance.evaluate_progress(current_capabilities, prime_directive)
print("[Jarvis Self-Guidance] Suggested next upgrades:")
for r in recommendations:
    print(" -", r)

# === Jarvis Tool Runner ===
TOOLS_FOLDER = "tools"

def list_tools():
    return [f[:-3] for f in os.listdir(TOOLS_FOLDER) if f.endswith(".py")]

def run_tool(tool_name, user_input):
    try:
        tool = importlib.import_module(f"{TOOLS_FOLDER}.{tool_name}")
        return tool.run(user_input)
    except Exception as e:
        return f"[Error running {tool_name}]: {e}"

# === Main Runtime Loop ===
def main():
    print("\n🤖 Jarvis MK6 online.")
    print("Type something, or type 'quit' to exit.")

    available_tools = list_tools()

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            print("🛑 Shutting down Jarvis.")
            break

        # 🧠 Use Intent Parser
        try:
            result = intent_parser.interpret_user_input(user_input)
            tool_name = result.get("tool")
            reason = result.get("reasoning", "")
            parsed_input = result.get("parsed_input", user_input)

            if reason:
                print(f"[Interpreter] 🤔 {reason}")
        except Exception as e:
            print(f"[Interpreter Error] {e}")
            tool_name = None
            parsed_input = user_input

        # 🛠 Run tool if found
        if tool_name in available_tools:
            response = run_tool(tool_name, parsed_input)
        else:
            response = "I don’t know how to do that yet."

        print(f"🤖 {response}")

if __name__ == "__main__":
    main()
