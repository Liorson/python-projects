#creating a hangman game
HANGMAN_ASCII_ART = "Welcome to the game Hangman"
print(HANGMAN_ASCII_ART)
#the title
print("""
  _    _                                         
 | |  | |                                        
 | |__| | __ _ _ __   __ _ _ __ ___   __ _ _ __  
 |  __  |/ _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
 | |  | | (_| | | | | (_| | | | | | | (_| | | | |
 |_|  |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                      __/ |                      
                     |___/ """)

#####################################################################################################                  
import random
# a function that will up;aod a word file and will choose a word for the player
def choose_word(file_path, index):
  # creating a list for all not duplicate elements
  none_duplicate_list=[]
  #opening the file
  file_list=open(file_path , 'r')
  file1=file_list.read()
  #changing the content of the file (strings) to a list
  file1_list=file1.split(' ')
  #uploading all the not duplictes words to the list before "none_duplicate_list"
  for word in file1_list:
    if word not in none_duplicate_list:
      none_duplicate_list.append(word)
 # print(none_duplicate_list)
  # calculating the index in the len of the list
  updated_index=index % len(file1_list)
  # tuple of not duplicate len list and the chosen word
  hangman_tuple=(len(none_duplicate_list), file1_list[updated_index])
  print(hangman_tuple)
  #creating a global var as the secret word of the game
  global secret_word
  secret_word=file1_list[updated_index]
  
word_file_path="C:\data4s lior\python py\words.txt"
index=random.randint(0 , 100)
choose_word(word_file_path ,index )
#creating lines as the lentgh of the secret word
progres_line=('_ '  * len(secret_word))
print(progres_line)
####################################################################################################
# presenting the max tries any player have 
MAX_TRIES= len(secret_word) + 2
print('max tries= ' , MAX_TRIES)   
#####################################################################################################
# a list that will contain the old letters the player chose
old_letters_guessed=[]
#changing the progres_line string to a list
list_progres_line=progres_line.split()
# a loop that will return to the guess a word element until the end of the game
while (list_progres_line.count('_') > 0) and (len(old_letters_guessed) < MAX_TRIES) :
  # a condistion that will brake the loop if the player lost and used all his tries  
  # requesting to guess a letter and converting the capital letters to small letters
  #input that will start a checking trail if the letter match 
  guess_a_letter=input('Guess a letter: ')
  guess_a_letter=guess_a_letter.lower()
  # a condition that will take me out of the loop if i would like to
  if guess_a_letter  == 'break' :
    break
 
############################a#########################################################################
   # a function that will make sure the player insert only one english letter that was not choose before
   # the function also will add the letters that will pass the if to the list
  def is_valid_input(letter_guessed, old_letters_guessed):
        if guess_a_letter.isalpha() == True and len(guess_a_letter) != 1:
           old_letters_guessed.sort()
           print('X\n' + '->'.join(old_letters_guessed) , '\nFalse')
           return None
        elif guess_a_letter.isalpha() == False and len(guess_a_letter) == 1:
             old_letters_guessed.sort()
             print('X\n' + '->'.join(old_letters_guessed) , '\nFalse')
             return None 
        elif len(guess_a_letter) != 1 and guess_a_letter.isalpha() == False:
             old_letters_guessed.sort()
             print('X\n' + '->'.join(old_letters_guessed) , '\nFalse')
             return None
        elif old_letters_guessed.count(guess_a_letter) >= 1:
             old_letters_guessed.sort()
             print('X\n' + '->'.join(old_letters_guessed) , '\nFalse')
        else:
             old_letters_guessed.append(guess_a_letter)
             print('letter is valid')
             return old_letters_guessed
     
  #activating the function  
  is_valid_input(guess_a_letter, old_letters_guessed)   
#####################################################################################################
    #reminder of what the player guessed so far
  print('old letters: ' , old_letters_guessed)
    # a function that will show the progress of the player
  def show_hidden_word(the_secret_word, old_letters_guessed):
    for i in range(len(the_secret_word) ):
      if the_secret_word[i] == guess_a_letter:
        list_progres_line[i]=guess_a_letter
      #transfering the list back to a string       
    new_progres_line= ' '.join(list_progres_line)       
    print(new_progres_line)
    return new_progres_line
       
  #activating the function        
  show_hidden_word(secret_word, old_letters_guessed)
