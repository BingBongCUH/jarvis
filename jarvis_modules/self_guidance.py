import json
import os

def get_manifest_capabilities():
    try:
        with open("tool_manifest.json", "r") as f:
            manifest = json.load(f)
        return [entry["fulfills"].lower() for entry in manifest if "fulfills" in entry]
    except:
        return []

def evaluate_progress(current_capabilities, prime_directive):
    manifest_tasks = get_manifest_capabilities()

    # Combine tool names and manifest tasks
    current_tasks = set()
    for cap in current_capabilities:
        if cap.lower().startswith("tool: "):
            current_tasks.add(cap[6:].strip().lower())
    current_tasks.update(manifest_tasks)

    goal_map = [
        ("natural language interpreter", ["natural language", "input parsing"]),
        ("self-upgrading tool generator", ["generate new tools", "upgrade itself"]),
        ("spawn specialized clones", ["specialist agents", "delegation"]),
        ("tool validation + testing", ["test tools", "check correctness"]),
    ]

    suggestions = []
    for task, keywords in goal_map:
        if not any(k in t for k in keywords for t in current_tasks):
            suggestions.append(task.capitalize())

    return suggestions
