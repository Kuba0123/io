from tkinter import *
from tkinter import messagebox


class Login:
    def loginForm(self):
        root = Tk()
        root.title('Login')
        root.geometry('400x300')
        root.configure(bg="white")
        root.resizable(False, False)

        def signin():
            username = user.get()
            passw = password.get()

            if username == 'admin' and passw == 'admin':
                print('poprawne')

            else:
                messagebox.showerror('Błąd w logowaniu', 'Nieprawidłowy login lub hasło')

        frame = Frame(root, width=300, height=250, bg="white")
        frame.place(x=55, y=25)
        heading = Label(frame, text='LOGIN', fg='#717F8A', bg='white', font=('Microsoft YaHei UI Light', 18, 'bold'))
        heading.place(x=100, y=10)

        # username
        def on_enter(e):
            user.delete(0, 'end')

        def on_leave(e):
            name = user.get()
            if name == '':
                user.insert(0, 'Nazwa użytkownika')

        user = Entry(frame, width=25, fg='black', border=1, bg='white', font=('Microsoft YaHei UI Light', 9))
        user.place(x=55, y=80)
        user.insert(0, 'Nazwa użytkownika')
        user.bind('<FocusIn>', on_enter)
        user.bind('<FocusOut>', on_leave)

        # password
        def on_enter(e):
            password.delete(0, 'end')

        def on_leave(e):
            name = password.get()
            if name == '':
                password.insert(0, 'Hasło')

        password = Entry(frame, width=25, fg='black', border=1, bg='white', font=('Microsoft YaHei UI Light', 9))
        password.place(x=55, y=120)
        password.insert(0, 'Hasło')
        password.bind('<FocusIn>', on_enter)
        password.bind('<FocusOut>', on_leave)

        # button
        button = Button(frame, width=20, pady=10, text='Zaloguj się', bg='#717F8A', fg='white', border=1,
                        command=signin)
        button.place(x=70, y=170)
        label = Label(frame, text="")

        root.mainloop()

login = Login()
login.loginForm()