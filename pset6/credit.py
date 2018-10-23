from cs50 import get_int

while True:
    print('Card Number: ', end='')

    card_number = get_int()

    if card_number >= 0:
        break

total = 0
first_digit = 0
first_two_digits = 0
digits = 0

while card_number >= 1:
    remainder = card_number % 10

    if card_number >= 10 and card_number < 100:
        first_two_digits = card_number

    if card_number < 10:
        first_digit = card_number

    if digits % 2 == 1:
        even = remainder * 2

        if even > 9:
            even = even // 10 + even % 10

        total += even
    else:
        total += remainder

    card_number //= 10

    digits += 1

if total%10 == 0:
    # American Express
    if digits == 15 and (first_two_digits == 34 or first_two_digits == 37):
        print('AMEX');
    # MasterCard
    elif digits == 16 and first_two_digits >= 51 and first_two_digits <= 55:
        print('MASTERCARD')
    # VISA
    elif (digits == 13 or digits == 16) and first_digit == 4:
        print('VISA')
    else:
        print('INVALID')
else:
    print('INVALID')