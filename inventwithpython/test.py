num = 3

total = 10
tries = 1

while tries <= total:
    
    while True:
        ans = input('Enter your guess: ')
        if ans.isdigit():
            break
        else:
            print('Enter a digit')    
    
    if ans == num:
        print(f"Correct! You guess the number {num} correctly on your {tries}'s try!")
        break
    else:
        tries +=1
        print(f"Wrong! you got {total - tries + 1} more turns!")

        
