import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        command = ["python", target_file]
        if args:
            command.extend(args)
        result = subprocess.run(
            command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30
        )
        result_str = ""
        if result.returncode != 0:
            result_str += f"Process exited with code {result.returncode}\n"
        if not result.stdout and not result.stderr:
            result_str += "No output produced\n"
        else:
            if result.stdout:
                result_str += f"STDOUT: {result.stdout}\n"
            if result.stderr:
                result_str += f"STDERR: {result.stderr}\n"
        return result_str.strip()
    except Exception as e:
        return f"Error: executing Python file: {e}"
