# test_get_file_content.py

from config import MAX_CHARS
from functions.get_file_content import get_file_content

if __name__ == "__main__":
    # files = [(f"'{x}'", x) if x != "." else ("current", x) for x in [".", "pkg", "/bin", "../"]]
    files = [
        "lorem.txt",
        "main.py",
        "pkg/calculator.py",
        "/bin/cat",
        "pkg/does_not_exist.py",
    ]
    for file in files:
        result = get_file_content("calculator", file)
        res_len = len(result)
        if res_len < MAX_CHARS:
            print(result)
        print(f"{file} length: {res_len}")
        print(f"{file} truncated: {'truncated' in result}")
