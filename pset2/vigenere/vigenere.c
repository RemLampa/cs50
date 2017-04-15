#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

#define true 1
#define false 0

int main (int argc, string argv[])
{
    int arg_is_alpha = true;

    if (argc == 2)
    {
        for (int i = 0; argv[1][i] != '\0'; i++)
        {
            if (isalpha(argv[1][i]) == false)
            {
                arg_is_alpha = false;
                break;
            }
        }
    }

    // ensure that there are only 2 command line arguments
    // and that the provided cipher key consists only of purely
    // alphabetical characters
    if (argc != 2 || arg_is_alpha == false)
    {
        printf("Usage error!\n");
        printf("Syntax: ./vigenere keyword\n");
        printf("keyword must consist of alphabetical characters only\n");
        return 1;
    }

    // convert cipher keyword into an array of 
    // alphabetical shift indices
    int key_length = strlen(argv[1]);

    int key_array[key_length];

    for (int i = 0; argv[1][i] != '\0'; i++)
    {
        key_array[i] = toupper(argv[1][i]) - 65;
    }

    // get plain text from user 
    printf("plaintext: ");
    
    string plain_text = get_string();

    // encrypt
    int text_length = strlen(plain_text);

    char cipher_text[text_length + 1];

    for (int i = 0, j = 0; plain_text[i] != '\0'; i++)
    {
        if (isalpha(plain_text[i]) == false)
        {
            cipher_text[i] = plain_text[i];
            continue;
        }

        int shift_index = (isupper(plain_text[i])) ? 65 : 97;

        int temp_char = plain_text[i] - shift_index;

        char cipher_char = (temp_char + key_array[j]) % 26;

        cipher_text[i] = cipher_char + shift_index;

        j++;

        if (j >= key_length) j = 0;
    }

    // terminate character array with null
    cipher_text[text_length] = '\0';

    printf("ciphertext: %s\n", cipher_text);

    return 0;
}

