import subprocess
import sqlite3
import sys
import os
from pathlib import Path

from defines import CL_ORIGIN, CURRENT, DB

con = sqlite3.connect(DB)
with con:
    con.execute("CREATE TABLE IF NOT EXISTS compile_commands(file, directory, command)")


def process_arg(arg: str) -> str:
    if arg.startswith('"'):
        arg = arg[1:-1]
    if "\\" in arg:
        arg = arg.replace("\\", "/")
    return arg


class UnimplementedError(Exception):
    pass


def insert_db(file: str, directory: str, command: str):
    with con:
        res = con.execute("SELECT * FROM compile_commands WHERE file=?", (file,))
        if res.fetchone():
            con.execute(
                "UPDATE compile_commands SET directory=?, command=? WHERE file=?",
                (
                    directory,
                    command,
                    file,
                ),
            )
        else:
            con.execute(
                "INSERT INTO compile_commands(file, directory, command) "
                "values (?, ?, ?)",
                (
                    file,
                    directory,
                    command,
                ),
            )


def write_compile_commands(args: list[str]):
    if args[0].startswith("@"):
        file = args[0][1:]
        content = Path(file).read_text(encoding="UTF-16")
        directory = str(Path(os.getcwd()).resolve())
        lines = content.split("\n")
        args = [process_arg(arg) for arg in lines[0].split(" ")]
        files = lines[1:]
        files = list(map(lambda x: str(Path(directory).resolve().joinpath(x)), files))
        for file in files:
            command = f"C:/PROGRA~1/LLVM/bin/clang-cl.exe {' '.join(args)}"
            insert_db(file, directory, command)
    else:
        raise UnimplementedError()


if __name__ == "__main__":
    args_without_exe_path = sys.argv[1:]
    write_compile_commands(args_without_exe_path)
    subprocess.run(
        [
            CL_ORIGIN,
            *args_without_exe_path,
        ],
        check=True,
    )
