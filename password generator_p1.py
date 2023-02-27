######The code is a Python script that generates passwords and inserts them into an SQL Server database.
######It uses the tkinter library to create a GUI and allows the user to select between two options for
######password generation: 1) manual input of a password and its corresponding application and username,
######or 2) automatic generation of a password with a specified length. The passwords are encrypted using
######the cryptography.fernet library before being inserted into the database. The program also verifies for
######duplicates before inserting the password. also the progrem encryptes the encryption keys with a master
######key that is stored in the envirment variables in the computer and stores them in a encrypted kyts file

####section 1 importing relevent modules and libraries
#importing a graphic library for crearing a user interface
import tkinter as tk
from tkinter import *
#importing a library that helps reading picturs
from PIL import ImageTk,Image
#impoting messagebox
from tkinter import messagebox
#creating a random password generator
#importing connection library between sql server to python
import pyodbc
#importing the random libery to choose for me random passwords
import secrets
#importing all the alphabet letters low and upper cases
import string
#importing the encyption library for encrypting the passwords
from cryptography.fernet import Fernet  
#############################################################################
####section 2
####in this section i will make first connect to sql server and will create the base 
####for the creation of the random password with secerts module and also creating  
####the key for encryption and decryption later on

# Connect to the SQL Server
sql_connect= pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-22FR3H2\SQLEXPRESS;"
    "DATABASE=pws_project;")

#craeting elements that will contain all the letters numbers and punctuations
all_charactes= string.ascii_letters + string.digits + string.punctuation
upper = string.ascii_uppercase
lower = string.ascii_lowercase
digits = string.digits
special_characters = string.punctuation

#creting the key for encrypting and decrypting the passwords
#You can use fernet to generate
# the key or use random key generator
# here I'm using fernet to generate key
global key
key= Fernet.generate_key()
#making the key to a global element
#making the Fernet as operational object
global fernet
fernet = Fernet(key)
#############################################################################
####section 3
####in this section i create the window page and everything in it as well as 
####taking all the inserted objects from the selected entries and encrypting 
####the passwords 

#creating the interface
root = Tk()
#rewriting the title of the page
root.title('password generator')
#replacing the page logo
root.iconbitmap('C:/Users/user/Desktop/icons/ironman_logo.ico')
#the page size
root.geometry('700x400')

#creating an exit button for the window page
exit_button = Button(root, text='exit', bd=1, command=root.quit)
exit_button.grid(row=2, column=0, pady=10, padx=10)

#stores the number of the chosen radionumber for later
Radiobutton_number = IntVar()

# defining variables 
password_length_entry = None
password_entry = None
application_name = None
username = None


#a function that will dispaly on the page the wanted entries to coninue the process
def Radiobutton_clcked(value):
    #making all the objects globals so that i will be able to use them later on
    global password_length_entry
    global password_entry
    global application_name
    global username
    #condition that if the user will choose 1 the second entries will be deleted and 
    #only the the first button entries will be shown and the way back as well
    if value == 1:
        # Remove entries for button 2
        #and previos button 1
        if password_entry is not None:
            password_entry.grid_forget()
        if password_length_entry is not None:
            password_length_entry.grid_forget()
        if application_name is not None:
            application_name.grid_forget()
        if username is not None:
            username.grid_forget()    

        # Create entries for button 1
        password_entry = Entry(root)
        password_entry.grid(row=0, column=2, padx=10)
        application_name = Entry(root)
        application_name.grid(row=0, column=3, padx=10)
        username = Entry(root)
        username.grid(row=0, column=4, padx=10)   
        
    elif value == 2:
        # Remove entries for button 1
        #and previos button 2
        if password_length_entry is not None:
            password_length_entry.grid_forget()
        if application_name is not None:
            application_name.grid_forget()
        if username is not None:
            username.grid_forget()
        if password_entry is not None:
            password_entry.grid_forget()
             
        # Create entries for button 2
        password_length_entry = Entry(root)
        password_length_entry.grid(row=1, column=2, padx=10)
        application_name = Entry(root)
        application_name.grid(row=1, column=3, padx=10)
        username = Entry(root)
        username.grid(row=1, column=4, padx=10)
        
