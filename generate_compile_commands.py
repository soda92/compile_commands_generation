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
    file.write_text(json.dumps(commands, default=CompileCommand.__json__, indent=4))


def get_compile_commands(context: Path):
    context: str = str(context).replace("\\", "/")
    if context.endswith("/"):
        context = context[:-1]
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    ret = []
    with con:
        res = con.execute(
            "SELECT file, directory, command FROM compile_commands"
            " WHERE directory LIKE ? || '%'",
            (context,),
        )
        all = res.fetchall()
        for i in all:
            d = dict(i)
            command = CompileCommand()
            command.file = d["file"]
            command.directory = d["directory"]
            command.command = d["command"]
            ret.append(command)
    return ret


if __name__ == "__main__":
    context = os.getcwd()
    context = Path(context).resolve()
    commands = get_compile_commands(context)
    file = context.joinpath("compile_commands.json")
    generate(commands, file)
