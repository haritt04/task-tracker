# Task Tracker CLI

A simple command-line interface (CLI) application to manage and track your tasks efficiently.

---

## Project Overview

This project is designed to help you build a CLI tool for task management, focusing on essential operations like adding, updating, deleting, and listing tasks. Tasks are stored in a local `tasks.json` file, ensuring data persistence across sessions. This application is ideal for developers looking to practice file handling, user input processing, and building CLI applications.

Inspired by the [Task Tracker project on roadmap.sh](https://roadmap.sh/projects/task-tracker), this tool serves as a practical exercise in creating a functional and user-friendly command-line application.

---

## Features

* **Add a New Task**: Create tasks with descriptions.
* **Update Task Description**: Modify existing task descriptions.
* **Delete a Task**: Remove tasks from your list.
* **Mark Task Status**: Set tasks as `todo`, `in-progress`, or `done`.
* **List Tasks**: View all tasks or filter by status.

---

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/haritt04/task-tracker.git
   cd task-tracker
   ```



2. Ensure Python 3 is installed on your system.

---

## Usage

Run the script with the desired command:

```bash
python task_cli.py <command> [<args>]
```



### Commands:

* **add**: Add a new task.

```bash
  python task_cli.py add "Task description"
```



* **update**: Update an existing task's description.

```bash
  python task_cli.py update <task_id> "New description"
```



* **delete**: Delete a task by ID.

```bash
  python task_cli.py delete <task_id>
```



* **mark-in-progress**: Set a task's status to `in-progress`.

```bash
  python task_cli.py mark-in-progress <task_id>
```



* **mark-done**: Set a task's status to `done`.

```bash
  python task_cli.py mark-done <task_id>
```



* **list**: List all tasks or filter by status.

```bash
  python task_cli.py list
  python task_cli.py list todo
  python task_cli.py list in-progress
  python task_cli.py list done
```



---

## 🗂️ Data Storage

Tasks are stored in a JSON file named `tasks.json` located in the same directory as the script. If the file doesn't exist, it will be created automatically.

Each task is represented as an object with the following structure:

```json
{
  "id": 1,
  "description": "Task description",
  "status": "todo",
  "createdAt": "2025-09-01T13:00:00Z",
  "updatedAt": "2025-09-01T13:00:00Z"
}
```

## 📬 Contact

For any questions or feedback, please open an issue in this repository or contact the maintainer at [harrynyinyi183@gmail.com]
