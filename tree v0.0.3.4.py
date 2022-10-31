import os
import pygame
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox
from functools import partial
pygame.font.init()


LENGTH = 200
WIN_WIDTH = 8.5*LENGTH
WIN_HEIGHT = 4.5*LENGTH
WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

FONT1 = pygame.font.SysFont('comicsans', 20)
FONT2 = pygame.font.SysFont('comicsans', 35)

class ButtonLogOut:
    def __init__(self) -> None:
        self.text =  FONT2.render("Log Out", 1, (0,0,0))
        self.x = int(WIN_WIDTH - self.text.get_width() - 20)
        self.y = int(WIN_HEIGHT - self.text.get_height() - 10)
        self.height = int(self.text.get_width())
        self.width = int(self.text.get_width())
        
    
    def draw(self,win):
        x,y = pygame.mouse.get_pos()
        if x in range(self.x,self.x+self.width) and y in range(self.y,self.y+self.height):
            self.text =  FONT2.render("Log Out", 1, (200,200,200))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            if pygame.mouse.get_pressed()[0] == 1:
                print("Wylogowano")
        else:
            self.text =  FONT2.render("Log Out", 1, (0,0,0))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            
        win.blit(self.text, (self.x,self.y))
        
logout = ButtonLogOut()

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
                
        #pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.height))



        #sprawia że wyświetlana lista jest w oknie programu
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
        self.current = False
        self.name = name
        self.surname = surname
        self.bornYear = bornYear
        self.img = img
        self.relations = {"parents":[],"childrens":[],"siblings":[]}
        self.isclickedR = False
        self.isclickedL = False
        self.partner = None


    def draw(self,win):
        x,y = pygame.mouse.get_pos()
        
        if ((x-self.x)**2 + (y-self.y)**2)**0.5 <= self.r:
            #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

            if pygame.mouse.get_pressed()[2] == 1:
                self.isclickedR = True
            else:
                self.isclickedR = False

            if pygame.mouse.get_pressed()[0] == 1:
                self.isclickedL = True

            else:
                self.isclickedL = False
                self.current = False

        else:
            self.current = False
                

        if self.isclickedL and self.current:
            self.x = x
            self.y = y

        pygame.draw.circle(win,self.colors[self.costume],(self.x,self.y),self.r) #rysuje osobę
        #for relation in list(self.relations):
        #    pygame.draw.line(win,self.color,(self.x,self.y),(relation.x,relation.y)) #rysuje relacje między osobami
        s = FONT1.render(str(self.name) + " " + str(self.surname), 1, (0,255,255)) 
        win.blit(s,(self.x -s.get_width()//2,(self.y-s.get_height()//2)+120)) #wyświetla imię, nazwisko i rok urodzenia

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
    
    def addParent(self, name="Adam",surname="Kowalski",bornYear=2000):
        newPerson = Person(name=name,surname=surname,bornYear=bornYear)
        self.persons.append(newPerson) #dodaje osobę do listy osób 
        self.currentPerson.relations["parents"].append(newPerson)
        newPerson.relations["childrens"].append(self.currentPerson)

    def addChild(self, name="Adam",surname="Kowalski",bornYear=2000):
        newPerson = Person(name=name,surname=surname,bornYear=bornYear)
        self.persons.append(newPerson) #dodaje osobę do listy osób 
        self.currentPerson.relations["childrens"].append(newPerson)
        newPerson.relations["parents"].append(self.currentPerson)

    def addSibling(self, name="Adam",surname="Kowalski",bornYear=2000):
        newPerson = Person(name=name,surname=surname,bornYear=bornYear)
        self.persons.append(newPerson) #dodaje osobę do listy osób 
        self.currentPerson.relations["siblings"].append(newPerson)
        newPerson.relations["siblings"].append(self.currentPerson)

    def something(self):
        for person in self.persons:
            print(person.relations)

    def addPicture(self):
        print("łobrozek")

    def deletePerson(self):
        self.persons.remove(self.currentPerson)

    def main(self,win):

        clock = pygame.time.Clock()
        run = True 
        root = None #główne okno tkintera

        while run:
            
            win.fill((255,255,200))
            events = pygame.event.get()
            #clock.tick(60)

            #odpowiedzialna za rysowanie osób
            for person in self.persons:

                if person.isclickedL and self.currentPerson is None:
                    self.currentPerson = person
                    person.current = True

                if person is self.currentPerson and not person.current:
                    self.currentPerson = None

                if person.isclickedR:
                    self.currentPerson = person
                    self.personList = PersonList(x,y,[ButtonList(x,y,"Edit",self.edit),ButtonList(x,y+50,"Add Parents",self.addParent),ButtonList(x,y+100,"Add Children",self.addChild),ButtonList(x,y+150,"Add Siblings",self.addSibling),ButtonList(x,y+200,"Delete Person",self.deletePerson)])
                
            
                for relation in list(person.relations.values()):    
                    for human in relation:
                        pygame.draw.line(win,(0,0,0),(human.x,human.y),(person.x,person.y))

                person.draw(win)

            if self.personList != None:
                self.personList.draw(win)

            for event in events:

                #odpowiada za zamknięcie aplikacji  
                if event.type==pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if event.button == 3:
                        x,y = pygame.mouse.get_pos()
                        self.personList = PersonList(x,y,[ButtonList(x,y,"Add Person",self.addPerson),ButtonList(x,y+50,"Something",self.something),ButtonList(x,y+100,"Something Else",self.something)])

                    if event.button == 1:
                        self.personList = None                
 
            #rysuje listę rozwijaną
            logout.draw(win)
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

                AddImg = Button(text="Add Picture", width="30", height="2", command=partial(self.addPicture))
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
