import random
import nltk
from nltk.corpus import words
from colorama import Fore, Style, init
init(autoreset = True)

# Get all 5-letter words, lowercase only, no punctuation or digits
five_letter_words = [word.upper() for word in words.words() if len(word) == 5 and word.isalpha()]

# Pick one at random
word_of_the_day = (random.choice(five_letter_words))
print(word_of_the_day)




#User Guess Area


i = 0
while i<6:
    guess = input("Enter a 5-letter word: _ _ _ _ _").upper()

    while len(guess) != 5 or not guess.isalpha():
        print("Invalid entry, 5 letter words only")
        guess = input("Enter a 5-letter word: _ _ _ _ _").upper()

    if guess.upper() == word_of_the_day:
        print("WELL DONE! You guessed it!")
        break
    else:
        #print("Feedback: ", end= "")
        for j in range(5):
            if guess[j] == word_of_the_day[j]:
                print(Fore.GREEN + guess[j], end = " ") #correct position
            elif guess[j] in word_of_the_day:
                print(Fore.YELLOW + guess[j], end=" ") #in word, wrong spot
            else:
                print(Fore.LIGHTBLACK_EX + guess[j], end= " ")
        print("\n")

    

    


    i+=1

print(f"The word was {word_of_the_day}, nice try!")