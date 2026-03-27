#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

long get_good_long(void);
bool check_sum(long card_number);
string check_valid_card(long card_number);

int main(void)
{

    long card_number = get_good_long();
    if (check_sum(card_number))
    {
        string result = check_valid_card(card_number);
        printf("%s\n", result);
    }
    else
    {
        printf("INVALID\n");
    }
}

long get_good_long(void)
{
    long card_number;
    do
    {
        card_number = get_long("Number: ");
    }
    while (card_number < 0);
    return card_number;
}

string check_valid_card(long card_number)
{

    // int number_digits = (int) log10(llabs(card_number)) + 1;
    char str_num[32]; // enough for 19 digits + '\0'
    int number_digits = snprintf(str_num, sizeof(str_num), "%ld", card_number);

    if ((number_digits == 15) && (strncmp(str_num, "34", 2) == 0 || strncmp(str_num, "37", 2) == 0))
    {
        return "AMEX";
    }
    else if ((number_digits == 16) &&
             (strncmp(str_num, "51", 2) == 0 || strncmp(str_num, "52", 2) == 0 ||
              strncmp(str_num, "53", 2) == 0 || strncmp(str_num, "54", 2) == 0 ||
              strncmp(str_num, "55", 2) == 0))
    {
        return "MASTERCARD";
    }
    else if ((number_digits == 16 || number_digits == 13) && (strncmp(str_num, "4", 1) == 0))
    {
        return "VISA";
    }
    else
    {
        return "INVALID";
    }
}

bool check_sum(long card_number)
{

    // long card_number = 4003600000000014;
    long temp = card_number;
    int sum = 0;
    int position = 0;

    while (temp > 0)
    {
        int digit = temp % 10;

        if (position % 2 == 0)
        {
            // every other digit starting from the right (unchanged)
            sum += digit;
        }
        else
        {
            // doubled digit
            int doubled = digit * 2;
            if (doubled > 9)
            {
                sum += doubled - 9; // same as summing digits
            }
            else
            {
                sum += doubled;
            }
        }

        temp /= 10;
        position++;
    }

    if (sum % 10 == 0)
    {
        return true;
    }
    else
    {
        return false;
    }

    // return 0;
}
