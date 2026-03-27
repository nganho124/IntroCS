#include <cs50.h>
#include <stdio.h>

int get_positive_change(void);
int return_number_of_coins(int change);

int main(void)
{
    int change = get_positive_change();
    int coin = return_number_of_coins(change);
    printf("%i\n", coin);
}

int get_positive_change(void)
{
    int change;
    do
    {
        change = get_int("Change owed: ");
    }
    while (change < 0);
    return change;
}

int return_number_of_coins(int change)
{
    int no_coin = 0;

    // Quarters (25 cents)
    no_coin += change / 25;
    change %= 25;

    // Dimes (10 cents)
    no_coin += change / 10;
    change %= 10;

    // Nickels (5 cents)
    no_coin += change / 5;
    change %= 5;

    // Pennies (1 cent) - whatever remains
    no_coin += change;

    return no_coin;
}
