#define _XOPEN_SOURCE

#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>

#define true 1
#define false 0

int check_match(string hash, string guess);

int main(int argc, string argv[])
{
    // ensure that there are exactly 2 command line arguments
    if (argc != 2)
    {
        printf("Usage error!\n");
        printf("Syntax: ./crack hash\n");
        printf("hash is DES-hashed password\n");
        return 1;
    }

    string hash = argv[1];

    char guess[5] = {'\0'};

    int found_match = false;

    // for character case checking & toggling
    int is_i_upper = true, is_j_upper = true, is_k_upper = true, is_x_upper = true;

    // FOR ALL LOOPS: if uppercase, then repeat step for lowercase

    // loop for 4th character
    for (int i = 65; i <= 90; i++)
    {
        // loop for 3rd character
        for (int j = 65; j <= 90; j++)
        {
            // loop for 2nd character
            for (int k = 65; k <= 90; k++)
            {
                // loop for 1st character
                for (int x = 65; x <= 90; x++)
                {
                    if (is_x_upper)
                    {
                        guess[0] = (char) x;
                        x--;
                    }
                    else
                    {
                        guess[0] = tolower(guess[0]);
                    }

                    found_match = check_match(hash, guess);

                    is_x_upper = !is_x_upper;

                    if (found_match)
                    {
                        break;
                    }
                }
                // end loop for 1st character

                if (found_match)
                {
                    break;
                }

                if (is_k_upper)
                {
                    guess[1] = (char) k;
                    k--;
                }
                else
                {
                    guess[1] = tolower(guess[1]);
                }

                is_k_upper = !is_k_upper;
            }
            // end loop for 2nd character

            if (found_match)
            {
                break;
            }

            if (is_j_upper)
            {
                guess[2] = (char) j;
                j--;
            }
            else
            {
                guess[2] = tolower(guess[2]);
            }

            is_j_upper = !is_j_upper;
        }
        // end loop for 3rd character

        if (found_match)
        {
            break;
        }

        if (is_i_upper)
        {
            guess[3] = (char) i;
            i--;
        }
        else
        {
            guess[3] = tolower(guess[3]);
        }

        is_i_upper = !is_i_upper;
    }
    // end loop for 4th character

    if (found_match)
    {
        printf("%s\n", guess);
    }
    else
    {
        printf("No possible password found. Invalid hash?\n");
    }

    return 0;
}

int check_match(string hash, string guess)
{
    char salt[3];

    // extract salt from hash
    strncpy(salt, hash, 2);

    char *guess_hash = crypt(guess, salt);

    // strcmp returns 0 if match
    return (strcmp(hash, guess_hash) == 0) ? true : false;
}
