####a second script for the password generator project that reverse the process,
####first on GUI user interface using tkinter the user inserts the entries 
####the application name and username. then the script connects to sql server
####and makes sure that it exists, afterwords its finds the info ID which 
####represent the password row number in the table and its encryption key 
####in the encrypted keys file, then using master key its starts decrypting 
####first the encrypted key and then the encrypted password and showing the 
####result on the window GUI 

####section 1 importing relevent modules and libraries
#importing a graphic library for crearing a user interface
import tkinter as tk
from tkinter import *
#importing a library that helps reading picturs
from PIL import ImageTk,Image
#impoting messagebox
from tkinter import messagebox
#importing a library that can encrypt and decrypt keys
from cryptography.fernet import Fernet
#importing a module that can draw the master key fron envirment varibales
import os
#importing a module that connects us to sql server where all the password are 
import pyodbc
##############################################################################
####section 2

#retriving the master key from the computer
demo_master_key = os.environ.get('demo_master_key')
#chaging the str form master key to bytes form for using to decrypt encryptions
bytes_master_key= demo_master_key.encode()
print('the master key is: ', bytes_master_key)
######################################################################################################
####section 3

# creating first connection with sql server
# and finding the wanted password     
## Connect to the SQL Server
sql_connect= pyodbc.connect(
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-22FR3H2\SQLEXPRESS;"
    "DATABASE=pws_project;")

#############################################################################
####section 4 creating the window, giving the user to fill up the application 
####name and the username and reatriving the password to the page, also making sure 
####the password exists if not giving an eror message, buliding a clear button 
####will clear the entries and the result  

#creating the interface
root = Tk()
#rewriting the title of the page
root.title('getting password info')
#replacing the page logo
root.iconbitmap('C:/Users/user/Desktop/icons/ironman_logo.ico')
#the page size
root.geometry('700x400')

#a function that will transfer the user info to a list and will compare it to 
#a list of all the dues in the db until it will find it and its place in the db list,
#then will get the right encrypted key from the key file(the place as the password
#info in the db list), and wll decrypt the key, then it will take the encrypted
#password and will decrypt it so it could print it on the window page
def get_query():
    info_lst = [app_name.get(), username.get()]
    print(info_lst)
    #crearing the connection operation on the sql_connnect info
    cursor = sql_connect.cursor()    
    sql_info = cursor.execute(f'select Application, Username from [pws_project].[dbo].[passwords] order by ID')
    password_info=[]
    #two loops that will append all the info in a pyodbc to the password_info list
    for row in sql_info:
        password_info.append(row)
    password_info = [list(row) for row in password_info]
    count = 0
    for row in password_info:
        if row == info_lst:
            count +=1
    #condition to decide if the wanted password is in the sql database
    #if not an errormessage will appear if its exists it will extract him        
    if count != 1:
        errormessage = messagebox.showerror('error', 'the wanted password was not found')  
    else:
        #finding the palce of the info in the password info list as ID
        ID = password_info.index(info_lst)
        #finding the password according the ID firt in bytes in a list
        password_enc=cursor.execute(f'select Encrypted_password from [pws_project].[dbo].[passwords] where ID = ?', ID)
        password_lst=[]
        for row in password_enc:
            password_lst.append(row)
        #breaking the list as str (removing the bytes)
        str_password= ''.join(map(str, password_lst[0]))
        #adding the bytes to the encrypted password for decryption
        bytes_password= str_password.encode()
        #openning the keys file to read the encrypted key from the file
        with open('keykey.txt', 'r') as key_file:
            lines = key_file.readlines()   
        #changing the form of the encrypted key from str to bytes for decryption
        bytes_encrypted_key=lines[ID].encode().rstrip()
        #creating cryptogrphy opration tool for decryption
        fernet= Fernet(bytes_master_key)
        #dercyting the encrypted key
        low_key= fernet.decrypt(bytes_encrypted_key)
        #changing the cryptogrphy operation from the masterkey to the low key
        fernet=Fernet(low_key)
        #dercyting the encrypted password
        decrypt_password= fernet.decrypt(bytes_password)
        global pass_label
        #printing the password in the window
        pass_label = Label(root, text=('the password is: ' + decrypt_password.decode())) 
        pass_label.grid(row=3, column=0, columnspan=2)
#a function that opearates with the clicked button 'clear' and clears all the 
#entries and the password output
def restart():
    app_name.delete(0, END)
    username.delete(0, END)
    pass_label.grid_forget()
    
#creating the inital entries and labels for the window
app_name= Entry(root, width=30)
app_name.grid(row=0, column=1, padx=20)
username = Entry(root, width=30)
username.grid(row=1, column=1, padx=20)

app_label = Label(root, text='application name')
app_label.grid(row=0, column=0)
username_label = Label(root, text='username')
username_label.grid(row=1, column=0)

query_button = Button(root, text='show records', command=get_query)
query_button.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=100)
clear_button = Button(root, text='reset', command=restart)
clear_button.grid(row=2, column=3, columnspan=2, pady=10, padx=10, ipadx=10)

#closing the window loop when the user closes the window
root.mainloop()