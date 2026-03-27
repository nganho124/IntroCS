from cs50 import SQL

db = SQL("sqlite:///favorites.db")

rows = db.execute("SELECT Language, COUNT(*) AS n FROM favorites GROUP BY Language ORDER BY n DESC")

for row in rows:
    print(row["Language"], row["n"])
