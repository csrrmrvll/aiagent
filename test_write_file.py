# test_write_file.py

from config import MAX_CHARS
from functions.write_file import write_file

if __name__ == "__main__":
    files_and_content = [
        ("lorem.txt", "wait, this isn't lorem ipsum"),
        ("pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
        ("/tmp/temp.txt", "this should not be allowed"),
    ]
    for file, content in files_and_content:
        result = write_file("calculator", file, content)
        print(result)
