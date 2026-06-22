# test_get_files_info.py

from functions.get_files_info import get_files_info

if __name__ == "__main__":
    dirs = [
        (f"'{x}'", x) if x != "." else ("current", x)
        for x in [".", "pkg", "/bin", "../"]
    ]
    for name, dir in dirs:
        print(f'Result for {name} directory:\n{get_files_info("calculator", dir)}')
