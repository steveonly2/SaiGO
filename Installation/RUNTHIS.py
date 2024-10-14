import importlib

modules = [
'customtkinter',
'os',
'keyboard',
'threading',
'pyautogui',
'sys'
]

def check_modules(modules):
    """Check if standard library modules are available."""
    for module in modules:
        try:
            importlib.import_module(module)
            print(f"'{module}' is available.")
        except ImportError:
            print(f"'{module}' is NOT available.")

if __name__ == "__main__":
    check_modules(modules)
