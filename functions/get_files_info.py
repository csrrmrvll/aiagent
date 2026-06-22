import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        if os.path.isdir(target_dir) == False:
            return f'Error: "{target_dir}" is not a directory'
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        dir_content = os.listdir(target_dir)
        return "\n".join(
            map(
                lambda entry: f"- {entry}: file_size={os.path.getsize(os.path.join(target_dir, entry))}, is_dir={os.path.isdir(os.path.join(target_dir, entry))}",
                dir_content,
            )
        )
    except Exception as e:
        return f'Error: {e}'
