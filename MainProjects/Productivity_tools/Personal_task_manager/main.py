import sys
import argparse
from database.db_manager import DatabaseManager
from cli.cli_interface import CLIInterface
from gui.main_window import MainWindow
from PyQt5.QtWidgets import QApplication

def main():
    parser = argparse.ArgumentParser(description='Personal Task Manager')
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode')
    parser.add_argument('--add', type=str, help='Add a new task')
    parser.add_argument('--list', action='store_true', help='List all tasks')
    parser.add_argument('--status', type=str, help='Filter by status')
    parser.add_argument('--delete', type=int, help='Delete task by ID')
    parser.add_argument('--update', type=int, help='Update task by ID')
    parser.add_argument('--export', type=str, help='Export tasks to file')
    parser.add_argument('--import-file', type=str, help='Import tasks from file')
    parser.add_argument('--complete', type=int, help='Mark task as complete')
    parser.add_argument('--priority', type=str, help='Set priority (low/medium/high)')
    parser.add_argument('--recurring', action='store_true', help='Make task recurring')
    parser.add_argument('--frequency', type=str, help='Recurrence frequency')
    parser.add_argument('--due-date', type=str, help='Set due date (YYYY-MM-DD)')
    parser.add_argument('--title', type=str, help='Task title')
    parser.add_argument('--description', type=str, help='Task description')
    parser.add_argument('--category', type=str, help='Task category')
    
    args = parser.parse_args()
    
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    if args.cli or any([args.add, args.list, args.delete, args.update, args.export, args.import_file, args.complete]):
        cli = CLIInterface(db_manager)
        
        if args.add:
            cli.add_task_quick(args.add, args.priority, args.due_date, args.category, args.recurring, args.frequency)
        elif args.list:
            cli.list_tasks(args.status)
        elif args.delete:
            cli.delete_task(args.delete)
        elif args.complete:
            cli.complete_task(args.complete)
        elif args.update:
            cli.update_task_interactive(args.update)
        elif args.export:
            cli.export_tasks(args.export)
        elif args.import_file:
            cli.import_tasks(args.import_file)
        else:
            cli.run()
    else:
        app = QApplication(sys.argv)
        window = MainWindow(db_manager)
        window.show()
        sys.exit(app.exec_())

if __name__ == '__main__':
    main()