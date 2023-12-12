from defines import DB
import sqlite3

con = sqlite3.connect(DB)
with con:
    con.execute("DROP TABLE IF EXISTS compile_commands")
