from cs50 import get_string

number = get_string("Number: ")


def check_valid(number):
    sum_num = 0
    check = ""
    if len(number) % 2 == 0:
        for i, char in enumerate(number):
            if i % 2 == 0:
                check = check + str(2 * int(char))
            else:
                sum_num += int(char)
    else:
        for i, char in enumerate(number):
            if i % 2 != 0:
                check = check + str(2 * int(char))
            else:
                sum_num += int(char)

    for i in check:
        sum_num += int(i)

    if sum_num % 10 == 0:
        return True
    else:
        return False


if len(number) == 15 and number[:2] in ["34", "37"] and check_valid(number):
    print("AMEX")
elif len(number) == 16 and number[:2] in ['51', '52', '53', '54', '55'] and check_valid(number):
    print("MASTERCARD")
elif len(number) in [13, 16] and number[:1] == "4" and check_valid(number):
    print("VISA")
else:
    print("INVALID")
