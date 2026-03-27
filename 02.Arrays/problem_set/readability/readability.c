#include <ctype.h>
#include <cs50.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    // Prompt the user for some text
    string input = get_string("Input: ");

    // Count the number of letters, words, and sentences in the text
    int sentence_count = 0;
    int letter_count = 0;
    int word_count = 1;

    for (int i = 0; i < strlen(input); i++)
    {
        if (input[i] == ' ')
        {
            word_count++;
        }
        else if (input[i] == '.' || input[i] == '?' || input[i] == '!')
        {
            sentence_count++;
        }
        else if (isalpha(input[i]))
        {
            letter_count++;
        }
    }

    // Compute the Coleman-Liau index
    float L = ((float) letter_count / word_count) * 100;
    float S = ((float) sentence_count / word_count) * 100;
    float index = 0.0588 * L - 0.296 * S - 15.8;
    int grade = round(index);

    // Print the grade level
    if (grade >= 16)
    {
        printf("Grade 16+\n");
    }
    else if (grade < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}
