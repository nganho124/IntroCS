#!/usr/bin/env python3
"""
Task Tracker with Audit Trail
A command-line task management system that maintains complete audit logs.
"""

import sys
from datetime import datetime
import os


class TaskTracker:
    """Manages tasks with persistent storage and audit logging."""

    def __init__(self, tasks_file="tasks.txt", audit_file="audit.txt"):
        self.tasks_file = tasks_file
        self.audit_file = audit_file
        self.tasks = {}
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from tasks.txt file."""
        if not os.path.exists(self.tasks_file):
            return

        try:
            with open(self.tasks_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    parts = line.split('\t')
                    if len(parts) == 3:
                        task_id = int(parts[0])
                        finish_state = int(parts[1])
                        task_name = parts[2]
                        self.tasks[task_id] = {
                            'name': task_name,
                            'finished': finish_state == 1
                        }
        except Exception as e:
            # If file is corrupted, start fresh
            self.tasks = {}

    def save_tasks(self):
        """Save tasks to tasks.txt file."""
        with open(self.tasks_file, 'w') as f:
            for task_id in sorted(self.tasks.keys()):
                task = self.tasks[task_id]
                finish_state = 1 if task['finished'] else 0
                f.write(f"{task_id}\t{finish_state}\t{task['name']}\n")

    def log_audit(self, command, success):
        """Log command execution to audit.txt."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = "S" if success else "F"
        log_entry = f"{timestamp} | {command} | {status}\n"

        with open(self.audit_file, 'a') as f:
            f.write(log_entry)

    def get_next_id(self):
        """Generate next available task ID."""
        if not self.tasks:
            return 1
        return max(self.tasks.keys()) + 1

    def add_task(self, task_name):
        """Add a new task to the tracker."""
        task_id = self.get_next_id()
        self.tasks[task_id] = {
            'name': task_name,
            'finished': False
        }
        self.save_tasks()
        print(f"Task added with ID: {task_id}")
        return True

    def list_tasks(self):
        """List all tasks with their status."""
        if not self.tasks:
            print("No tasks found.")
            return True

        for task_id in sorted(self.tasks.keys()):
            task = self.tasks[task_id]
            status = "[X]" if task['finished'] else "[ ]"
            print(f"{task_id} {status} {task['name']}")
        return True

    def finish_task(self, task_id):
        """Mark a task as finished."""
        if task_id not in self.tasks:
            print(f"Error: Task with ID {task_id} does not exist.")
            return False

        if self.tasks[task_id]['finished']:
            print(f"Task {task_id} is already finished.")
            return True

        self.tasks[task_id]['finished'] = True
        self.save_tasks()
        print(f"Task {task_id} marked as finished.")
        return True

    def delete_task(self, task_id):
        """Delete a task from the tracker."""
        if task_id not in self.tasks:
            print(f"Error: Task with ID {task_id} does not exist.")
            return False

        del self.tasks[task_id]
        self.save_tasks()
        print(f"Task {task_id} deleted.")
        return True


def main():
    """Main entry point for the task tracker."""
    if len(sys.argv) < 2:
        print("Usage: python tracker.py <command> [arguments]")
        print("Commands:")
        print("  add \"<task_name>\"    - Add a new task")
        print("  list                  - List all tasks")
        print("  finish <task_id>      - Mark task as finished")
        print("  delete <task_id>      - Delete a task")
        sys.exit(1)

    command = sys.argv[1].lower()
    tracker = TaskTracker()

    # Reconstruct full command for audit log
    full_command = ' '.join(sys.argv[1:])
    success = False

    try:
        if command == "add":
            if len(sys.argv) < 3:
                print("Error: Task name is required.")
                print("Usage: python tracker.py add \"<task_name>\"")
            else:
                task_name = sys.argv[2]
                success = tracker.add_task(task_name)

        elif command == "list":
            success = tracker.list_tasks()

        elif command == "finish":
            if len(sys.argv) < 3:
                print("Error: Task ID is required.")
                print("Usage: python tracker.py finish <task_id>")
            else:
                try:
                    task_id = int(sys.argv[2])
                    success = tracker.finish_task(task_id)
                except ValueError:
                    print("Error: Task ID must be a number.")

        elif command == "delete":
            if len(sys.argv) < 3:
                print("Error: Task ID is required.")
                print("Usage: python tracker.py delete <task_id>")
            else:
                try:
                    task_id = int(sys.argv[2])
                    success = tracker.delete_task(task_id)
                except ValueError:
                    print("Error: Task ID must be a number.")

        else:
            print(f"Error: Unknown command '{command}'")
            print("Valid commands: add, list, finish, delete")

    except Exception as e:
        print(f"Error: {e}")
        success = False

    finally:
        # Always log to audit file
        tracker.log_audit(full_command, success)


if __name__ == "__main__":
    main()
