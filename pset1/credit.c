#include <stdio.h>
#include <cs50.h>

long long power(int base, unsigned int pow);

int main(void)
{
    long long card_number;
    int sum = 0;
    int first_digit = 0;
    int first_two_digits = 0;
    int digits;

    do
    {
        printf("Number: ");
        card_number = get_long_long();
    }
    while (card_number < 0);

    for (digits = 0; card_number >= 1; digits++)
    {
        int remainder = card_number % 10;

        if (card_number >= 10 && card_number < 100)
        {
            first_two_digits = card_number;
        }

        if (card_number < 10)
        {
            first_digit = card_number;
        }

        if (digits % 2 == 1)
        {
            int even = remainder * 2;

            if (even > 9)
            {
                even = even / 10 + even % 10;
            }

            sum += even;
        }
        else
        {
            sum += remainder;
        }

        card_number /= 10;
    }

    if (sum % 10 == 0)
    {
        // American Express
        if (digits == 15 && (first_two_digits == 34 || first_two_digits == 37))
        {
            printf("AMEX\n");
        }
        // MasterCard
        else if (digits == 16 && first_two_digits >= 51 && first_two_digits <= 55)
        {
            printf("MASTERCARD\n");
        }
        // VISA
        else if ((digits == 13 || digits == 16) && first_digit == 4)
        {
            printf("VISA\n");
        }
        // INVALID
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }

    return 0;
}
