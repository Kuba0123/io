from tkinter import *
from tkinter import messagebox


class Login:
    def __init__(self, root):
        self.root = root
        self.root.title('Login')
        self.root.geometry('400x300')
        self.root.configure(bg="white")
        self.root.resizable(False, False)

        self.frame = Frame(root, width=300, height=250, bg="white")
        self.frame.place(x=55, y=25)
        heading = Label(self.frame, text='LOGIN', fg='#717F8A', bg='white',
                        font=('Microsoft YaHei UI Light', 18, 'bold'))
        heading.place(x=100, y=10)

        self.username = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                              font=('Microsoft YaHei UI Light', 9))
        self.username.place(x=55, y=80)
        self.username.insert(0, 'Nazwa użytkownika')

        self.password = Entry(self.frame, width=25, fg='black', border=1, bg='white',
                              font=('Microsoft YaHei UI Light', 9))
        self.password.place(x=55, y=120)
        self.password.insert(0, 'Hasło')

        self.button = Button(self.frame, width=20, pady=10, text='Zaloguj się', bg='#717F8A', fg='white', border=1,
                             command=self.signIn)
        self.button.place(x=70, y=170)
        self.username.bind('<FocusIn>', self.onEnterUser)
        self.password.bind('<FocusIn>', self.onEnterPassw)

    def signIn(self):
        self.user = self.username.get()
        self.passw = self.password.get()

        if self.user == 'admin' and self.passw == 'admin':
            print('Poprawnie')

        else:
            messagebox.showerror('Błąd!', 'Nieprawidłowy login lub hasło')

    def onEnterUser(self, e):
        self.username.delete(0, 'end')

    def onEnterPassw(self, e):
        self.password.delete(0, 'end')


if __name__ == "__main__":
    root = Tk()
    login = Login(root)
    root.mainloop()
