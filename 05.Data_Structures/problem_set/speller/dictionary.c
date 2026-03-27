// Implements a dictionary's functionality

#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // 1. Hash the word to find which bucket to search
    int bucket = hash(word);

    // 2. Traverse the linked list in that bucket
    for (node *cursor = table[bucket]; cursor != NULL; cursor = cursor->next)
    {
        // 3. Compare words (case-insensitive)
        if (strcasecmp(cursor->word, word) == 0)
        {
            return true; // Found it!
        }
    }

    // 4. Word not found
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    unsigned int hash_value = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash_value = (hash_value << 2) ^ toupper(word[i]);
    }
    return hash_value % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // Initialize hash table to NULL
    for (int i = 0; i < N; i++)
    {
        table[i] = NULL;
    }
    // Open the dictionary file
    FILE *source = fopen(dictionary, "r");

    if (source == NULL)
    {
        return false;
    }
    // Read each word in the file
    char word[LENGTH + 1];
    while (fscanf(source, "%s", word) != EOF)
    {
        // 1. Allocate memory for new node
        node *new_node = malloc(sizeof(node));
        if (new_node == NULL)
            return false;

        // 2. Copy word into node
        strcpy(new_node->word, word);

        // 3. Hash the word to get bucket index
        int bucket = hash(word);

        // 4. Insert at beginning of linked list
        new_node->next = table[bucket];
        table[bucket] = new_node;
    }

    fclose(source);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    unsigned int count = 0;
    for (int i = 0; i < N; i++)
    {
        for (node *cursor = table[i]; cursor != NULL; cursor = cursor->next)
        {
            count++;
        }
    }
    return count;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    // For each bucket in the hash table
    for (int i = 0; i < N; i++)
    {
        // Traverse and free each node in the linked list
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}
