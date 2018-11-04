// Helper functions for music

#include <cs50.h>
#include <math.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

#include "helpers.h"

// Converts a fraction formatted as X/Y to eighths
int duration(string fraction)
{
    int numerator = fraction[0] - '0';
    int denominator = fraction[2] - '0';

    return 8 * numerator / denominator;
}

// Calculates frequency (in Hz) of a note
int frequency(string note)
{
    char *key = (char *)malloc(3);
    char *octave = (char *)malloc(2);

    if (strlen(note) == 2)
    {
        strncpy(key, note, 1);
        strncpy(octave, note + 1, 1);

        key[1] = '\0';
        octave[1] = '\0';
    }
    else
    {
        strncpy(key, note, 2);
        strncpy(octave, note + 2, 1);

        key[2] = '\0';
        octave[1] = '\0';
    }

    int key_val;

    // Assign distances with respect to A in the same octave
    // Negative denotes left of A
    if (strcmp(key, "A") == 0)
    {
        key_val = 0;
    }
    else if (strcmp(key, "A#") == 0 || strcmp(key, "Bb") == 0)
    {
        key_val = 1;
    }
    else if (strcmp(key, "B") == 0)
    {
        key_val = 2;
    }
    else if (strcmp(key, "C") == 0)
    {
        key_val = -9;
    }
    else if (strcmp(key, "C#") == 0 || strcmp(key, "Db") == 0)
    {
        key_val = -8;
    }
    else if (strcmp(key, "D") == 0)
    {
        key_val = -7;
    }
    else if (strcmp(key, "D#") == 0 || strcmp(key, "Eb") == 0)
    {
        key_val = -6;
    }
    else if (strcmp(key, "E") == 0)
    {
        key_val = -5;
    }
    else if (strcmp(key, "F") == 0)
    {
        key_val = -4;
    }
    else if (strcmp(key, "F#") == 0 || strcmp(key, "Gb") == 0)
    {
        key_val = -3;
    }
    else if (strcmp(key, "G") == 0)
    {
        key_val = -2;
    }
    else if (strcmp(key, "G#") == 0 || strcmp(key, "Ab") == 0)
    {
        key_val = -1;
    }
    else
    {
        printf("Invalid note encountered!");

        exit(-1);
    }

    // get actual distance accdg to the note's octave
    // distance = Distance of Key from its octaves' A note + (current octave - 4) * 12
    int distance = key_val + (atoi(octave) - 4) * 12;

    // freq = (2 ^ n/12) * 440;
    int freq = round(pow(2.0, distance / 12.0) * 440);

    return freq;
}

// Determines whether a string represents a rest
bool is_rest(string s)
{
    return *s == '\0';
}
