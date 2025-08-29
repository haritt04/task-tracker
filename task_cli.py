#!/usr/bin/env python3

import json 
import os 
from datetime import datetime
import sys
    
JSON_FILE = 'tasks.json'

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

def main():
    args = sys.argv[1:]

    if not args:
        print ("Usage: task-cli <command> [<args>]")
        print ("Commands: add, list, complete, delete")
        return
    
    comand = args[0]

    if comand == "add":
        if len(args) < 2:
            print("Provide a task description.")
        else:
            description = " ".join(args[1:])
            add_task(description)

    # elif comand == "list":
    #     tasks = load_tasks()
    #     if not tasks:
    #         print("No tasks found.")
    #     else:
    #         for task in tasks:
    #             status = task['status']
    #             desc = task['description']
    #             tid = task['id']
    #             print(f"[{tid}] {desc} - {status}")
    else:
        print(f"Unknown command: {comand}")
    

        
if __name__ == "__main__":
    main()