import os
import threading
import pygame
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox
from functools import partial
import json
from os import path
import hashlib

pygame.font.init()

LENGTH = 200
WIN_WIDTH = 8.5 * LENGTH
WIN_HEIGHT = 4.5 * LENGTH

FONT1 = pygame.font.SysFont('comicsans', 20)
FONT2 = pygame.font.SysFont('comicsans', 35)


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
                    root.destroy()

                    WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
                    game = Game(WIN)
                    game.loadFromJSON()
                    game.main()

                else:
                    messagebox.showerror('Error', 'Invalid username or password!')
            else:
                messagebox.showerror('Error', 'Invalid username or password!')


class InfoWindow:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def draw(self, win):
        pass


class ButtonLogOut:
    def __init__(self) -> None:
        self.text = FONT2.render("Log Out", 1, (0, 0, 0))
        self.x = int(WIN_WIDTH - self.text.get_width() - 20)
        self.y = int(WIN_HEIGHT - self.text.get_height() - 10)
        self.height = int(self.text.get_width())
        self.width = int(self.text.get_width())
        self.isclicked = False

    def draw(self, win):
        x, y = pygame.mouse.get_pos()
        if x in range(self.x, self.x + self.width) and y in range(self.y, self.y + self.height):
            self.text = FONT2.render("Log Out", 1, (200, 200, 200))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] == 1:
                print("Wylogowano")
                self.isclicked = True

        else:
            self.text = FONT2.render("Log Out", 1, (0, 0, 0))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            self.isclicked = False

        win.blit(self.text, (self.x, self.y))


logout = ButtonLogOut()


# tworzy listę rozwijaną osoby
class PersonList:
    def __init__(self, x, y, buttons) -> None:
        self.x = x
        self.y = y
        self.buttons = buttons
        self.width = 300
        self.height = len(buttons) * 50
        self.color = (240, 240, 240)
        self.isclicked = False

    def draw(self, win):
        x, y = pygame.mouse.get_pos()
        if x in range(self.x, self.x + self.width) and y in range(self.y, self.y + self.height):
            if pygame.mouse.get_pressed()[0] == 1:
                self.isclicked = True

            if pygame.mouse.get_pressed()[2] == 1:
                self.isclicked = False

        # sprawia że wyświetlana lista jest w oknie programu
        for button in self.buttons:
            if self.x > WIN_WIDTH - self.width:
                button.x = button.x - self.width
            if self.y > WIN_HEIGHT - self.height:
                button.y = button.y - self.height
            button.draw(win)
        if self.x > WIN_WIDTH - self.width:
            self.x = self.x - self.width
        if self.y > WIN_HEIGHT - self.height:
            self.y = self.y - self.height


def do_nothing():
    pass


