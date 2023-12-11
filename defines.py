from pathlib import Path

CL_DIR = "C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/bin/"
CL_DIR = Path(CL_DIR).resolve()

CL_DIR_2019_64 = "C:/Program Files (x86)/Microsoft Visual Studio 14.0/VC/bin/amd64"
CL_DIR_2019_64 = Path(CL_DIR_2019_64).resolve()


CL_ORIGIN = CL_DIR.joinpath("cl2.exe")
CURRENT = Path(__file__).resolve().parent

DB = CURRENT.joinpath("db.sqlite3")

import sys

if getattr(sys, "frozen", False):
    CURRENT = Path(sys.executable).resolve().parent
    DB = CURRENT.parent.joinpath("db.sqlite3")
