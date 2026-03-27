#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // Ensure there is exactly one command-line argument & key length is 26
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    else
    {
        // Check that all characters are alphabetic
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (!isalpha(argv[1][i]))
            {
                printf("Key must contain only letters.\n");
                return 1;
            }
        }

        // Check for duplicate letters
        for (int i = 0; i < strlen(argv[1]) - 1; i++)
        {
            for (int j = i + 1; j < strlen(argv[1]); j++)
            {
                if (tolower(argv[1][i]) == tolower(argv[1][j]))
                {
                    printf("Key must not contain repeated letters.\n");
                    return 1;
                }
            }
        }

        // Get plaintext from user
        string in_str = get_string("plaintext: ");

        // Prepare space for ciphertext (plus null terminator)
        char out_str[strlen(in_str) + 1];

        // Encrypt each character
        for (int i = 0; i < strlen(in_str); i++)
        {
            if (isalpha(in_str[i]))
            {
                if (islower(in_str[i]))
                {
                    int key = in_str[i] - 'a';
                    out_str[i] = tolower(argv[1][key]);
                }
                else
                {
                    int key = in_str[i] - 'A';
                    out_str[i] = toupper(argv[1][key]);
                }
            }
            else
            {
                out_str[i] = in_str[i];
            }
        }

        // Null-terminate the ciphertext string
        out_str[strlen(in_str)] = '\0';

        // Output the ciphertext
        printf("ciphertext: %s\n", out_str);
        return 0;
    }
}
