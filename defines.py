from pathlib import Path

CL_DIR = "C:/Program Files (x86)/Microsoft Visual Studio 9.0/VC/bin/"
CL_DIR = Path(CL_DIR).resolve()


CL_ORIGIN = CL_DIR.joinpath("cl2.exe")
CURRENT = Path(__file__).resolve().parent

DB = CURRENT.joinpath("db.sqlite3")
