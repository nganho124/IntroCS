#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int main(int argc, string argv[])
{
    // Ensure there is exactly one command-line argument
    if (argc == 2)
    {
        // Check if the key contains only digits
        for (int i = 0; argv[1][i] != '\0'; i++)
        {
            if (!isdigit(argv[1][i]))
            {
                printf("Usage: ./caesar key\n");
                return 1;
            }
        }

        // Convert key to integer
        int key = atoi(argv[1]);

        // Get plaintext from user
        string plain_text = get_string("plaintext: ");

        // Prepare space for ciphertext (plus null terminator)
        char cipher_text[strlen(plain_text) + 1];

        // Encrypt each character
        for (int i = 0; i < strlen(plain_text); i++)
        {
            if (islower(plain_text[i]))
            {
                cipher_text[i] = ((plain_text[i] - 'a' + key) % 26) + 'a';
            }
            else if (isupper(plain_text[i]))
            {
                cipher_text[i] = ((plain_text[i] - 'A' + key) % 26) + 'A';
            }
            else
            {
                cipher_text[i] = plain_text[i];
            }
        }

        // Null-terminate the ciphertext string
        cipher_text[strlen(plain_text)] = '\0';

        // Print the ciphertext
        printf("ciphertext: %s\n", cipher_text);
        return 0;
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}
