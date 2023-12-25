import subprocess
import sys
import os
from pathlib import Path
import psycopg2

from cl_dir_defines import get_cl_origin

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="")


def process_arg(arg: str) -> str:
    if arg.startswith('"'):
        arg = arg[1:-1]
    if "\\" in arg:
        arg = arg.replace("\\", "/")
    return arg


class UnimplementedError(Exception):
    pass


def insert_db(file: str, directory: str, command: str):
    with connection.cursor() as cursor:
        res = cursor.execute("SELECT * FROM compile_commands WHERE file=%s", (file,))
        if res != 0:
            cursor.execute(
                "UPDATE compile_commands SET directory=%s, command=%s WHERE file=%s",
                (
                    directory,
                    command,
                    file,
                ),
            )
        else:
            cursor.execute(
                "INSERT INTO compile_commands(file, directory, command) "
                "values (%s, %s, %s)",
                (
                    file,
                    directory,
                    command,
                ),
            )
    connection.commit()


def write_compile_commands(args: list[str]):
    if args[0].startswith("@"):
        file = args[0][1:]
        content = Path(file).read_text(encoding="UTF-16")
        directory = str(Path(os.getcwd()).resolve()).replace("\\", "/")
        args = []
        files = []
        if "\n" in content:  # VS2008
            lines = content.split("\n")
            args = [process_arg(arg) for arg in lines[0].split(" ")]
            files = lines[1:]
        else:
            args_raw = [process_arg(arg) for arg in content.split(" ")]
            for arg in args_raw:
                if Path(arg).exists():
                    files.append(arg)
                else:
                    args.append(arg)

        files = list(filter(lambda x: x.strip() != "", files))
        files = list(
            map(
                lambda x: str(Path(directory).resolve().joinpath(x)).replace("\\", "/"),
                files,
            )
        )
        for file in files:
            command = f"C:/PROGRA~1/LLVM/bin/clang-cl.exe {' '.join(args)} {file}"
            insert_db(file, directory, command)
    else:
        raise UnimplementedError()


if __name__ == "__main__":
    vs_version = sys.argv[1]
    cl_origin = get_cl_origin(vs_version=vs_version)
    args_without_exe_path = sys.argv[2:]
    # print(sys.argv)
    write_compile_commands(args_without_exe_path)
    connection.close()
    subprocess.run(
        [
            cl_origin,
            *args_without_exe_path,
        ],
        check=True,
    )
