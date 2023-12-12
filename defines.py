from pathlib import Path

CL_DIR = Path("C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/bin/").resolve()
CL_DIR_2019_64 = Path(
    "C:/Program Files (x86)/Microsoft Visual Studio/2019/Professional/VC/Tools/MSVC/14.29.30133/bin/Hostx64/x64"
).resolve()


def get_cl_dir(vs_version: str):
    if vs_version == "2008":
        return CL_DIR
    elif vs_version == "2019_64":
        return CL_DIR_2019_64


def get_cl_origin(vs_version: str):
    cl_dir = get_cl_dir(vs_version=vs_version)
    return cl_dir.joinpath("cl2.exe")


CURRENT = Path(__file__).resolve().parent

DB = CURRENT.joinpath("db.sqlite3")

import sys

if getattr(sys, "frozen", False):
    CURRENT = Path(sys.executable).resolve().parent
    DB = CURRENT.parent.joinpath("db.sqlite3")
