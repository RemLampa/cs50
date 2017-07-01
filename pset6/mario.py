from cs50 import get_int

while True:
    print('Height: ', end='')
   
    n = get_int()
    
    if n >= 0 and n <= 23:
        break
    else:
        print('Height must be between 0 and 23')
        print()

for i in range(n):
    # Add left side spaces
    for j in range(n-(i+1)):
        print(' ', end='')
    
    # Add left side hashes
    for j in range(i+1):
        print('#', end='')
    
    # Add middle spaces
    print('  ', end='')
    
    # Add right side hashes
    for j in range(i+1):
        print('#', end='')
        
    print()