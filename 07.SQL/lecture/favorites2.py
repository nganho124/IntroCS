from cs50 import SQL

db = SQL("sqlite:///favorites.db")

favorite = input("Favorites: ")

rows = db.execute(f"SELECT COUNT(*) AS n FROM favorites WHERE Problem = ?", favorite)

row = rows[0]

print(row["n"])

