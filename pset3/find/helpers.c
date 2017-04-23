/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */
 
#include <cs50.h>
#include <string.h>

#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
bool search(int value, int values[], int n)
{
    if (n <= 0) return false;

    int lower_limit = 0;
    int upper_limit = n - 1;
    int middle;

    // binary search
    while (lower_limit <= upper_limit) {
        middle = (upper_limit + lower_limit) / 2;

        // return true if value found
        if (value == values[middle]) return true;

        // if value is less than middle value, move upper bound
        if (value < values[middle]) upper_limit = middle - 1;

        // if value is more than middle value, move lower bound
        if (value > values[middle]) lower_limit = middle + 1;
    }

    return false;
}

/**
 * Sorts array of n values.
 */
void sort(int values[], int n)
{
    // initialize counting array with zero values
    const int max = 65536;
    int counting_array[max];
    memset(counting_array, 0, sizeof(counting_array));

    // populate counting array
    for (int i = 0; i < n; i++) {
        int this_number = values[i];
        counting_array[this_number]++;
    }

    // use counting array to fill sorted
    // values of original array
    for (int i = 0, j = 0; i < max; i++) {
        int occurences = counting_array[i];

        for (int k = 0; k < occurences; k++) {
            values[j] = i;

            j++;
        }
    }

    return;
}
