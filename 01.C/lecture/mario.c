#include <stdio.h>

void print_row(int n);

int main(void)
{
    int n = 4;

    // Print n rows
    for (int i = 0; i < n; i++)
    {
        print_row(n);
    }
}

void print_row(int n)
{
    for (int j = 0; j < n; j++)
    {
        printf("#");
    }
    printf("\n");
}
