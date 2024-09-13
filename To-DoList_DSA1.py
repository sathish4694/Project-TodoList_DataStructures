import json
import os

# Defining the Task class
class Task:
    def __init__(self, task_name, category_name, priority, duedate, status, tags=None):
        self.task_name = task_name
        self.category_name = category_name
        self.priority = priority
        self.duedate = duedate
        self.status = status
        self.tags = tags if tags else []

    def to_dict(self):
        return {
            "task_name": self.task_name,
            "category_name": self.category_name,
            "priority": self.priority,
            "duedate": self.duedate,
            "status": self.status,
            "tags": self.tags
        }

# TaskNode for LinkedList
class TaskNode:
    def __init__(self, task):
        self.task = task
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_task(self, task):
        new_node = TaskNode(task)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete_task_by_name(self, task_name):
        current = self.head
        prev = None
        while current:
            if current.task.task_name == task_name:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return current.task
            prev = current
            current = current.next
        return None

    def view_tasks(self):
        current = self.head
        while current:
            print(f"{current.task.task_name}: {current.task.category_name} - Priority: {current.task.priority} - Due_Date: {current.task.duedate} - Status: {current.task.status}")
            current = current.next

    def find_task(self, task_name):
        current = self.head
        while current:
            if current.task.task_name == task_name:
                return current
            current = current.next
        return None

    def to_list(self):
        tasks = []
        current = self.head
        while current:
            tasks.append(current.task.to_dict())
            current = current.next
        return tasks

# Implementing Stack for undo feature
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, action):
        self.stack.append(action)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

# Hash Table for efficient search
class HashTable:
    def __init__(self):
        self.table = {}

    def add_task(self, task):
        for tag in task.tags:
            if tag not in self.table:
                self.table[tag] = []
            self.table[tag].append(task)

    def remove_task(self, task):
        for tag in task.tags:
            if tag in self.table:
                self.table[tag] = [t for t in self.table[tag] if t.task_name != task.task_name]

    def search_tasks(self, keyword):
        return self.table.get(keyword, [])

# JSON file operations
json_file_path = r'D:\Miraclesoft\To-DoListApplication_DataStructures\tasks.json'

def save_to_json():
    tasks = task_list.to_list()
    os.makedirs(os.path.dirname(json_file_path), exist_ok=True)  # Create directory if it doesn't exist
    with open(json_file_path, 'w') as file:
        json.dump(tasks, file, indent=4)

def load_from_json():
    if os.path.exists(json_file_path):
        try:
            with open(json_file_path, 'r') as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    task = Task(
                        task_data['task_name'],
                        task_data['category_name'],
                        task_data['priority'],
                        task_data['duedate'],
                        task_data['status'],
                        task_data['tags']
                    )
                    task_list.add_task(task)
                    search_table.add_task(task)
        except FileNotFoundError:
            print("No existing task file found. Starting fresh.")
    else:
        print(f"No file found at {json_file_path}. Starting fresh.")

# Task List, Undo Stack, and Search Table
task_list = LinkedList()
undo_stack = Stack()
search_table = HashTable()

# Adding a task
def add_task():
    task_name = input("Enter Task Name: ")
    category_name = input("Enter Category Name: ")
    priority = input("Enter Priority (High, Medium, Low): ")
    duedate = input("Enter Due Date (YYYY-MM-DD): ")
    status = input("Enter Status: ")
    tags = input("Enter Tags: ").split(',')

    task = Task(task_name, category_name, priority, duedate, status, tags)
    task_list.add_task(task)
    search_table.add_task(task)

    # Save the action in the undo stack
    undo_stack.push(('add', task_name))
    save_to_json()
    print("Task added successfully.")

# Viewing tasks
def view_tasks():
    task_list.view_tasks()

# Editing a task
def edit_task():
    task_name = input("Enter Task Name to edit: ")
    node = task_list.find_task(task_name)
    if node:
        node.task.task_name = input("Enter new Task Name: ")
        node.task.category_name = input("Enter new Category Name: ")
        node.task.priority = input("Enter new Priority (High, Medium, Low): ")
        node.task.duedate = input("Enter new Due Date (YYYY-MM-DD): ")
        node.task.status = input("Enter new Status: ")
        tags = input("Enter new Tags: ").split(',')
        node.task.tags = tags

        search_table.remove_task(node.task)
        search_table.add_task(node.task)
        save_to_json()
        print("Task updated successfully.")
    else:
        print("Task not found.")

# Deleting a task
def delete_task():
    task_name = input("Enter Task Name to delete: ")
    deleted_task = task_list.delete_task_by_name(task_name)
    if deleted_task:
        search_table.remove_task(deleted_task)
        undo_stack.push(('delete', deleted_task))
        save_to_json()
        print("Task deleted successfully.")
    else:
        print("Task not found.")

# Undo last action
def undo():
    undo_task = undo_stack.pop()
    if undo_task:
        action, task_info = undo_task
        if action == 'add':
            deleted_task = task_list.delete_task_by_name(task_info)
            search_table.remove_task(deleted_task)
        elif action == 'delete':
            task_list.add_task(task_info)
            search_table.add_task(task_info)
        save_to_json()
        print("Undo successful.")
    else:
        print("No actions to undo.")

# Searching tasks by keyword
def search_task():
    keyword = input("Enter tag/keyword to search: ")
    tasks = search_table.search_tasks(keyword)
    if tasks:
        for task in tasks:
            print(f"{task.task_name}: {task.category_name} - Priority: {task.priority} - Due: {task.duedate} - Status: {task.status}")
    else:
        print("No tasks found with that keyword.")

# Main function for testing 
def main():
    load_from_json()  # Load tasks from JSON file at startup

    while True:
        print("\nMain Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Edit Task")
        print("4. Delete Task")
        print("5. Undo Task")
        print("6. Search Task")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_task()
        elif choice == '2':
            view_tasks()
        elif choice == '3':
            edit_task()
        elif choice == '4':
            delete_task()
        elif choice == '5':
            undo()
        elif choice == '6':
            search_task()
        elif choice == '7':
            save_to_json()  # Save tasks before exiting
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
