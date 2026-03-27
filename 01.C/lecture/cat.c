#include <stdio.h>
#include <cs50.h>

void meow(int n);
int get_positive_int(void);

int main(void)
{
    int times = get_positive_int();
    meow(times);
}

int get_positive_int(void)
{
    int n;
    do
    {
        n = get_int("Number: ");
    }
    while (n < 1);
    return n;
}

void meow(int times)
{
    for (int i = 0; i < times; i++)
    {
       printf("meow\n");
    }

}
