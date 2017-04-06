#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <cs50.h>

int main (void)
{
  string name = NULL;
  char initials[5];

  name = get_string();

  // if user input begins in a letter
  if (name[0] != ' ') 
  {
    initials[0] = toupper(name[0]);
  }

  int length = strlen(name);
  for (int i = 0; i < length; i++)
  {
    // if space succeeded by a letter
    if(name[i] == ' ' && name[i+1] != ' ')
    {
      char temp_str[2];
      temp_str[0] = toupper(name[i+1]);
      temp_str[1] = '\0';

      strcat(initials, temp_str);
    }
  }

  printf("%s\n", initials);

  return 0;
}
