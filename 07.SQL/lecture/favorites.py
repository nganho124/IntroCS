import csv

with open("favorites.csv", "r") as file:
    reader = csv.DictReader(file)
    count = {}
    for row in reader:
        favorite = row["Language"]
        if favorite in count:
            count[favorite] += 1
        else:
            count[favorite] = 1

for favorite in sorted(count, key=count.get, reverse=True):
    print(f"{favorite}: {count[favorite]}")

