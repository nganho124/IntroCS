#include <cs50.h>
#include <stdio.h>

int get_positive_height();
void draw_lines(int height);

int main(void)
{

    int height = get_positive_height();
    draw_lines(height);
}

int get_positive_height(void)
{

    int height;
    do
    {
        height = get_int("Height: ");
    }
    while (height <= 0);
    return height;
}

void draw_lines(int height)
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height + i + 3; j++)
        {
            if (j < height - i - 1 || j == height || j == height + 1)
            {
                printf(" ");
            }
            else
            {
                printf("#");
            }
        }
        printf("\n");
    }
}
