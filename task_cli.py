#!/usr/bin/env python3
import json
import os
import sys
import tempfile
from datetime import datetime, timezone

JSON_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")
STATUS = {'todo', 'in-progress', 'done'}

def current_utc():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')

def ensure_file_exists():
    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w") as f:
            json.dump([], f, indent=2)

def load_tasks():
    ensure_file_exists()
    try:
        with open(JSON_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list):
            backup_corrupt_file("not-a-list")
            return []
        return data
    except json.JSONDecodeError:
        backup_corrupt_file("json-decode-error")
        return []

def backup_corrupt_file(reason):
    ts = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    backup_name = f"{JSON_FILE}.bak.{ts}"
    try:
        os.rename(JSON_FILE, backup_name)
        print(f"Corrupt or invalid {JSON_FILE} backed up as {backup_name}. A new empty {JSON_FILE} was created.")
    except OSError:
        print(f"Failed to back up corrupted {JSON_FILE}. Overwriting with a new empty file.")
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f)

def save_tasks(tasks):
    tmp = f"{JSON_FILE}.tmp"
    with open(tmp, "w") as f:
        json.dump(tasks, f, indent=2)
    os.replace(tmp, JSON_FILE)

def get_new_id(tasks):
    if not tasks:
        return 1
    return max(task.get('id', 0) for task in tasks) + 1

def add_task(description):
    desc = description.strip()
    if not desc:
        print("Error: Task description cannot be empty.")
        sys.exit(1)
    tasks = load_tasks()
    new_id = get_new_id(tasks)
    now = current_utc()
    new_task = {
        "id": new_id,
        "description": desc,
        "status": "todo",
        "createdAt": now,
        "updatedAt": now
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {new_id})")

def find_task(tasks, task_id):
    for t in tasks:
        if t.get('id') == task_id:
            return t
    return None 

def update_task_description(task_id, new_description):
    desc = new_description.strip()
    if not desc:
        print("Error: Task description cannot be empty.")
        sys.exit(1)
    tasks = load_tasks()
    t = find_task(tasks, task_id)
    if not t:
        print(f"Task with ID {task_id} not found.")
        sys.exit(1)
    t['description'] = desc
    t['updatedAt'] = current_utc()
    save_tasks(tasks)
    print(f"Task {task_id} updated successfully.")

def update_task_status(task_id, new_status):
    status = new_status.strip()
    if status not in STATUS:
        print(f"Error: Invalid status '{status}'. Allowed: {', '.join(sorted(STATUS))}")
        sys.exit(1)
    tasks = load_tasks()
    t = find_task(tasks, task_id)
    if not t:
        print(f"Task with ID {task_id} not found.")
        sys.exit(1)
    t['status'] = status
    t['updatedAt'] = current_utc()
    save_tasks(tasks)
    print(f"Task {task_id} marked as {status}.")

def delete_task(task_id):
    tasks = load_tasks()
    for i, t in enumerate(tasks):
        if t.get('id') == task_id:
            del tasks[i]
            save_tasks(tasks)
            print(f"Task {task_id} deleted.")
            return
    print(f"Task with ID {task_id} not found.")
    sys.exit(1)

def list_tasks(filter_status=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    if filter_status:
        if filter_status not in STATUS:
            print(f"Error: Invalid filter '{filter_status}'. Allowed: {', '.join(sorted(STATUS))}")
            sys.exit(1)
        tasks = [t for t in tasks if t.get('status') == filter_status]
    if not tasks:
        if filter_status:
            print(f"No tasks with status '{filter_status}' found.")
        else:
            print("No tasks found.")
        return
    print("ID | Description | Status | createdAt | updatedAt")
    print("-" * 80)
    for t in tasks:
        tid = t.get('id')
        desc = t.get('description', '')
        status = t.get('status', '')
        created = t.get('createdAt', '')
        updated = t.get('updatedAt', '')
        print(f"{tid} | {desc} | {status} | {created} | {updated}")

def print_help():
    print("Usage: task-cli <command> [<args>]")
    print("Commands:")
    print("  add \"description\"             Add a new task (status defaults to 'todo')")
    print("  update <id> \"new description\"  Update task description")
    print("  delete <id>                    Delete a task")
    print("  mark-in-progress <id>          Mark a task as in-progress")
    print("  mark-done <id>                 Mark a task as done")
    print("  list [done|todo|in-progress]   List tasks (optionally filter by status)")

def main():
    args = sys.argv[1:]
    if not args:
        print_help()
        return

    cmd = args[0]

    try:
        if cmd == "add":
            if len(args) < 2:
                print("Provide a task description.")
                sys.exit(1)
            description = " ".join(args[1:])
            add_task(description)

        elif cmd == "update":
            if len(args) < 3:
                print("Usage: task-cli update <task_id> \"new description\"")
                sys.exit(1)
            try:
                task_id = int(args[1])
            except ValueError:
                print("Task ID must be an integer.")
                sys.exit(1)
            description = " ".join(args[2:])
            update_task_description(task_id, description)

        elif cmd == "delete":
            if len(args) < 2:
                print("Usage: task-cli delete <task_id>")
                sys.exit(1)
            try:
                task_id = int(args[1])
            except ValueError:
                print("Task ID must be an integer.")
                sys.exit(1)
            delete_task(task_id)

        elif cmd == "mark-in-progress":
            if len(args) < 2:
                print("Usage: task-cli mark-in-progress <task_id>")
                sys.exit(1)
            try:
                task_id = int(args[1])
            except ValueError:
                print("Task ID must be an integer.")
                sys.exit(1)
            update_task_status(task_id, "in-progress")

        elif cmd == "mark-done":
            if len(args) < 2:
                print("Usage: task-cli mark-done <task_id>")
                sys.exit(1)
            try:
                task_id = int(args[1])
            except ValueError:
                print("Task ID must be an integer.")
                sys.exit(1)
            update_task_status(task_id, "done")

        elif cmd == "list":
            if len(args) == 1:
                list_tasks()
            else:
                filter_status = args[1]
                list_tasks(filter_status)

        elif cmd in ("-h", "--help", "help"):
            print_help()

        else:
            print(f"Unknown command: {cmd}")
            print_help()
            sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)

if __name__ == "__main__":
    main()