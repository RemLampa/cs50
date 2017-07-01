from cs50 import get_int

while True:
    print('Height: ', end='')
   
    n = get_int()
    
    if n >= 0 and n <= 23:
        break
    else:
        print('Height must be between 0 and 23')
        print()

for i in range(0, n):
    # Add left side spaces
    for j in range(0, n-(i+1)):
        print(' ', end='')
    
    # Add left side hashes
    for j in range(0, i+1):
        print('#', end='')
    
    # Add middle spaces
    print('  ', end='')
    
    # Add right side hashes
    for j in range(0, i+1):
        print('#', end='')
        
    print()