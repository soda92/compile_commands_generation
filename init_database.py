from defines import DB
import sqlite3

con = sqlite3.connect(DB)
with con:
    con.execute("CREATE TABLE IF NOT EXISTS compile_commands(file, directory, command)")
