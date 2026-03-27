#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void) {

    string names[] = {"Yuliia", "David", "John"};
    string numbers[] = {"+1-123-414-1223", "+1-123-412-1223", "+1-112-434-1267"};

    string name = get_string("Name: ");
    for (int i = 0; i < 3; i++) {
        if (strcmp(name, names[i]) == 0) {
            printf("Found %s\n", numbers[i]);
            return 0;
        }
    }
    printf("Not found\n");
    return 1;
}
