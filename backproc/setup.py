import tkinter
import requests
import firebase_admin
from firebase_admin.credentials import Certificate
from firebase_admin.firestore import client
import os
import jsonapis
import time

credentials = Certificate('json/firebase.json')
app = firebase_admin.initialize_app(credentials, name='GDLive')
database = client(app)

def create_account(username: str, password: str, email: str):
    if not database.collection('Accounts').document(email).get().to_dict() == None:
        raise_error_screen('Invalid email', 'This email is already in use')
    else:
        if not database.collection('Users').document(username).get().to_dict() == None:
            raise_error_screen('Invalid Username', 'This username is already in use try again')
        else:
            document = {'username': username, 'password': password}
            database.collection('Accounts').document(email).set(document)
            document = {'joined_collabs': [], 'requested_collabs': []}
            database.collection('Users').document(username).set(document)
            switch(2)

def login_account(email: str, password: str):
    account_json = database.collection('Accounts').document(email).get().to_dict()
    if account_json == None:
        raise_error_screen('Invalid Email', 'email does not exist')
    else:
        if account_json['password'] == password:
            jsonapis.edit_json_file('json/user-settings.json', 'username', account_json['username'])
            jsonapis.edit_json_file('json/user-settings.json', 'password', password)
            switch(3)
        else:
            raise_error_screen('Invalid password', 'Password is incorrect')

def check_internet_connection() -> bool:
    try:
        requests.get('https://google.com')
        return True
    except requests.ConnectionError:
        return False

def raise_error_screen(error: str, description: str):
    errwin = tkinter.Tk()
    errwin.title('There has been an error')
    errwin.geometry('300x100')
    
    tkinter.Label(errwin, text=error, font=1).place(anchor='center', relx=0.5, rely=0.13)
    tkinter.Label(errwin, text=description).place(anchor='center', relx=0.5, rely=0.5)
    
    errwin.mainloop()

__window: None

def switch(page: int):
    __window.destroy()
    main(page)

def main(page: int):
    global __window
    window = tkinter.Tk()
    window.title('Install GDLive')
    window.geometry('400x200')
    window.wm_maxsize(400, 200)
    __window = window
    
    if page == 0:
        tkinter.Label(window, text='GDLive License and EULA', font=1).place(anchor='w', x=20, y=20)
        tkinter.Label(window, text='By continuing with the installation you as the end user agree to').place(anchor='w', x=20, y=50)
        tkinter.Label(window, text='the License, security policy and the EULA.').place(anchor='w', x=20, y=70)
        tkinter.Label(window, text='Click on any of the buttons below to view any of the documents').place(anchor='w', x=20, y=100)
        
        tkinter.Button(window, text='View License (./License.txt)', width=20, command=lambda: os.system('notepad "License.txt"')).place(anchor='w', x=20, y=130)
        tkinter.Button(window, text='View EULA (./EULA.rst)', width=20, command=lambda: os.system('notepad "EULA.rst"')).place(anchor='w', x=20, y=150)
        tkinter.Button(window, text='View Readme (./security.md)', width=20, command=lambda: os.system('notepad "security.md"')).place(anchor='w', x=20, y=170)
        
        tkinter.Button(window, text='Continue', command=lambda: switch(1)).place(anchor='w', x=270, y=170)
    
    elif page == 1:
        tkinter.Label(window, text='Create your GDLive account', font=1).place(anchor='w', x=20, y=20)
        tkinter.Label(window, text='Enter your email').place(anchor='w', x=20, y=50)
        email = tkinter.Entry(window, width=26); email.place(anchor='w', x=20, y=70)
        tkinter.Label(window, text='Enter your username').place(anchor='w', x=20, y=100)
        username = tkinter.Entry(window, width=26); username.place(anchor='w', x=20, y=120)
        tkinter.Label(window, text='Enter your password').place(anchor='w', x=20, y=150)
        password = tkinter.Entry(window, width=26); password.place(anchor='w', x=20, y=170)
        
        tkinter.Button(window, text='Create Account', command=lambda: create_account(username.get(), password.get(), email.get())).place(anchor='w', x=200, y=130)
        tkinter.Button(window, text='Already have an account (Skip)', command=lambda: switch(2)).place(anchor='w', x=200, y=170)
    
    elif page == 2:
        tkinter.Label(window, text='Sign into your Account', font=1).place(anchor='w', x=20, y=20)
        tkinter.Label(window, text='Enter your email').place(anchor='w', x=20, y=50)
        email = tkinter.Entry(window, width=26); email.place(anchor='w', x=20, y=70)
        tkinter.Label(window, text='Enter your password').place(anchor='w', x=20, y=100)
        password = tkinter.Entry(window, width=26); password.place(anchor='w', x=20, y=120)
        
        tkinter.Button(window, text='Sign In', command=lambda: login_account(email.get(), password.get())).place(anchor='w', x=20, y=170)
    
    elif page == 3:
        tkinter.Label(window, text='Sucsessfuly signed into your account', font=1).place(anchor='w', x=20, y=20)
        tkinter.Label(window, text='You can now exit this page and continue with GDLive').place(anchor='w', x=20, y=50)
        tkinter.Button(window, text='Close Window', command=lambda: exit(0)).place(anchor='w', x=20, y=170)
    
    window.mainloop()

if __name__ == '__main__':
    if check_internet_connection() == True:
        main(0)
    else:
        raise_error_screen('No Internet Connection', 'You are not connected to the internet or\nany local network')