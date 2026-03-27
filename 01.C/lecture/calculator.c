#include <cs50.h>
#include <stdio.h>

int main(void)
{
    long dollars = 1;
    while (true)
    {
        char c = get_char("Here is $%li. Double it and give it to the next person? ", dollars);
        if (c == 'y')
        {
            dollars = dollars * 2;
        }
        else {
            break;

        }

    }
    printf("Here is %li dollars\n", dollars);
}
