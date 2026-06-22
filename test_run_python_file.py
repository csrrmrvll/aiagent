# test_run_python_file.py

from functions.run_python_file import run_python_file

if __name__ == "__main__":
    files_and_args = [
        ("main.py", []),
        ("main.py", ["3 + 5"]),
        ("tests.py", []),
        ("../main.py", []),
        ("nonexistent.py", []),
        ("lorem.txt", []),
    ]
    for file, args in files_and_args:
        result = run_python_file("calculator", file, args)
        print(result)
