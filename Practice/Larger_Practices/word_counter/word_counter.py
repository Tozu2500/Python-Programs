from pathlib import Path

class WordCounter:
    # Handle word counting and character counting

    def __init__(self, text: str):
        self.text = text

    def count_words(self) -> int:
        return len(self.text.split())
    
    def char_count_with_spaces(self) -> int:
        return len(self.text)
    
    def char_count_without_spaces(self) -> int:
        return len(self.text.replace(" ", ""))
    
    def get_results(self) -> str:
        return (
            f"Word count: {self.count_words()}\n"
            f"Characters (with spaces): {self.char_count_with_spaces()}\n"
            f"Characters (without spaces): {self.char_count_without_spaces()}\n"
        )
    
class FileManager:
    # Handle file paths and input & output

    @staticmethod
    def resolve_path(user_input: str) -> Path:
        path = Path(user_input).expanduser()
        if not path.is_absolute():
            path = Path.cwd() / path
        return path.resolve()
    
    @staticmethod
    def read_file(path: Path) -> str | None:
        try:
            return path.read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Error: File not found {path}")
        except IsADirectoryError:
            print("Error: Path is a directory")
        except PermissionError:
            print("Error: Permission denied")
        return None

class WordCounterApp:
    # Main application
    
    def run(self):
        print("Word counter app")
        print("1. Enter text manually")
        print("2. Read text from a file")

        choice = input("Choose an option 1 or 2: ").strip()

        if choice == "1":
            text = input("\nEnter your sentence:\n")

        elif choice == "2":
            path_input = input("Enter file path, absolute or relative: ").strip()
            path = FileManager.resolve_path(path_input)
            text = FileManager.read_file(path)
            if text is None:
                return
        else:
            print("Invalid choice!")
            return
        
        counter = WordCounter(text)
        result = counter.get_results()

        print("\nResults\n")
        print(result)

if __name__ == "__main__":
    app = WordCounterApp()
    app.run()