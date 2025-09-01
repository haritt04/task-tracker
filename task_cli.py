#!/usr/bin/env python3

import json 
import os 
from datetime import datetime
import sys
    
JSON_FILE = 'tasks.json'
Status = {'todo', 'in-progress', 'done'}

#current timestamp in iso format
def now_iso_utc():
    return datetime.utcnow().replace(microsecond=0).isoformat() + 'Z'

#load and create json file if does not exist
if not os.path.exists(JSON_FILE):
    with open(JSON_FILE, 'w') as f:
        json.dump([], f)

#load tasks from json file
def load_tasks():
    with open(JSON_FILE, 'r') as f:
        return json.load(f)
    
#save tasks to json file
def save_tasks(tasks):
    with open(JSON_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

#generate a new id for a task
def get_new_id(tasks):
    if not tasks:
        return 1
    return max(task['id'] for task in tasks) + 1

#add a new task
def add_task(description):
    tasks = load_tasks()
    new_id = get_new_id(tasks)
    now = datetime.now().isoformat()
    
    new_task = {
        'id': new_id,
        'description': description,
        'status': 'todo',
        'created_at': now,
        'completed_at': None
    }

    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task added with ID: {new_id}")

#update task status
def update_task(task_id, new_status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = new_status
            if new_status == 'completed':
                task['completed_at'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f"Task {task_id} marked as {new_status}.")
            return
    print(f"Task with ID {task_id} not found.")

#delete a task
def delete_task(task_id):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task['id'] == task_id:
            del tasks[i]
            save_tasks(tasks)
            print(f"Task {task_id} deleted.")
            return
    print(f"Task with ID {task_id} not found.")
    
#list all tasks 
def list_tasks(filter_status=None):
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
        return
    if filter_status:
        tasks = [t for t in tasks if t['status'] == filter_status]
    if not tasks:
        print(f"No tasks with status '{filter_status}' found.")
        return
    
    print("Tasks:")
    print("ID | Description | Status | Created At | Completed At")
    print("-" * 60)
    for task in tasks:
        tid = task['id']
        desc = task['description']
        status = task['status']
        created_at = task['created_at']
        completed_at = task['completed_at'] if task['completed_at'] else "N/A"
        print(f"{tid} | {desc} | {status} | {created_at} | {completed_at}")

def main():
    args = sys.argv[1:]

    if not args:
        print ("Usage: task-cli <command> [<args>]")
        print ("Commands: add, list, complete, delete")
        return
    
    cmd = args[0]

    if cmd == "add":
        if len(args) < 2:
            print("Provide a task description.")
        else:
            description = " ".join(args[1:])
            add_task(description)

    elif cmd == "update":
        if len(args) < 3:
            print("Usage: task-cli update <task_id> <status>")
        else:
            try:
                task_id = int(args[1])
                new_status = args[2]
                update_task(task_id, new_status)
            except ValueError:
                print("Task ID must be an integer.")

    elif cmd == "delete":
        if len(args) < 2:
            print("Usage: task-cli delete <task_id>")
        else:
            try:
                task_id = int(args[1])
                delete_task(task_id)
            except ValueError:
                print("Task ID must be an integer.")
    
    elif cmd == "list":
        if len(args) == 1:
            list_tasks()
        else:
            filter_status = args[1]
            list_tasks(filter_status)
        
if __name__ == "__main__":
    main()