# klasa przycisk
class ButtonList:
    def __init__(self, x, y, text="", command=do_nothing, command2=do_nothing) -> None:
        self.x = x
        self.y = y
        self.command = command
        self.command2 = command2
        self.text = FONT1.render(str(text), 1, (0, 0, 0))
        self.width = 300
        self.height = 50
        self.costume = 0
        self.colors = [(240, 240, 240), (200, 200, 200)]
        self.isclicked = False
        self.time = 0

    def draw(self, win):

        x, y = pygame.mouse.get_pos()
        if x in range(self.x, self.x + self.width) and y in range(self.y, self.y + self.height):
            self.costume = 1
            self.time += 1
            if pygame.mouse.get_pressed()[0] == 1:
                self.isclicked = True
                self.command()
            elif pygame.mouse.get_pressed()[2] == 1:
                self.isclicked = False

            if self.time > 20:
                self.command2()
        else:
            self.costume = 0
            self.time = 0

        pygame.draw.rect(win, self.colors[self.costume], (self.x, self.y, self.width, self.height))
        win.blit(self.text, ((2 * self.x + self.width) // 2 - (self.text.get_width()) // 2,
                             (2 * self.y + self.height) // 2 - (self.text.get_height()) // 2))


class Person:
    def __init__(self, id, x=100, y=100, r=80, name="", surname="", bornYear=0, img=[],
                 relations={"parents": [], "childrens": [], "siblings": [], "partner": []},
                 colors=[(7, 56, 99), (107, 56, 99)], costume=0, bool=False, current=False, isclickedR=False,
                 isclickedL=False, time=0) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.r = r
        self.name = name
        self.surname = surname
        self.bornYear = bornYear
        self.img = img
        self.relations = relations
        self.colors = colors
        self.costume = costume
        self.bool = bool
        self.current = current
        self.isclickedR = isclickedR
        self.isclickedL = isclickedL
        # self.partner = None
        self.time = time
        # self.relationsCount = 0

    def draw(self, win):
        x, y = pygame.mouse.get_pos()

        if ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5 <= self.r:
            # pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            # self.costume = 1
            self.time += 1
            if pygame.mouse.get_pressed()[2] == 1:
                self.isclickedR = True
                self.time = 0
            else:
                self.isclickedR = False

            if pygame.mouse.get_pressed()[0] == 1:
                self.isclickedL = True
                self.time = 0

            else:
                self.isclickedL = False
                self.current = False

        else:
            self.current = False
            self.time = 0
            # self.costume = 0

        if self.isclickedL and self.current:
            self.x = x
            self.y = y

        pygame.draw.circle(win, self.colors[self.costume], (self.x, self.y), self.r)  # rysuje osobę
        # for relation in list(self.relations):
        #    pygame.draw.line(win,self.color,(self.x,self.y),(relation.x,relation.y)) #rysuje relacje między osobami
        s = FONT1.render(f"{self.name} {self.surname}", 1, (0, 255, 255))
        win.blit(s, (self.x - s.get_width() // 2,
                     (self.y - s.get_height() // 2) + 1.2 * self.r))  # wyświetla imię, nazwisko i rok urodzenia

        # def toJSON(self,filename):
        #    with open(filename, 'w') as file:
        #        file.write(json.dumps(self.__dict__,indent=2))
        # return json.dumps(self,default=lambda o: o.__dict__,sort_keys=True,indent=4)

        """ 
        if self.time > 250:
            x,y = pygame.mouse.get_pos()
            pygame.draw.rect(win,(30,100,200),(x,y,4*self.r,2*self.r))
            text = FONT1.render(f"{self.name} {self.surname} {self.bornYear}", 1, (255,255,255))
            win.blit(text,(x + 2*self.r-text.get_width()//2,y + self.r-text.get_height()//2)) 
       """


class Game:
    def __init__(self, win) -> None:
        self.curId = 0
        self.win = win
        self.persons = {}
        self.form = False
        self.currentPerson = None
        self.lastCurrentPerson = None
        self.relationPerson = None
        self.personList = None
        self.list2 = None
        self.newRelation = 0

        # self.relationCount = 0
        self.lx = 0
        self.ly = 0

    def forma(self):
        # x,y = pygame.mouse.get_pos()
        root = Tk()
        root.geometry("500x500")
        firstname_text = Label(text="Firstname ", )
        firstname_text.place(x=15, y=30)
        firstname = StringVar()
        firstname_entry = Entry(textvariable=firstname, width="30")
        firstname_entry.place(x=80, y=30)

        surnname_text = Label(text="Surnname  ", )
        surnname_text.place(x=15, y=60)
        surnname = StringVar()
        surnname_entry = Entry(textvariable=surnname, width="30")
        surnname_entry.place(x=80, y=60)

        bornyear_text = Label(text="Born Year ", )
        bornyear_text.place(x=15, y=90)
        bornyear = StringVar()
        bornyear_entry = Entry(textvariable=bornyear, width="30")
        bornyear_entry.place(x=80, y=90)

        AddImg = Button(text="Add Picture", width="30", height="2", command=partial(self.addPicture))
        AddImg.place(x=140, y=180)

        save = Button(text="Save", width="30", height="2",
                      command=partial(self.changeInformation, firstname, surnname, bornyear, root))
        save.place(x=140, y=230)

        root.mainloop()

    def edit(self):
        t = threading.Thread(target=self.forma)
        t.start()
        # self.form = True
        self.personList = None

    # uaktualnia dane po edycji w formularzu
    def changeInformation(self, name, surname, bornyear, root):
        self.lastCurrentPerson.name = name.get()
        self.lastCurrentPerson.surname = surname.get()
        self.lastCurrentPerson.bornYear = bornyear.get()
        root.destroy()
        # self.form = False

    def addPerson(self):
        self.edit()
        x, y = pygame.mouse.get_pos()
        self.persons[self.curId] = Person(id=self.curId, x=x, y=y)  # dodaje osobę do listy osób
        self.curId += 1

    def addParent(self):
        self.edit()
        x, y = pygame.mouse.get_pos()
        self.persons[self.curId] = Person(id=self.curId, x=x, y=y)  # dodaje osobę do listy osób
        self.lastCurrentPerson.relations["parents"].append(self.curId)
        self.persons[self.curId].relations["childrens"].append(self.lastCurrentPerson.id)
        self.curId += 1
        # newPerson.relationsCount += 1
        # self.lastCurrentPerson.relationsCount += 1
        # self.relationCount += 2

    def addChild(self):
        self.edit()
        x, y = pygame.mouse.get_pos()
        self.persons[self.curId] = Person(id=self.curId, x=x, y=y)  # dodaje osobę do listy osób
        self.lastCurrentPerson.relations["childrens"].append(self.curId)
        self.persons[self.curId].relations["parents"].append(self.lastCurrentPerson.id)
        self.curId += 1
        # newPerson.relationsCount += 1
        # self.lastCurrentPerson.relationsCount += 1
        # self.relationCount += 2

    def addSibling(self):
        self.edit()
        x, y = pygame.mouse.get_pos()
        self.persons[self.curId] = Person(id=self.curId, x=x, y=y)  # dodaje osobę do listy osób
        self.lastCurrentPerson.relations["siblings"].append(self.curId)
        self.persons[self.curId].relations["siblings"].append(self.lastCurrentPerson.id)
        self.curId += 1

        # newPerson.relationsCount += 1
        # self.lastCurrentPerson.relationsCount += 1
        # self.relationCount += 2

    def addPartner(self):
        self.edit()
        x, y = pygame.mouse.get_pos()
        self.persons[self.curId] = Person(id=self.curId, x=x, y=y)  # dodaje osobę do listy osób
        self.lastCurrentPerson.relations["partner"].append(self.curId)
        self.persons[self.curId].relations["partner"].append(self.lastCurrentPerson.id)
        self.lastCurrentPerson.relations["childrens"], self.persons[self.curId].relations["childrens"] = \
            self.lastCurrentPerson.relations["childrens"] + self.persons[self.curId].relations["childrens"], \
            self.lastCurrentPerson.relations["childrens"] + self.persons[self.curId].relations["childrens"]
        self.curId += 1

        # newPerson.relationsCount += 1
        # self.lastCurrentPerson.relationsCount += 1
        # self.relationCount += 2

    def connectParent(self):
        self.newRelation = 1
        self.relationPerson = self.lastCurrentPerson

    def connectChild(self):
        self.newRelation = 2
        self.relationPerson = self.lastCurrentPerson

    def connectSibling(self):
        self.newRelation = 3
        self.relationPerson = self.lastCurrentPerson

    def connectPartner(self):
        self.newRelation = 4
        self.relationPerson = self.lastCurrentPerson

    def info(self):
        print(
            f"name: {self.lastCurrentPerson.name} surname: {self.lastCurrentPerson.surname} age: {self.lastCurrentPerson.bornYear}")

    def add(self):
        if self.personList.buttons[2].x + 2 * self.personList.width > WIN_WIDTH:
            xList = self.personList.buttons[2].x - self.personList.width
        else:
            xList = self.personList.buttons[2].x + self.personList.width

        yList = self.personList.buttons[2].y

        self.list2 = PersonList(xList, yList, [ButtonList(xList, yList, "Parent", self.addParent),
                                               ButtonList(xList, yList + 50, "Sibling", self.addSibling),
                                               ButtonList(xList, yList + 100, "Child", self.addChild),
                                               ButtonList(xList, yList + 150, "Partner", self.addPartner)])

    def connect(self):
        if self.personList.buttons[2].x + 2 * self.personList.width > WIN_WIDTH:
            xList = self.personList.buttons[3].x - self.personList.width
        else:
            xList = self.personList.buttons[3].x + self.personList.width

        yList = self.personList.buttons[3].y

        self.list2 = PersonList(xList, yList, [ButtonList(xList, yList, "With parent", self.connectParent),
                                               ButtonList(xList, yList + 50, "With sibling", self.connectSibling),
                                               ButtonList(xList, yList + 100, "With child", self.connectChild),
                                               ButtonList(xList, yList + 150, "With partner", self.connectPartner)])

    def backToStart(self):
        for person in list(self.persons.values()):
            person.x -= self.lx
            person.y -= self.ly

        self.lx = 0
        self.ly = 0

    def newStartingPoint(self):
        self.lx = 0
        self.ly = 0

    def something(self):
        for person in list(self.persons.values()):
            print(person.relations)

    def addPicture(self):
        print("łobrozek")

    def deletePerson(self):
        # for person in self.lastCurrentPerson.relations.values():
        # print(person.relations)
        # if person != []:
        # list(person.relations.values()).remove(self.lastCurrentPerson)
        for person in list(self.persons.values()):
            for v in person.relations.values():
                if self.lastCurrentPerson.id in v:
                    v.remove(self.lastCurrentPerson.id)

        del self.persons[self.lastCurrentPerson.id]

    def saveToJSON(self):
        # for person in self.persons:
        #   person.toJSON("persons.json")
        with open("persons.json", 'w+') as file:
            file.write(json.dumps([person.__dict__ for person in list(self.persons.values())], indent=3))
        file.close()

    def loadFromJSON(self):
        with open("persons.json", "r") as file:
            data = json.load(file)
        self.persons = {id: Person(**person) for id, person in enumerate(data)}
        self.curId = len(self.persons)
        file.close()

    def main(self):

        # clock = pygame.time.Clock()
        run = True
        root = None  # główne okno tkintera

        while run:

            self.win.fill((255, 255, 200))
            events = pygame.event.get()
            # clock.tick(60)
            if len(self.persons) == 0:
                self.lx = 0
                self.ly = 0
            # odpowiedzialna za rysowanie osób
            for person in list((self.persons).values()):

                # person.r = 80 + (len(self.persons)*person.relationsCount - self.relationCount)

                x, y = pygame.mouse.get_pos()

                if x > 0.99 * WIN_WIDTH:
                    person.x -= 1 / 2
                    self.lx -= 1 / (2 * len(self.persons))

                elif x < 0.01 * WIN_WIDTH:
                    person.x += 1 / 2
                    self.lx += 1 / (2 * len(self.persons))

                if y > 0.99 * WIN_HEIGHT:
                    person.y -= 1 / 2
                    self.ly -= 1 / (2 * len(self.persons))

                elif y < 0.01 * WIN_HEIGHT:
                    person.y += 1 / 2
                    self.ly += 1 / (2 * len(self.persons))

                if self.newRelation == 1 and person.isclickedL:
                    self.newRelation = 0
                    self.relationPerson.relations["parents"].append(person.id)
                    person.relations["childrens"].append(self.relationPerson.id)
                    # self.relationCount += 1
                    # person.relationsCount += 1
                    # self.relationCount += 2

                elif self.newRelation == 2 and person.isclickedL:
                    self.newRelation = 0
                    self.relationPerson.relations["siblings"].append(person.id)
                    person.relations["siblings"].append(self.relationPerson.id)
                    # self.relationCount += 1
                    # person.relationsCount += 1
                    # self.relationCount += 2

                elif self.newRelation == 3 and person.isclickedL:
                    self.newRelation = 0
                    self.relationPerson.relations["childrens"].append(person.id)
                    person.relations["parents"].append(self.relationPerson.id)
                    # self.relationCount += 1
                    # person.relationsCount += 1
                    # self.relationCount += 2

                elif self.newRelation == 4 and person.isclickedL:
                    self.newRelation = 0
                    self.relationPerson.relations["partner"].append(person.id)
                    person.relations["partner"].append(self.relationPerson.id)
                    person.relations["childrens"], self.relationPerson.relations["childrens"] = person.relations[
                                                                                                    "childrens"] + \
                                                                                                self.relationPerson.relations[
                                                                                                    "childrens"], \
                                                                                                person.relations[
                                                                                                    "childrens"] + \
                                                                                                self.relationPerson.relations[
                                                                                                    "childrens"]
                    # self.relationCount += 1
                    # person.relationsCount += 1
                    # self.relationCount += 2

                if person.isclickedL and self.currentPerson is None:
                    self.currentPerson = person
                    self.lastCurrentPerson = person
                    person.current = True

                if person is self.currentPerson and not person.current:
                    self.currentPerson = None

                if person.isclickedR:
                    self.currentPerson = person
                    self.lastCurrentPerson = person
                    self.personList = PersonList(x, y, [ButtonList(x, y, "Edit", self.edit),
                                                        ButtonList(x, y + 50, "Info", self.info),
                                                        ButtonList(x, y + 100, " " * 18 + "Add" + " " * 18 + ">",
                                                                   command2=self.add),
                                                        ButtonList(x, y + 150, " " * 15 + "Connect" + " " * 15 + ">",
                                                                   command2=self.connect),
                                                        ButtonList(x, y + 200, "Delete Person", self.deletePerson)])

                # stary zapis relacji
                """
                for relation in list(person.relations.values()):    
                    for human in relation:
                        pygame.draw.line(self.win,(0,0,0),(human.x,human.y),(person.x,person.y))
                """
                # nowy zapis relacji

                # for human in person.relations["parents"]:
                #    pygame.draw.line(self.win,(0,0,0),(human.x,human.y),(person.x,person.y))

                for indx in person.relations["siblings"]:
                    pygame.draw.line(self.win, (0, 0, 0), (self.persons[indx].x, self.persons[indx].y),
                                     (person.x, person.y), 5)

                for indx in person.relations["childrens"]:
                    if person.relations["partner"] != []:
                        pygame.draw.line(self.win, (81, 81, 81), (self.persons[indx].x, self.persons[indx].y), (
                            (person.x + person.relations["partner"][0].x) // 2,
                            (person.y + person.relations["partner"][0].y) // 2), 5)
                    else:
                        pygame.draw.line(self.win, (81, 81, 81), (self.persons[indx].x, self.persons[indx].y),
                                         (person.x, person.y), 5)

                for indx in person.relations["partner"]:
                    pygame.draw.line(self.win, (162, 162, 162), (self.persons[indx].x, self.persons[indx].y),
                                     (person.x, person.y), 5)

                person.draw(self.win)

            if self.newRelation != 0:
                x, y = pygame.mouse.get_pos()
                pygame.draw.line(self.win, (255, 255, 255), (x, y), (self.relationPerson.x, self.relationPerson.y), 5)

            if self.personList != None:
                self.personList.draw(self.win)

            if self.list2 != None:
                self.list2.draw(self.win)

            for event in events:

                # odpowiada za zamknięcie aplikacji
                if event.type == pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:

                    if event.button == 3:
                        x, y = pygame.mouse.get_pos()
                        self.personList = PersonList(x, y, [ButtonList(x, y, "Add Person", self.addPerson),
                                                            ButtonList(x, y + 50, "Back to start", self.backToStart),
                                                            ButtonList(x, y + 100, "New starting point",
                                                                       self.newStartingPoint),
                                                            ButtonList(x, y + 150, "Something", self.something),
                                                            ButtonList(x, y + 200, "Something Else", self.something)])
                        self.list2 = None
                        self.newRelation = False

                    if event.button == 1:
                        self.personList = None
                        self.list2 = None

            # rysuje listę rozwijaną
            logout.draw(self.win)
            if logout.isclicked:
                self.saveToJSON()

            # formularz
            """
            if self.form:
                x,y = pygame.mouse.get_pos()
                root = Tk()
                root.geometry("500x500")
                firstname_text = Label(text="Firstname ", )
                firstname_text.place(x=15, y=30)
                firstname = StringVar()
                firstname_entry = Entry(textvariable=firstname, width="30")
                firstname_entry.place(x=80, y=30)
                surnname_text = Label(text="Surnname  ", )
                surnname_text.place(x=15, y=60)
                surnname = StringVar()
                surnname_entry = Entry(textvariable=surnname, width="30")
                surnname_entry.place(x=80, y=60)
                bornyear_text = Label(text="Born Year ", )
                bornyear_text.place(x=15, y=90)
                bornyear = StringVar()
                bornyear_entry = Entry(textvariable=bornyear, width="30")
                bornyear_entry.place(x=80, y=90)
                AddImg = Button(text="Add Picture", width="30", height="2", command=partial(self.addPicture))
                AddImg.place(x=140, y=180)
                save = Button(text="Save", width="30", height="2", command=partial(self.changeInformation, firstname, surnname, bornyear,root)) 
                save.place(x=140, y=230)
                """
            pygame.display.update()

            # if root:
            #    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    loginForm = LoginForm(root)
    root.mainloop()