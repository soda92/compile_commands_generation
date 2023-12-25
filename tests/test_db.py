# %%
import psycopg2

connection = psycopg2.connect(
    host="localhost", database="postgres", user="postgres", password=""
)

# %%
with connection.cursor() as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS test(r1 varchar(20), r2 varchar(20))")

# %%
with connection.cursor() as cursor:
    cursor.execute("INSERT INTO test(r1, r2) values ('a', 'b'), ('c', 'd'), ('e', 'f')")

# %%
with connection.cursor() as cursor:
    cursor.execute("SELECT r1, r2 FROM test")
    result = cursor.fetchall()
    for row in result:
        print(row[0], row[1])

# %%