#a function that will run until the page is closed and whithin it will be the 
#encryption, the duplicate verification and insertion of all objects to ssms
def enter_generator():
    #making all the objects globals so that i will be able to use them later on    
    global password_value
    global application_name
    global username
    global password_length_entry
    #creating a message box that will make sure the user wants to submit his info
    response = messagebox.askyesno('this is my popup', 'hello world!')
    #depends on the user choise on the messagebox (yes=1, no=0)
    #if he decides to click yes(1) the program will continue
    if response == 1:
        #this condition will check which way the user chose to go through
        #if he chose way number 1 (radiobutton 1) first all the info will be printed
        #then he takes the value of the password encryptes it and making it a global var
        if Radiobutton_number.get() == 1:
            password_value = password_entry.get()
            print('the password is: ', password_value)
            app_name = application_name.get()
            print('the wanted password length is: ', password_length_entry)
            user_name = username.get()
            print('the username is: ', user_name)

            #incrypting the password and globalizing it            
            initial_password = password_value
            global encrypted_password
            encrypted_password = fernet.encrypt(initial_password.encode())
            print('the password is: ' , initial_password, '\nthe encrypted password is: ', str(encrypted_password))
        
        #second way/button within it the same process as the previos one but the
        #password will be change to a length wnd a random password using secrets
        #will be created and then it will get encrypted
        elif Radiobutton_number.get() == 2:
            #passing the value from entery to object because tou cant change entry value to int 
            password_length = password_length_entry.get()
            #making sure the length is digits only 
            if password_length.isdigit():
                wanted_length = int(password_length)
            print('the wanted password length is: ', wanted_length)
            app_name = application_name.get()
            print('the application name is: ', app_name)
            user_name = username.get()
            print('the username is: ', user_name)
            
            #the minimum length is 8 char so if it less the diffult is 8, also
            #the random passworrd will ne build like that: first char is upper letter,
            #the last char will be special char and between will be a mix of numbers
            #and lower letters
            if wanted_length < 8:
               wanted_length = 8
            password= secrets.choice(upper) + ''.join(secrets.choice(lower + digits) for i in range(wanted_length - 2)) + secrets.choice(special_characters)
            # to encrypt the string must be encoded to bytes before encryption,
            #changing the encrypted password to global element
            encrypted_password = fernet.encrypt(password.encode())
            print('the password is: ' , password, '\nthe encrypted password is: ', str(encrypted_password))
    
#######################################################################################
    ####section 4
    ####this section is for eliminate duplicates and is there is none then adding a 
    ####uniqe ID and inserting them into ssms, the connection to sql was applied 
    ####on the second section of the script

    #building a list to check and will not uplaod a password that already have
    #the same username and application namein the ssms
    password_info = [app_name, user_name]

    #connecting to sql server
    cursor = sql_connect.cursor()

    #reaching to sql server and getting to a list all the applications names and usernams to avoid from duplicates
    sql=cursor.execute(f'SELECT Application, Username FROM [pws_project].[dbo].[passwords] '  )
    sql_server_results = []
    for row in sql:
        sql_server_results.append(list(row))

    #checking for duplicates
    count_duplicates = 0
    for i in sql_server_results:
        if i == password_info:
            count_duplicates += 1
    if count_duplicates > 0:
        duplicate_error = messagebox.showerror('duplicate eror', 'there is already a password on that appliction and username')
    else:
        print('ok')
        #creating an ID to the password by counting the row in the database , making it a list and then a int
        row_count = []
        #checking the number of rows
        id_create=cursor.execute(f'SELECT count(*) FROM [pws_project].[dbo].[passwords] ')
        for row in id_create:
            row_count.append(list(row))
        ID=int(''.join(map(str, row_count[0])))     
        # Insert the data into the table
        cursor.execute('INSERT INTO [pws_project].[dbo].[passwords] VALUES (?, ?, ?, ?)',(app_name, encrypted_password, user_name, ID))

###################################################################################################
    #section5
    ####this section will upload the keys in encripted form to a txt file,
    ####the encryption of the keys will be done by master key that i stored in the 
    ####environment variabl in the computer while taking use of it to encrypt the keys
    ####and also will finish ceating the buttons of the radiobutton and the enter
    ####function as well to extra buttons and labels hat are in the window and closing 
    ####the loop when the user finish and closes the window

    #this module helps me to take the masterkey from deep in the computer where istore it in the 'environment variable'
    import os
    #creating the same condition from before, if the application name and usename allready taken it will not uplaod
    # the encrypted key to the encrypted keys file  
    if count_duplicates == 0:
        #taking the master key from the 'environment variable'
        demo_master_key = os.environ.get('demo_master_key') 
        #changing the master key from a string to bytes
        bytes_master_key= demo_master_key.encode()
        #creating new fernet for the master key
        master_fernet = Fernet(bytes_master_key) 

        #encrypting the keys
        encrypted_key= master_fernet.encrypt(key)
        str_encrypted_key= encrypted_key.decode()

        #openning the keys file to append the encrypted key to the file
        with open('keykey.txt', 'a') as key_file:
            key_file.write(str_encrypted_key)
            key_file.write('\n')

#creating and displaying the radiobuttons    
password_choise1 = Radiobutton(root,  variable=Radiobutton_number, value=1, command=lambda:Radiobutton_clcked(Radiobutton_number.get()))
password_choise2 = Radiobutton(root, variable=Radiobutton_number, value=2,command=lambda:Radiobutton_clcked(Radiobutton_number.get()))
password_choise1.grid(row=0, column=0)
password_choise2.grid(row=1, column=0)
radio_label1 = Label(root, text='proceed with a password creation')
radio_label2 = Label(root, text='proceed with no password creation')
radio_label1.grid(row=0, column=1)
radio_label2.grid(row=1, column=1)
#creating and displaying extra buttons
exit_button = Button(root, text='exit', bd=1, command=root.quit)
exit_button.grid(row=2, column=0, pady=10, padx=10)
submit_button = Button(root, text='submit', bd=1, command=enter_generator)
submit_button.grid(row=2, column=1, pady=10, padx=10, ipadx=100, columnspan=2)

#esecuting the page
root.mainloop()
# Commit the changes
sql_connect.commit()

# Close the connection
sql_connect.close()



