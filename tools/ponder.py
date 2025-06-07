import json
import os
import random
import threading
import time
from datetime import datetime
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
client = OpenAI()

# File paths
THOUGHT_LOG_PATH = "data/thought_log.json"
TOOL_MANIFEST_PATH = "tool_manifest.json"
TASK_QUEUE_PATH = "data/task_queue.json"

# Basic prompt starter ideas
THOUGHT_SEEDS = [
    "How can I improve myself today?",
    "Which tool haven’t I used in a while, and why?",
    "Is there any feature Alexander might want soon?",
    "Do I remember anything that could be automated better?",
    "Am I missing any important skills?"
]

def ponder():
    thought = {
        'timestamp': datetime.now().isoformat(),
        'seed': random.choice(THOUGHT_SEEDS)
    }

    # Pull current tools from manifest
    tool_names = []
    if os.path.exists(TOOL_MANIFEST_PATH):
        try:
            with open(TOOL_MANIFEST_PATH, 'r') as f:
                tools = json.load(f)
            tool_names = [tool['name'] for tool in tools.get('tools', [])]
            thought['tool_count'] = len(tool_names)
            thought['tools_sampled'] = random.sample(tool_names, min(3, len(tool_names)))
        except Exception as e:
            thought['tools_error'] = str(e)
    else:
        thought['tools_error'] = "No tool manifest found."

    # Use GPT to generate a real conclusion
    try:
        tool_summary = ", ".join(thought.get('tools_sampled', []))
        gpt_prompt = (
            f"You are Jarvis, an autonomous AI assistant reflecting on your current state. "
            f"Your current seed thought is: '{thought['seed']}'. "
            f"Here are a few tools you currently have: {tool_summary}. "
            f"Write a self-reflective internal thought about how you might improve or what you could build."
        )
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a thoughtful, autonomous AI reflecting on how to evolve."},
                {"role": "user", "content": gpt_prompt}
            ],
            temperature=0.7
        )
        conclusion = response.choices[0].message.content.strip()
        thought['conclusion'] = conclusion
    except Exception as e:
        thought['conclusion'] = f"(Failed to generate GPT thought: {e})"

    # Append to thought log
    os.makedirs(os.path.dirname(THOUGHT_LOG_PATH), exist_ok=True)
    log = []
    if os.path.exists(THOUGHT_LOG_PATH) and os.path.getsize(THOUGHT_LOG_PATH) > 0:
        with open(THOUGHT_LOG_PATH, 'r') as f:
            try:
                log = json.load(f)
            except json.JSONDecodeError:
                log = []
    log.append(thought)
    with open(THOUGHT_LOG_PATH, 'w') as f:
        json.dump(log, f, indent=2)

    # Determine if this thought should be added to the task queue
    keywords = ["improve", "develop", "build", "create", "suggest", "expand"]
    if any(k in thought['conclusion'].lower() for k in keywords):
        task_prompt = {
            "timestamp": thought['timestamp'],
            "idea": thought['conclusion'],
            "action_requested": True,
            "status": "pending"
        }
        os.makedirs(os.path.dirname(TASK_QUEUE_PATH), exist_ok=True)
        task_queue = []
        if os.path.exists(TASK_QUEUE_PATH) and os.path.getsize(TASK_QUEUE_PATH) > 0:
            with open(TASK_QUEUE_PATH, 'r') as f:
                try:
                    task_queue = json.load(f)
                except json.JSONDecodeError:
                    task_queue = []
        task_queue.append(task_prompt)
        with open(TASK_QUEUE_PATH, 'w') as f:
            json.dump(task_queue, f, indent=2)

        # Prompt the user immediately
        print("\n🔧 [Jarvis Suggestion] I had an idea:")
        print(f"🧠 {task_prompt['idea']}")
        print("💡 Should I explore this further, add it to your roadmap, or build something new from it?\n")

    return thought

def handle_user_response(response: str):
    if not os.path.exists(TASK_QUEUE_PATH):
        print("No task queue found.")
        return

    with open(TASK_QUEUE_PATH, 'r') as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            print("Task queue is corrupted.")
            return

    if not tasks:
        print("No tasks to update.")
        return

    last_task = next((task for task in reversed(tasks) if task.get("status") == "pending"), None)
    if not last_task:
        print("No pending tasks found.")
        return

    response = response.lower()
    if "explore" in response:
        last_task["status"] = "approved: explore"
    elif "build" in response:
        last_task["status"] = "approved: build"
    elif "roadmap" in response:
        last_task["status"] = "approved: roadmap"
    elif "ignore" in response:
        last_task["status"] = "ignored"
    else:
        print("Unrecognized response. Please use: explore, build, roadmap, or ignore.")
        return

    with open(TASK_QUEUE_PATH, 'w') as f:
        json.dump(tasks, f, indent=2)
    print(f"✅ Task updated to '{last_task['status']}'")

def start_ponder_loop(interval_seconds=60):
    def loop():
        while True:
            thought = ponder()
            print(f"[Jarvis Thought] {thought['timestamp']}: {thought['conclusion']}")
            time.sleep(interval_seconds)

    thread = threading.Thread(target=loop, daemon=True)
    thread.start()