#################################################################################################
# a function that will check if the palyer gussed all the letters of the secret word 
  def check_win(secret_word, old_letters_guessed):
    if list_progres_line.count('_') == 0:
      print('true you won')
    else:
      print('keep going')  
  # activating the function
  check_win(secret_word, old_letters_guessed)
  #################################################################################################
  # a function that will present the hangman drawing progress until it's fully hanged
  def print_hangman(num_of_tries):
    #a list of hangman elements from it we will draw the hangman
    hangman_process = [['|' , '|' , '|' , '|'  , '|'] , ['x'] , ['-' ,  '-' , '-' , '-' , '-' , '-' , '-'] 
  , ['x'] , ['|'] , [' 0' , '/|\\' , '/ \\'] ] 
    # showing how much tries left
    print('the numbers of tries left: ' , MAX_TRIES - len(old_letters_guessed))
    #a condition that will check if u won or lost if u got to the 6 chance
    if list_progres_line.count('_') != 0:
    #Conditions that every attempt the code will draw another part of the hangman
        if len(old_letters_guessed) == 1 :
            for i in range(len(hangman_process[0])):
                print(hangman_process[0][i])
        elif len(old_letters_guessed) == 2 :
             print(''.join(hangman_process[1])) 
             for i in range(len(hangman_process[0])):
                print(hangman_process[0][i])
        elif len(old_letters_guessed) == 3 : 
             print(''.join(hangman_process[1]) + ''.join(hangman_process[2]) )
             for i in range(len(hangman_process[0])):
                 print(hangman_process[0][i])  
        elif len(old_letters_guessed) == 4 :
             print(''.join(hangman_process[1]) + ''.join(hangman_process[2]) + ''.join(hangman_process[3]) )
             for i in range(len(hangman_process[0])):
                 print(hangman_process[0][i])
        elif len(old_letters_guessed) == 5 :
             print(''.join(hangman_process[1]) + ''.join(hangman_process[2]) + ''.join(hangman_process[3]) )
             print((hangman_process[0][0]) , ('\t' + ''.join(hangman_process[4]) ))
             for i in range(len(hangman_process[0]) - 1):
                 print(hangman_process[0][i])
        elif len(old_letters_guessed) == 6 :
             print(''.join(hangman_process[1]) + ''.join(hangman_process[2]) + ''.join(hangman_process[3]) )
             print((hangman_process[0][0]) , ('\t' + ''.join(hangman_process[4]) ))
             for i in range(len(hangman_process[0]) - 2):
                 print(hangman_process[0][i] + (' ' * (len(hangman_process[2]) -1))  + hangman_process[-1][i])
             for i in range(len(hangman_process[0]) - 4):
                print(hangman_process[0][i])
             if len(old_letters_guessed) == MAX_TRIES:          
                print('game lost the secret word was:' , secret_word) 
        elif len(old_letters_guessed) == 7 :
             print(''.join(hangman_process[1]) + ''.join(hangman_process[2]) + ''.join(hangman_process[3]) )
             print((hangman_process[0][0]) , ('\t' + ''.join(hangman_process[4]) ))
             for i in range(len(hangman_process[0]) - 2):
                 print(hangman_process[0][i] + (' ' * (len(hangman_process[2]) -1))  + hangman_process[-1][i])
             for i in range(len(hangman_process[0]) - 4):
                print(hangman_process[0][i])
             if len(old_letters_guessed) == MAX_TRIES:          
                print('game lost the secret word was:' , secret_word) 
        elif len(old_letters_guessed) == 8 :
             print(''.join(hangman_process[1]) + ''.join(hangman_process[2]) + ''.join(hangman_process[3]) )
             print((hangman_process[0][0]) , ('\t' + ''.join(hangman_process[4]) ))
             for i in range(len(hangman_process[0]) - 2):
                 print(hangman_process[0][i] + (' ' * (len(hangman_process[2]) -1))  + hangman_process[-1][i])
             for i in range(len(hangman_process[0]) - 4):
                print(hangman_process[0][i])
             if len(old_letters_guessed) == MAX_TRIES:          
                print('game lost the secret word was:' , secret_word)
        elif len(old_letters_guessed) == 9 :
             print(''.join(hangman_process[1]) + ''.join(hangman_process[2]) + ''.join(hangman_process[3]) )
             print((hangman_process[0][0]) , ('\t' + ''.join(hangman_process[4]) ))
             for i in range(len(hangman_process[0]) - 2):
                 print(hangman_process[0][i] + (' ' * (len(hangman_process[2]) -1))  + hangman_process[-1][i])
             for i in range(len(hangman_process[0]) - 4):
                print(hangman_process[0][i])
             if len(old_letters_guessed) == MAX_TRIES:          
                print('game lost the secret word was:' , secret_word)
                                                                                          
    
    else:
        print('game won the secret word is:' , secret_word)              
  # activating the function          
  print_hangman(MAX_TRIES) 
  