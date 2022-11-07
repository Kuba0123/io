import os
import threading
import pygame
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox
from functools import partial
import json
pygame.font.init()


LENGTH = 200
WIN_WIDTH = 8.5*LENGTH
WIN_HEIGHT = 4.5*LENGTH
WIN = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

FONT1 = pygame.font.SysFont('comicsans', 20)
FONT2 = pygame.font.SysFont('comicsans', 35)

class InfoWindow:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y

    def draw(self,win):
        pass

    
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
    def __init__(self, x, y,text="",command = do_nothing,command2 = do_nothing) -> None:
        self.x = x
        self.y = y
        self.command = command
        self.command2 = command2
        self.text =  FONT1.render(str(text), 1, (0,0,0))
        self.width = 300
        self.height = 50
        self.costume = 0
        self.colors = [(240,240,240),(200,200,200)]
        self.isclicked = False
        self.time = 0
        
    def draw(self, win):

        x,y = pygame.mouse.get_pos()
        if x in range(self.x,self.x+self.width) and y in range(self.y,self.y+self.height):
            self.costume = 1
            self.time += 1
            if pygame.mouse.get_pressed()[0] == 1:
                self.isclicked = True
                self.command()
            elif pygame.mouse.get_pressed()[2] == 1:
                self.isclicked = False

            if self.time>20:
                self.command2()
        else:
            self.costume = 0
            self.time = 0

        pygame.draw.rect(win,self.colors[self.costume],(self.x,self.y,self.width,self.height))
        win.blit(self.text, ((2*self.x+self.width)//2 - (self.text.get_width())//2, (2*self.y + self.height)//2 - (self.text.get_height())//2))


class Person:
    def __init__(self,x=100,y=100,r=80,name = "",surname = "",bornYear = 0,img = []) -> None:
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
        self.relations = {"parents":[],"childrens":[],"siblings":[],"partner":[]}
        self.isclickedR = False
        self.isclickedL = False
        self.partner = None
        self.time = 0
        #self.relationsCount = 0


    def draw(self,win):
        x,y = pygame.mouse.get_pos()
        
        if ((x-self.x)**2 + (y-self.y)**2)**0.5 <= self.r:
            #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            #self.costume = 1
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
            #self.costume = 0

        if self.isclickedL and self.current:
            self.x = x
            self.y = y

        pygame.draw.circle(win,self.colors[self.costume],(self.x,self.y),self.r) #rysuje osobę
        #for relation in list(self.relations):
        #    pygame.draw.line(win,self.color,(self.x,self.y),(relation.x,relation.y)) #rysuje relacje między osobami
        s = FONT1.render(f"{self.name} {self.surname}", 1, (0,255,255)) 
        win.blit(s,(self.x -s.get_width()//2,(self.y-s.get_height()//2)+1.2*self.r)) #wyświetla imię, nazwisko i rok urodzenia

        """ 
        if self.time > 250:
            x,y = pygame.mouse.get_pos()
            pygame.draw.rect(win,(30,100,200),(x,y,4*self.r,2*self.r))
            text = FONT1.render(f"{self.name} {self.surname} {self.bornYear}", 1, (255,255,255))
            win.blit(text,(x + 2*self.r-text.get_width()//2,y + self.r-text.get_height()//2)) 
       """ 

class Game:
    def __init__(self,win) -> None:
        self.win = win
        self.persons = []
        self.form = False
        self.currentPerson = None
        self.lastCurrentPerson = None
        self.relationPerson = None
        self.personList = None
        self.list2 = None
        self.newRelation = 0
        #self.relationCount = 0
        self.lx = 0
        self.ly = 0
    
    def forma(self):
        #x,y = pygame.mouse.get_pos()
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

        root.mainloop()
        

    def edit(self):
        t = threading.Thread(target=self.forma)
        t.start()
        #self.form = True
        self.personList = None

    #uaktualnia dane po edycji w formularzu
    def changeInformation(self, name, surname, bornyear,root):
        self.lastCurrentPerson.name = name.get()  
        self.lastCurrentPerson.surname = surname.get()
        self.lastCurrentPerson.bornYear = bornyear.get()
        root.destroy()
        #self.form = False
        

    def addPerson(self):
        self.edit()
        x,y = pygame.mouse.get_pos()
        newPerson = Person(x=x,y=y)
        self.persons.append(newPerson) #dodaje osobę do listy osób
        
    

    def addParent(self):
        self.edit()
        x,y = pygame.mouse.get_pos()
        newPerson = Person(x=x,y=y)
        self.persons.append(newPerson) #dodaje osobę do listy osób 
        self.lastCurrentPerson.relations["parents"].append(newPerson)
        newPerson.relations["childrens"].append(self.lastCurrentPerson)
        #newPerson.relationsCount += 1
        #self.lastCurrentPerson.relationsCount += 1
        #self.relationCount += 2


    def addChild(self):
        self.edit()
        x,y = pygame.mouse.get_pos()
        newPerson = Person(x=x,y=y)
        self.persons.append(newPerson) #dodaje osobę do listy osób 
        self.lastCurrentPerson.relations["childrens"].append(newPerson)
        newPerson.relations["parents"].append(self.lastCurrentPerson)
        #newPerson.relationsCount += 1
        #self.lastCurrentPerson.relationsCount += 1
        #self.relationCount += 2


    def addSibling(self):
        self.edit()
        x,y = pygame.mouse.get_pos()
        newPerson = Person(x=x,y=y)
        self.persons.append(newPerson) #dodaje osobę do listy osób 
        self.lastCurrentPerson.relations["siblings"].append(newPerson)
        newPerson.relations["siblings"].append(self.lastCurrentPerson)

        #newPerson.relationsCount += 1
        #self.lastCurrentPerson.relationsCount += 1
        #self.relationCount += 2


    def addPartner(self):
        self.edit()
        x,y = pygame.mouse.get_pos()
        newPerson = Person(x=x,y=y)
        self.persons.append(newPerson)
        self.lastCurrentPerson.relations["partner"].append(newPerson)
        newPerson.relations["partner"].append(self.lastCurrentPerson)
        self.lastCurrentPerson.relations["childrens"],newPerson.relations["childrens"] = self.lastCurrentPerson.relations["childrens"] + newPerson.relations["childrens"],self.lastCurrentPerson.relations["childrens"] + newPerson.relations["childrens"]
        #newPerson.relationsCount += 1
        #self.lastCurrentPerson.relationsCount += 1
        #self.relationCount += 2



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
        print(f"name: {self.lastCurrentPerson.name} surname: {self.lastCurrentPerson.surname} age: {self.lastCurrentPerson.bornYear}")


    def add(self):
        if self.personList.buttons[2].x + 2*self.personList.width > WIN_WIDTH:
            xList = self.personList.buttons[2].x - self.personList.width   
        else:
            xList = self.personList.buttons[2].x + self.personList.width

        yList = self.personList.buttons[2].y
        
        self.list2 = PersonList(xList,yList,[ButtonList(xList,yList,"Parent",self.addParent),ButtonList(xList,yList + 50,"Sibling",self.addSibling),ButtonList(xList,yList + 100,"Child",self.addChild),ButtonList(xList,yList + 150,"Partner",self.addPartner)])

    def connect(self):
        if self.personList.buttons[2].x + 2*self.personList.width > WIN_WIDTH:
            xList = self.personList.buttons[3].x - self.personList.width   
        else:
            xList = self.personList.buttons[3].x + self.personList.width

        yList = self.personList.buttons[3].y
        
        self.list2 = PersonList(xList,yList,[ButtonList(xList,yList,"With parent",self.connectParent),ButtonList(xList,yList + 50,"With sibling",self.connectSibling),ButtonList(xList,yList + 100,"With child",self.connectChild),ButtonList(xList,yList + 150,"With partner",self.connectPartner)])

    def backToStart(self):
        for person in self.persons:
            person.x -= self.lx
            person.y -= self.ly

        self.lx = 0
        self.ly = 0


    def newStartingPoint(self):
        self.lx = 0
        self.ly = 0


    def something(self):
        for person in self.persons:
            print(person.relations)


    def addPicture(self):
        print("łobrozek")


    def deletePerson(self):
        #for person in self.lastCurrentPerson.relations.values():
            #print(person.relations)
            #if person != []:
                #list(person.relations.values()).remove(self.lastCurrentPerson)
        for person in self.persons:
            for v in person.relations.values():
                if self.lastCurrentPerson in v:
                    v.remove(self.lastCurrentPerson)

        self.persons.remove(self.lastCurrentPerson)


    def main(self):

        #clock = pygame.time.Clock()
        run = True 
        root = None #główne okno tkintera

        while run:
            
            self.win.fill((255,255,200))
            events = pygame.event.get()
            #clock.tick(60)
            if len(self.persons) == 0:
                self.lx = 0
                self.ly = 0
            #odpowiedzialna za rysowanie osób
            for person in self.persons:

                #person.r = 80 + (len(self.persons)*person.relationsCount - self.relationCount)

                x,y = pygame.mouse.get_pos()
                
                if x>0.99*WIN_WIDTH:
                    person.x -= 1/2
                    self.lx -= 1/(2*len(self.persons))

                elif x<0.01*WIN_WIDTH:
                    person.x += 1/2
                    self.lx += 1/(2*len(self.persons))

                if y>0.99*WIN_HEIGHT:
                    person.y -= 1/2
                    self.ly -= 1/(2*len(self.persons))

                elif y<0.01*WIN_HEIGHT:
                    person.y += 1/2
                    self.ly += 1/(2*len(self.persons))


                if self.newRelation == 1 and person.isclickedL:
                    self.newRelation = 0
                    self.relationPerson.relations["parents"].append(person)
                    person.relations["childrens"].append(self.relationPerson)
                    #self.relationCount += 1
                    #person.relationsCount += 1
                    #self.relationCount += 2

                elif self.newRelation == 2 and person.isclickedL:
                    self.newRelation = 0
                    self.relationPerson.relations["siblings"].append(person)
                    person.relations["siblings"].append(self.relationPerson)
                    #self.relationCount += 1
                    #person.relationsCount += 1
                    #self.relationCount += 2

                elif self.newRelation == 3 and person.isclickedL:
                    self.newRelation = 0
                    self.relationPerson.relations["childrens"].append(person)
                    person.relations["parents"].append(self.relationPerson)
                    #self.relationCount += 1
                    #person.relationsCount += 1
                    #self.relationCount += 2

                elif self.newRelation == 4 and person.isclickedL:
                    self.newRelation = 0
                    self.relationPerson.relations["partner"].append(person)
                    person.relations["partner"].append(self.relationPerson)
                    person.relations["childrens"],self.relationPerson.relations["childrens"] = person.relations["childrens"] + self.relationPerson.relations["childrens"], person.relations["childrens"] + self.relationPerson.relations["childrens"]
                    #self.relationCount += 1
                    #person.relationsCount += 1
                    #self.relationCount += 2   
                
                if person.isclickedL and self.currentPerson is None:
                    self.currentPerson = person
                    self.lastCurrentPerson = person
                    person.current = True

                if person is self.currentPerson and not person.current:
                    self.currentPerson = None
                
                if person.isclickedR:
                    self.currentPerson = person
                    self.lastCurrentPerson = person
                    self.personList = PersonList(x,y,[ButtonList(x,y,"Edit",self.edit),ButtonList(x,y+50,"Info",self.info),ButtonList(x,y+100," "*18 + "Add" + " "*18 + ">",command2 = self.add),ButtonList(x,y+150," "*15 + "Connect" + " "*15 + ">",command2 = self.connect),ButtonList(x,y+200,"Delete Person",self.deletePerson)])
                
                #stary zapis relacji
                """
                for relation in list(person.relations.values()):    
                    for human in relation:
                        pygame.draw.line(self.win,(0,0,0),(human.x,human.y),(person.x,person.y))
                """
                #nowy zapis relacji
                
                #for human in person.relations["parents"]:
                #    pygame.draw.line(self.win,(0,0,0),(human.x,human.y),(person.x,person.y))
            
            
                for human in person.relations["siblings"]:    
                    pygame.draw.line(self.win,(0,0,0),(human.x,human.y),(person.x,person.y),5)

            
                for human in person.relations["childrens"]:
                    if person.relations["partner"] != []:
                        pygame.draw.line(self.win,(81,81,81),(human.x,human.y),((person.x + person.relations["partner"][0].x)//2 ,(person.y + person.relations["partner"][0].y)//2),5)
                    else:
                        pygame.draw.line(self.win,(81,81,81),(human.x,human.y),(person.x,person.y),5)
            
            
                for human in person.relations["partner"]:    
                    pygame.draw.line(self.win,(162,162,162),(human.x,human.y),(person.x,person.y),5)

                person.draw(self.win)

            if self.newRelation != 0:
                x,y = pygame.mouse.get_pos()
                pygame.draw.line(self.win,(255,255,255),(x,y),(self.relationPerson.x,self.relationPerson.y),5)

            if self.personList != None:
                self.personList.draw(self.win)

            if self.list2 != None:
                self.list2.draw(self.win)
                

            for event in events:

                #odpowiada za zamknięcie aplikacji  
                if event.type==pygame.QUIT:
                    run = False
                    pygame.quit()
                    quit()
                  
                if event.type == pygame.MOUSEBUTTONDOWN:
                    
                    if event.button == 3:
                        x,y = pygame.mouse.get_pos()
                        self.personList = PersonList(x,y,[ButtonList(x,y,"Add Person",self.addPerson),ButtonList(x,y+50,"Back to start",self.backToStart),ButtonList(x,y+100,"New starting point",self.newStartingPoint),ButtonList(x,y+150,"Something",self.something),ButtonList(x,y+200,"Something Else",self.something)])
                        self.list2 = None
                        self.newRelation = False

                    if event.button == 1:
                        self.personList = None 
                        self.list2 = None
            
 
            #rysuje listę rozwijaną
            logout.draw(self.win)

            #formularz
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

            #if root:
            #    root.mainloop()

    
if __name__ == "__main__":
    game = Game(WIN)
    game.main()
