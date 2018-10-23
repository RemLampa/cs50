import sys
from crypt import crypt


def main():
    if len(sys.argv) != 2:
        print('Usage error!')
        print('Syntax: python crack.py hash')
        print('hash is DES-hashed password')
        sys.exit(1)

    hashed_password = sys.argv[1]

    characters = list(range(0, 1)) + list(range(65, 91)) + list(range(97, 123))

    # initialize guess string
    guess = ''

    # loop for 4th character
    for i in characters:

        # loop for 3rd character
        for j in characters:

            # loop for 2nd character
            for x in characters:

                # loop for 1st character
                for y in characters:

                    # build guess string
                    guess = guess if i == 0 else guess + chr(i)
                    guess = guess if j == 0 else guess + chr(j)
                    guess = guess if x == 0 else guess + chr(x)
                    guess = guess if y == 0 else guess + chr(y)

                    found_match = check_match(hashed_password, guess)

                    if found_match:
                        break

                    # reset guess string
                    guess = ''

                if found_match:
                    break

            if found_match:
                break

        if found_match:
            break

    if found_match:
        print(guess)
    else:
        print('No possible password found. Invalid hash?')

    sys.exit(0)


def check_match(hashed_password, guess):
    # extract salt from hashed_password
    salt = hashed_password[0:2]

    # encrypt guess
    guess_hash = crypt(guess, salt)

    return hashed_password == guess_hash


if __name__ == '__main__':
    main()