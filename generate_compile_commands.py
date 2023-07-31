import json
import os
import sqlite3
from pathlib import Path

from defines import DB


class CompileCommand:
    file: str = ""
    directory: str = ""
    command: str = ""

    def __json__(self) -> dict:
        return {
            "file": self.file,
            "directory": self.directory,
            "command": self.command,
        }


def generate(commands: list[CompileCommand], file: Path):
    file.write_text(json.dumps(commands, default=CompileCommand.__json__))


def get_compile_commands():
    con = sqlite3.connect(DB)
    ret = []
    with con:
        res = con.execute("SELECT(file, directory, command) FROm compile_commands")
        all = res.fetchall()
        for i in all:
            ret.append(i["file"], i["directory"], i["command"])
    return ret


if __name__ == "__main__":
    commands = get_compile_commands()
    context = os.getcwd()
    file = Path(context).resolve().joinpath("compile_commands.json")
    generate(commands, file)
