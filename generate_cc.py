import json
import os
import psycopg2
from pathlib import Path

connection = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="postgres",
    password="")


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
    
    ret = []
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT file, directory, command FROM compile_commands"
            " WHERE directory LIKE CONCAT(%s, '%%')",
            (context,),
        )
        all = cursor.fetchall()
        for i in all:
            d = i
            command = CompileCommand()
            command.file = d[0]
            if not Path(command.file).exists():
                continue
            command.directory = d[1]
            command.command = d[2]
            ret.append(command)
    return ret


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", "-P", type=str, default=os.getcwd())
    args = parser.parse_args()
    context = Path(args.path).resolve()
    commands = get_compile_commands(context)
    file = context.joinpath("compile_commands.json")
    generate(commands, file)
