from pathlib import Path

CL_DIR = Path("C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/bin/").resolve()
CL_DIR_2019_64 = Path("C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/amd64").resolve()


CL_ORIGIN = CL_DIR.joinpath("cl2.exe")
CURRENT = Path(__file__).resolve().parent

DB = CURRENT.joinpath("db.sqlite3")

import sys

if getattr(sys, "frozen", False):
    CURRENT = Path(sys.executable).resolve().parent
    DB = CURRENT.parent.joinpath("db.sqlite3")
