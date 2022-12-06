from tkinter import *
from tkinter import messagebox
import hashlib
import os.path
from os import path


class LoginForm:
    def __init__(self, rootLogin):
        self.rootLogin = rootLogin
        self.rootLogin.title('Login')
        self.rootLogin.geometry('400x300')
        self.rootLogin.configure(bg="white")
        self.rootLogin.resizable(False, False)

        self.frame = Frame(rootLogin, width=400, height=300, bg="white")
        self.frame.place(x=0, y=0)
        heading = Label(self.frame, text='LOGIN', fg='#717F8A', bg='white',
                        font=('Microsoft YaHei UI Light', 18, 'bold'))
        heading.place(x=155, y=10)

        usernamelabel = Label(self.frame, text='Username:', fg='black', bg='white',
                              font=('Microsoft YaHei UI Light', 9))
        usernamelabel.place(x=45, y=80)

        passwordlabel = Label(self.frame, text='Password:', fg='black', bg='white',
                              font=('Microsoft YaHei UI Light', 9))
        passwordlabel.place(x=50, y=120)

        self.username = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                              font=('Microsoft YaHei UI Light', 9))
        self.username.place(x=110, y=80)

        self.password = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                              font=('Microsoft YaHei UI Light', 9), show='*')
        self.password.place(x=110, y=120)

        self.buttonLogin = Button(self.frame, width=20, pady=10, text='Log In', bg='#717F8A', fg='white', border=1,
                                  command=self.LogIn)
        self.buttonLogin.place(x=125, y=170)

        self.buttonRegister = Button(text='Don\'t have an account yet? Click here', borderwidth=0, bg='white',
                                     command=self.Register)
        self.buttonRegister.place(x=95, y=240)

    def Register(self):
        self.Register = Tk()
        self.Register.title('Register')
        self.Register.geometry('400x300')
        self.Register.resizable(False, False)
        self.Register.configure(bg="white")
        self.frame = Frame(self.Register, width=400, height=300, bg="white")
        self.frame.place(x=0, y=0)

        headingregister = Label(self.frame, text='REGISTER', fg='#717F8A', bg='white',
                                font=('Microsoft YaHei UI Light', 18, 'bold'))
        headingregister.place(x=135, y=0)

        usernamereglabel = Label(self.frame, text='Username:', fg='black', bg='white',
                                 font=('Microsoft YaHei UI Light', 9))
        usernamereglabel.place(x=45, y=70)

        passwordlabel = Label(self.frame, text='Password:', fg='black', bg='white',
                              font=('Microsoft YaHei UI Light', 9))
        passwordlabel.place(x=50, y=120)

        confpasswordlabel = Label(self.frame, text='Confirm\npassword:', fg='black', bg='white',
                                  font=('Microsoft YaHei UI Light', 9))
        confpasswordlabel.place(x=50, y=153)

        self.usernameReg = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                                 font=('Microsoft YaHei UI Light', 9))
        self.usernameReg.place(x=110, y=70)

        self.passwordReg = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                                 font=('Microsoft YaHei UI Light', 9), show='*')
        self.passwordReg.place(x=110, y=120)

        self.confirmPasswordReg = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                                        font=('Microsoft YaHei UI Light', 9), show='*')
        self.confirmPasswordReg.place(x=110, y=170)

        self.buttonSingup = Button(self.frame, width=20, pady=10, text='Sign Up', bg='#717F8A', fg='white', border=1,
                                   command=self.SignUp)
        self.buttonSingup.place(x=125, y=220)

    def SignUp(self):
        i = 1
        with open('login.txt', 'r') as f:
            content = f.read()

            if self.usernameReg.get() not in content:
                if len(self.usernameReg.get()) > 3:
                    if self.passwordReg.get() == self.confirmPasswordReg.get():
                        if len(self.passwordReg.get()) > 5:
                            with open('login.txt', 'a') as f:
                                f.write(self.usernameReg.get() + ':' + hashlib.sha256(
                                    self.passwordReg.get().encode('utf-8')).hexdigest() + ':')

                                while path.isfile(str(i) + '.json'):  # Tworzenie pliku .json
                                    i += 1

                                name = str(i) + '.json'
                                with open(name, 'w') as file:
                                    file.write('[]')
                                    f.write(name + '\n')

                        else:
                            messagebox.showerror('Error', 'Password must have at least 6 characters!')
                    else:
                        messagebox.showerror('Error', 'Passwords do not match!')
                else:
                    messagebox.showerror('Error', 'Username must have at least 4 characters!')
            else:
                messagebox.showerror('Error', 'Username already exists!')

    def LogIn(self):
        with open('login.txt', 'r') as f:
            content = f.read()

            if self.username.get() in content:
                passw = int(content.find(self.username.get())) + int(len(self.username.get())) + 1
                hash = content[passw:passw + 64]

                if hash == hashlib.sha256(self.password.get().encode('utf-8')).hexdigest():
                    print('DZIAłAAAA!!!!!!!!!!!!!!!!!')

                else:
                    messagebox.showerror('Error', 'Invalid username or password!')
            else:
                messagebox.showerror('Error', 'Invalid username or password!')


if __name__ == "__main__":
    root = Tk()
    loginForm = LoginForm(root)
    root.mainloop()
