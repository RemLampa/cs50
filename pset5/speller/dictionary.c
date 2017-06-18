/**
 * Implements a dictionary's functionality.
 */

#include <stdlib.h>
#include <stdio.h>
#include <stdbool.h>
#include <string.h>
#include <ctype.h>

#include "dictionary.h"

// trie struct declaration
struct _node
{
    bool is_word;

    struct _node * nodes[27];
};

// dictionary pointer
node * loaded_dictionary;

// number of words loaded in dictionary
unsigned int words;

/**
 * Returns true if word is in dictionary else false.
 */
bool check(const char *word)
{
    node * current_node = loaded_dictionary;
    
    const unsigned int length = strlen(word);
    
    for (int i = 0; i <= length; i++)
    {
        // end of word
        if (i == length)
        {
            if  (current_node->is_word == false) return false;
        }
        else {
            unsigned int index = shift_index(word[i]);
            
            // no word has the current letter in its sequence        
            if (current_node->nodes[index] == NULL) return false;
            
            // move on to next letter
            current_node = current_node->nodes[index];
        }
    }
    
    return true;
}

/**
 * Loads dictionary into memory. Returns true if successful else false.
 */
bool load(const char *dictionary)
{
    // open dictionary file
    FILE *fp = fopen(dictionary, "r");
    
    // file open failed
    if (fp == NULL) return false;
    
    // initialize dictionary trie node
    loaded_dictionary = init_node();
    
    words = 0;
    
    node * current_node = loaded_dictionary;
    
    // read file one character at a time
    for (int c = fgetc(fp); c != EOF; c = fgetc(fp))
    {
        // end of line, thus end of word
        if (c == '\n')
        {
            current_node->is_word = true;
            
            current_node = loaded_dictionary;
            
            words++;
        }
        else
        {
            unsigned int index = shift_index(c);
            
            // if node for current letter does not exist yet, initialize a node for it
            if (current_node->nodes[index] == NULL) current_node->nodes[index] = init_node();

            // move to the next node
            current_node = current_node->nodes[index];
        }
    }
    
    // check if file read errors occured
    if (ferror(fp)) return false;
    
    // close file
    fclose(fp);

    // successfully loaded dictionary
    return true;
}

/**
 * Returns number of words in dictionary if loaded else 0 if not yet loaded.
 */
unsigned int size(void)
{
    return words;
}

/**
 * Unloads dictionary from memory. Returns true if successful else false.
 */
bool unload(void)
{
    free_node(loaded_dictionary);
    
    return true;
}

/**
 * Initialize a node
 */
node * init_node(void)
{
    node * new_node = malloc(sizeof(node));
    
    new_node->is_word = false;
    
    // set all sub-nodes to NULL
    for(int i = 0; i < 27; i++) new_node->nodes[i] = NULL;
    
    return new_node;
}

/**
 * Deallocate memory given to a node
 */
void free_node(node * current_node)
{
    for (int i = 0; i < 27; i++)
    {
        if (current_node->nodes[i] != NULL)
        {
            free_node(current_node->nodes[i]);
        }
    }

    free(current_node);
}

/**
 * Shifts ASCII to zero index
 */
unsigned int shift_index(char c)
{
    return c == '\'' ? 26 : tolower(c) - 97;
}
