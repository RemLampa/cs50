#include <stdio.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

#define true 1
#define false 0

int main (int argc, string argv[])
{
    printf("%i\n", argc);
  
    for (int i = 0; i < argc; i++)
    {
        printf("%s\n", argv[i]);
    }

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

    if (argc != 2 || arg_is_alpha == false)
    {
        printf("Error!");
        return 1;
    }
    else
    {
        
    }

    return 0;
}

