import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class Task:    
    def __init__(self, description: str, priority: str = "medium"):
        self.id = id(self)
        self.description = description
        self.priority = priority.lower()
        self.completed = False
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.completed_at = None
    
    def mark_complete(self):
        self.completed = True
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    def mark_incomplete(self):
        self.completed = False
        self.completed_at = None
    
    def to_dict(self) -> Dict:
        """Convert task to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'description': self.description,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at,
            'completed_at': self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict):
        task = cls(data['description'], data['priority'])
        task.id = data['id']
        task.completed = data['completed']
        task.created_at = data['created_at']
        task.completed_at = data['completed_at']
        return task
    
    def __str__(self):
        status = "✓" if self.completed else "○"
        priority_symbols = {"high": "!!!", "medium": "!!", "low": "!"}
        priority = priority_symbols.get(self.priority, "!!")
        return f"[{status}] {priority} {self.description}"


class TodoList:    
    def __init__(self, filename: str = "tasks.json"):
        self.filename = filename
        self.tasks: List[Task] = []
        self.load_tasks()
    
    def add_task(self, description: str, priority: str = "medium") -> Task:
        task = Task(description, priority)
        self.tasks.append(task)
        self.save_tasks()
        return task
    
    def remove_task(self, task_id: int) -> bool:
        for i, task in enumerate(self.tasks):
            if task.id == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False
    
    def complete_task(self, task_id: int) -> bool:
        task = self.find_task(task_id)
        if task:
            task.mark_complete()
            self.save_tasks()
            return True
        return False
    
    def uncomplete_task(self, task_id: int) -> bool:
        task = self.find_task(task_id)
        if task:
            task.mark_incomplete()
            self.save_tasks()
            return True
        return False
    
    def find_task(self, task_id: int) -> Optional[Task]:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_tasks(self, show_completed: bool = True) -> List[Task]:
        if show_completed:
            return self.tasks
        return [task for task in self.tasks if not task.completed]
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        return [task for task in self.tasks if task.priority == priority.lower()]
    
    def save_tasks(self):
        try:
            data = [task.to_dict() for task in self.tasks]
            with open(self.filename, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_tasks(self):
        if not os.path.exists(self.filename):
            return
        
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
        except Exception as e:
            print(f"Error loading tasks: {e}")
    
    def get_stats(self) -> Dict[str, int]:
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.completed])
        pending = total - completed
        
        priority_counts = {"high": 0, "medium": 0, "low": 0}
        for task in self.tasks:
            if not task.completed and task.priority in priority_counts:
                priority_counts[task.priority] += 1
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            **priority_counts
        }


class TodoInterface:    
    def __init__(self):
        self.todo_list = TodoList()
    
    def display_menu(self):
        print("\n" + "="*50)
        print("           TO-DO LIST MANAGER")
        print("="*50)
        print("1. View tasks")
        print("2. Add task")
        print("3. Complete task")
        print("4. Remove task")
        print("5. View statistics")
        print("6. Filter by priority")
        print("7. Toggle task completion")
        print("8. Exit")
        print("-"*50)
    
    def display_tasks(self, tasks: List[Task] = None, title: str = "ALL TASKS"):
        if tasks is None:
            tasks = self.todo_list.get_tasks()
        
        if not tasks:
            print(f"\n{title}: No tasks found!")
            return
        
        print(f"\n{title}:")
        print("-"*50)
        
        # Group by completion status
        pending = [t for t in tasks if not t.completed]
        completed = [t for t in tasks if t.completed]
        
        if pending:
            print("PENDING:")
            for task in sorted(pending, key=lambda x: x.priority):
                print(f"  ID: {task.id} | {task}")
        
        if completed:
            print("\nCOMPLETED:")
            for task in completed:
                print(f"  ID: {task.id} | {task} (Done: {task.completed_at})")
    
    def add_task_interactive(self):
        print("\nADD NEW TASK")
        print("-"*20)
        description = input("Task description: ").strip()
        
        if not description:
            print("Task description cannot be empty!")
            return
        
        print("Priority levels: high, medium, low")
        priority = input("Priority (default: medium): ").strip().lower()
        
        if priority not in ["high", "medium", "low"]:
            priority = "medium"
        
        task = self.todo_list.add_task(description, priority)
        print(f"✓ Task added successfully! ID: {task.id}")
    
    def complete_task_interactive(self):
        self.display_tasks(self.todo_list.get_tasks(show_completed=False), "PENDING TASKS")
        
        try:
            task_id = int(input("\nEnter task ID to complete: "))
            if self.todo_list.complete_task(task_id):
                print("✓ Task marked as complete!")
            else:
                print("✗ Task not found!")
        except ValueError:
            print("✗ Please enter a valid task ID!")
    
    def remove_task_interactive(self):
        self.display_tasks()
        
        try:
            task_id = int(input("\nEnter task ID to remove: "))
            if self.todo_list.remove_task(task_id):
                print("✓ Task removed successfully!")
            else:
                print("✗ Task not found!")
        except ValueError:
            print("✗ Please enter a valid task ID!")
    
    def toggle_task_interactive(self):
        self.display_tasks()
        
        try:
            task_id = int(input("\nEnter task ID to toggle completion: "))
            task = self.todo_list.find_task(task_id)
            
            if not task:
                print("✗ Task not found!")
                return
            
            if task.completed:
                self.todo_list.uncomplete_task(task_id)
                print("✓ Task marked as incomplete!")
            else:
                self.todo_list.complete_task(task_id)
                print("✓ Task marked as complete!")
        except ValueError:
            print("✗ Please enter a valid task ID!")
    
    def filter_by_priority(self):
        print("\nFILTER BY PRIORITY")
        print("-"*20)
        priority = input("Enter priority (high/medium/low): ").strip().lower()
        
        if priority not in ["high", "medium", "low"]:
            print("✗ Invalid priority level!")
            return
        
        tasks = self.todo_list.get_tasks_by_priority(priority)
        self.display_tasks(tasks, f"{priority.upper()} PRIORITY TASKS")
    
    def display_statistics(self):
        stats = self.todo_list.get_stats()
        
        print("\nTASK STATISTICS")
        print("="*30)
        print(f"Total tasks:      {stats['total']}")
        print(f"Completed tasks:  {stats['completed']}")
        print(f"Pending tasks:    {stats['pending']}")
        print("\nPending by priority:")
        print(f"  High:    {stats['high']}")
        print(f"  Medium:  {stats['medium']}")
        print(f"  Low:     {stats['low']}")
        
        if stats['total'] > 0:
            completion_rate = (stats['completed'] / stats['total']) * 100
            print(f"\nCompletion rate: {completion_rate:.1f}%")
    
    def run(self):
        print("Welcome to your To-Do List Manager!")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Select an option (1-8): ").strip()
                
                if choice == "1":
                    self.display_tasks()
                elif choice == "2":
                    self.add_task_interactive()
                elif choice == "3":
                    self.complete_task_interactive()
                elif choice == "4":
                    self.remove_task_interactive()
                elif choice == "5":
                    self.display_statistics()
                elif choice == "6":
                    self.filter_by_priority()
                elif choice == "7":
                    self.toggle_task_interactive()
                elif choice == "8":
                    print("\nThanks for using To-Do List Manager!")
                    break
                else:
                    print("✗ Invalid option! Please select 1-8.")
                
                input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break
            except Exception as e:
                print(f"✗ An error occurred: {e}")


def main():
    app = TodoInterface()
    app.run()


if __name__ == "__main__":
    main()