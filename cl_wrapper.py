import subprocess
import sqlite3
import sys

from tools import CL_ORIGIN, CURRENT

DB = CURRENT.joinpath("db.sqlite3")

con = sqlite3.connect(DB)
cur = con.cursor()


def write_compile_commands(args):
    print(args)


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
