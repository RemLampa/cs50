#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int n;

    // Get input from user
    do
    {
        printf("Height: ");
        n = get_int();
    }
    // limit the height
    while (n < 0 || n > 23);

    // print the pyramid
    for (int i = 0; i < n; i++)
    {
        // print spaces on the left side
        for (int j = 0; j < n - (i + 1); j++)
        {
            printf(" ");
        }

        // print left side blocks
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }

        // print middle gap
        printf("  ");

        // print right side blocks
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }

        // go to next line
        printf("\n");
    }

    return 0;
}
