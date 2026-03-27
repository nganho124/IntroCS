#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int get_score(string s);

int main(void)
{

    string s1 = get_string("Player 1: ");
    string s2 = get_string("Player 2: ");
    int score1 = get_score(s1);
    int score2 = get_score(s2);

    if (score1 < score2) {
        printf("Player 2 wins!\n");
    }
    else if (score1 > score2) {
        printf("Player 1 wins!\n");
    }
    else {
        printf("Ties!\n");
    }


}


int get_score(string s) {

    // Point of each character in Scrabble
    int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    int score = 0;
    for (int i = 0; i < strlen(s); i++) {
        if (isalpha(s[i])) {
            score = score + POINTS[toupper(s[i]) - 'A'];
        }
        else {
            score = score + 0;
        }

    }
    return score;

}
