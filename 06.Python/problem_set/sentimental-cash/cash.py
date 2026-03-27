from cs50 import get_float

change = get_float("Change: ")
num_coins = 0
if change < 0:
    change = get_float("Change: ")

if change >= 0.25:
    quarters = int(change // 0.25)
    num_coins += quarters
    change = round(change % 0.25, 2)
if change >= 0.10:
    dimes = int(change // 0.10)
    num_coins += dimes
    change = round(change % 0.10, 2)
if change >= 0.05:
    nickels = int(change // 0.05)
    num_coins += nickels
    change = round(change % 0.05, 2)
if change >= 0.01:
    pennies = change // 0.01
    num_coins += pennies

print(num_coins)
