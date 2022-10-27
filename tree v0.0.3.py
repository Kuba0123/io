import os
import pygame
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox
from functools import partial
pygame.font.init()


pygame.font.init()

LENGTH = 200
WIN_WIDTH = 8.5*LENGTH
WIN_HEIGHT = 4.5*LENGTH
WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

FONT1 = pygame.font.SysFont('comicsans', 14)

#tworzy listę rozwijaną osoby

class PersonList:
    def __init__(self,x,y,buttons) -> None:
        self.x = x
        self.y = y
        self.buttons = buttons
        self.width = 300
        self.height = len(buttons)*50
        self.color = (240,240,240)
        self.isclicked = False

    def draw(self,win):
        x,y = pygame.mouse.get_pos()
        if x in range(self.x,self.x+self.width) and y in range(self.y,self.y+self.height):
            if pygame.mouse.get_pressed()[0] == 1:
                self.isclicked = True
            
            if pygame.mouse.get_pressed()[2] == 1:
                self.isclicked = False

        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))
        for button in self.buttons:
            button.draw(win)

def do_nothing():
    pass

#klasa przycisk
class ButtonList:
    def __init__(self, x, y,text="",command = do_nothing) -> None:
        self.x = x
        self.y = y
        self.command = command
        self.text =  FONT1.render(str(text), 1, (0,0,0))
        self.width = 300
        self.height = 50
        self.costume = 0
        self.colors = [(240,240,240),(200,200,200)]
        self.isclicked = False
        
    def draw(self, win):

        x,y = pygame.mouse.get_pos()
        
        if x in range(self.x,self.x+self.width) and y in range(self.y,self.y+self.height):
            self.costume = 1
            if pygame.mouse.get_pressed()[0] == 1:
                self.isclicked = True
                self.command()
            elif pygame.mouse.get_pressed()[2] == 1:
                self.isclicked = False
                
                
        else:
            self.costume = 0
        
        pygame.draw.rect(win,self.colors[self.costume],(self.x,self.y,self.width,self.height))
        win.blit(self.text, ((2*self.x+self.width)//2 - (self.text.get_width())//2, (2*self.y + self.height)//2 - (self.text.get_height())//2))

class Person:
    def __init__(self,x=300,y=300,r=100,name = "Adam",surname = "Kowalski",bornYear = 2000,img = []) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.colors = [(7, 56, 99),(107, 56, 99)]
        self.costume = 0
        self.bool = False
        #self.relations = set()
        self.name = name
        self.surname = surname
        self.bornYear = bornYear
        self.img = img
        self.parents = []
        self.childrens = []
        self.siblings = []
        self.isclickedR = False
        self.isclickedL = False
        self.partner = None


    def draw(self,win):
        x,y = pygame.mouse.get_pos()
        
        if ((x-self.x)**2 + (y-self.y)**2)**0.5 <= self.r:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if pygame.mouse.get_pressed()[2] == 1:
                self.isclickedR = True
            else:
                self.isclickedR = False

            if pygame.mouse.get_pressed()[0] == 1:
                self.isclickedL = True
            else:
                self.isclickedL = False
                
        else:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if self.isclickedL:
            self.x = x
            self.y = y

        pygame.draw.circle(win,self.colors[self.costume],(self.x,self.y),self.r) #rysuje osobę
        #for relation in list(self.relations):
        #    pygame.draw.line(win,self.color,(self.x,self.y),(relation.x,relation.y)) #rysuje relacje między osobami
        s = FONT1.render(str(self.name) + " " + str(self.surname) + " " + str(self.bornYear) , 1, (0,255,255)) 
        win.blit(s,(self.x -s.get_width()//2,(self.y-s.get_height()//2)+50)) #wyświetla imię, nazwisko i rok urodzenia


forPersonList = []
forBgList = []

class Game:
    def __init__(self) -> None:
        self.persons = []
        self.form = False
        self.currentPerson = None
        self.personList = None

    def edit(self):
        self.form = True
        self.personList = None

    def changeInformation(self, name, surname, bornyear,root):
        self.currentPerson.name = name.get()  
        self.currentPerson.surname = surname.get()
        self.currentPerson.bornYear = bornyear.get()
        root.quit()
        self.form = False
    
    #uaktualnia dane po edycji w formularzu
    
    def addPerson(self,name="Adam",surname="Kowalski",bornYear=2000):
        newPerson = Person(name=name,surname=surname,bornYear=bornYear)
        self.persons.append(newPerson) #dodaje osobę do listy osób 
    
    def AddParent(self, name="Adam",surname="Kowalski",bornYear=2000):
        self.persons.append(Person(name=name,surname=surname,bornYear=bornYear))
        newPerson = Person(name=name,surname=surname,bornYear=bornYear)
        self.persons.append(newPerson) #dodaje osobę do listy osób 
        self.currentPerson.parents.append(newPerson)

    def AddChild(self, name="Adam",surname="Kowalski",bornYear=2000):
        self.persons.append(Person(name=name,surname=surname,bornYear=bornYear))
        newPerson = Person(name=name,surname=surname,bornYear=bornYear)
        self.persons.append(newPerson) #dodaje osobę do listy osób 
        self.currentPerson.childrens.append(newPerson)

    def AddSibling(self, name="Adam",surname="Kowalski",bornYear=2000):
        self.persons.append(Person(name=name,surname=surname,bornYear=bornYear))
        newPerson = Person(name=name,surname=surname,bornYear=bornYear)
        self.persons.append(newPerson) #dodaje osobę do listy osób 
        self.currentPerson.siblings.append(newPerson)

    def AddPicture(self):
        print("łobrozek")


    def main(self,win):

        clock = pygame.time.Clock()
        run = True 
        root = None #główne okno tkintera

        while run:

            win.fill((255,255,200))
            events = pygame.event.get()
            clock.tick(60)

            #odpowiedzialna za rysowanie osób
            for person in self.persons:
                if person.isclickedR:
                    self.currentPerson = person
                    self.personList = PersonList(x,y,[ButtonList(x,y,"Edit",self.edit),ButtonList(x,y+50,"Add Parents",self.AddParent),ButtonList(x,y+100,"Add Children",self.AddChild),ButtonList(x,y+150,"Add Siblings",self.AddSibling)])
                    
                person.draw(win)

            if self.personList != None:
                self.personList.draw(win)

            for event in events:
                if event.type==pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()

                #odpowiada za zamknięcie aplikacji    
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if event.button == 3:
                        x,y = pygame.mouse.get_pos()
                        self.personList = PersonList(x,y,[ButtonList(x,y,"Add Person",self.addPerson),ButtonList(x,y+50,"Something"),ButtonList(x,y+100,"Something Else")])

                    if event.button == 1:
                        self.personList = None                
 
            #rysuje listę rozwijaną

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

                #AddParents = Button(text="Add Parents", width="30", height="2", command=partial(self.AddParent))
                #AddParents.place(x=15, y=120)

                #AddChild = Button(text="Add Child", width="30", height="2", command=partial(self.AddChild))
                #AddChild.place(x=260, y=120)

                AddImg = Button(text="Add Picture", width="30", height="2", command=partial(self.AddPicture))
                AddImg.place(x=140, y=180)

                save = Button(text="Save", width="30", height="2", command=partial(self.changeInformation, firstname, surnname, bornyear,root)) 
                save.place(x=140, y=230)

            #formularz 
            pygame.display.update()

            if root:
                root.mainloop()
    
            
if __name__ == "__main__":
    game = Game()
    game.main(WIN)
