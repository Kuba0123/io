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

FONT1 = pygame.font.SysFont('comicsans', 14)

class MainMenu:
    def __init__(self) -> None:
        self.x = 50
        self.y = 50
        self.width = 500
        self.heigth = 100
        self.color = (100,60,50)
        self.button = 50
        self.buttonColor = (12,124,20)

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.heigth)) #rysuje główne menu
        pygame.draw.rect(win,self.buttonColor,(self.x+self.button,self.y+(self.heigth-self.button)//2,self.button,self.button)) #rysuje pierwszy przycisk
        pygame.draw.rect(win,self.buttonColor,(self.x+3*self.button,self.y+(self.heigth-self.button)//2,self.button,self.button)) #rysuje drugi przycisk
        pygame.draw.rect(win,self.buttonColor,(self.x+5*self.button,self.y+(self.heigth-self.button)//2,self.button,self.button)) #rysuje trzeci przycisk


menu = MainMenu() # tworzy obiekt klasy MainMenu

#tworzył listę rozwijaną osoby

class PersonList:
    def __init__(self,x,y) -> None:
        self.x = x
        self.y = y
        self.length = 300
        self.height = 400
        self.color = (240,240,240)
    
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.length,self.height))



class Person:
    def __init__(self,x=300,y=300,r=100,name = "Adam",surname = "Kowalski",bornYear = 2000,img = []) -> None:
        self.x = x
        self.y = y
        self.r = r
        self.color = (7, 56, 99)
        self.bool = False
        self.relations = set()
        self.name = name
        self.surname = surname
        self.bornYear = bornYear
        self.img = img
        self.parents = []
        self.children = []
        self.siblings = []
        self.partner = None


    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.r) #rysuje osobę
        for relation in list(self.relations):
            pygame.draw.line(win,self.color,(self.x,self.y),(relation.x,relation.y)) #rysuje relacje między osobami
        s = FONT1.render(str(self.name) + " " + str(self.surname) + " " + "(" + str(self.bornYear) + ")", 1, (0,255,255)) 
        win.blit(s,(self.x -s.get_width()//2,(self.y-s.get_height()//2)+50)) #wyświetla imię, nazwisko i rok urodzenia



    def options(self,win): #w planie będzie tworzyło listę rozwijaną
        pass


#embed = tk.Frame(root, width = 500, height = 500) #creates embed frame for pygame window
#embed.grid(columnspan = (600), rowspan = 500) # Adds grid
#embed.pack(side = LEFT) #packs window to the left
#buttonwin = tk.Frame(root, width = 75, height = 500)
#buttonwin.pack(side = LEFT)
#os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
#os.environ['SDL_VIDEODRIVER'] = 'windib'

class Game:
    def __init__(self) -> None:
        self.persons = []
        self.button3 = False
        self.currentPerson = None

    def changeName(self, name):
        self.currentPerson.name = name.get() #zmienia imie po edycji w formularzu
    
    def addPerson(self,name="Adam",surname="Kowalski",bornYear=2000):
        self.persons.append(Person(name=name,surname=surname,bornYear=bornYear)) #dodaje osobę do listy osób 
    
    def main(self,win):
        clock = pygame.time.Clock()
        run = True 
        root = None #główne okno tkintera
        relationBool = False #służy przy dodawaniu relacji (button 2)
        tempSet = set() #do niego dodawane są osoby tymczasowo osoby które są w relacji
        personList = None
        while run:

            win.fill((255,255,200))
            events = pygame.event.get()
            clock.tick(30)
            self.button3 = False 
            for event in events:
                if event.type==pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    run = False
                    pygame.quit()
                    quit()
                #odpowiada za zamknięcie aplikacji

                if event.type == pygame.MOUSEMOTION:
                    x,y = pygame.mouse.get_pos()
                    p = False
                    for person in self.persons:
                        if ((x-person.x)**2 + (y-person.y)**2)**0.5 <= person.r:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            p = True
                        
                    if not p:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                #zmienia kursor po najechaniu na osobę
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    for person in self.persons:
                        if ((x-person.x)**2 + (y-person.y)**2)**0.5 <= person.r and not relationBool:
                            if event.button == 1:
                                person.bool = True
                                self.currentPerson = person
                            elif event.button == 3:
                                personList = PersonList(x,y)
                            #tworzy listę dla osoby
                    
                        
                    #po kliknięciu na osobę zmienia ją na obecną i tworzy listę rozwijaną

                        elif ((x-person.x)**2 + (y-person.y)**2)**0.5 <= person.r and relationBool:
                            tempSet.add(person)
                    #służy do dodawania relacji między osobami
                        if event.button == 1 and personList != None:
                            personList = None
                    #usuwa listę dla osoby

                if event.type == pygame.MOUSEBUTTONUP:
                    for person in self.persons:
                        person.bool = False

            
                if event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    if x in range(menu.x,menu.x + menu.width) and y in range(menu.y,menu.y + menu.heigth):
                        if x in range(menu.x+menu.button,menu.x+2*menu.button) and y in range(menu.y+(menu.heigth-menu.button)//2,menu.y+(menu.heigth-menu.button)//2+menu.button):
                            self.addPerson()
                        #pierwszy przycisk tworzy nową osobę
                        elif x in range(menu.x+3*menu.button,menu.x+4*menu.button) and y in range(menu.y+(menu.heigth-menu.button)//2,menu.y+(menu.heigth-menu.button)//2+menu.button):
                            relationBool = True
                        #drugi przycisk odpowiedzialny za robienie relacji

                        elif x in range(menu.x+5*menu.button,menu.x+6*menu.button) and y in range(menu.y+(menu.heigth-menu.button)//2,menu.y+(menu.heigth-menu.button)//2+menu.button):
                            self.button3 = True
                            if root:
                                root.quit()
                        #trzeci przycisk uruchamia formularz

                if event.type == pygame.MOUSEMOTION:
                    x,y = pygame.mouse.get_pos()
                    if x in range(menu.x,menu.x + menu.width) and y in range(menu.y,menu.y + menu.heigth):
                        if any([x in range(menu.x+menu.button,menu.x+2*menu.button),x in range(menu.x+3*menu.button,menu.x+4*menu.button),x in range(menu.x+5*menu.button,menu.x+6*menu.button)]) and y in range(menu.y+(menu.heigth-menu.button)//2,menu.y+(menu.heigth-menu.button)//2+menu.button):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                #zmienia kursor myszy po najechaniu na obiekt klasy MainMenu
                
            menu.draw(win)
            if len(list(tempSet)) >= 2:
                list(tempSet)[0].relations.add(list(tempSet)[1])
                list(tempSet)[1].relations.add(list(tempSet)[0])
                tempSet.clear()
                relationBool = False
            #tworzy relacje między osobami
            

            for person in self.persons:
                x,y = pygame.mouse.get_pos()
                if person.bool:
                    person.x = x
                    person.y = y
                if person is self.currentPerson:
                    person.color = (107, 56, 99)
                else:
                    person.color = (7, 56, 99)
                person.draw(win)
            #odpowiedzialna za rysowanie osób
            

            if self.currentPerson == None and len(self.persons)==1:
                self.currentPerson = self.persons[0]
            #ustawia pierwszą osobę jako obecną

            if personList != None:
                personList.draw(win)
            #rysuje listę rozwijaną

            if self.button3:
                root = Tk()
                root.geometry("500x500")
                firstname_text = Label(text = "Firstname ",)
                firstname_text.place(x = 15, y = 70)
                firstname = StringVar()
                firstname_entry = Entry(textvariable=firstname,width = "30")
                firstname_entry.place(x = 15 ,y = 100)
                register = Button(text = "Register", width="30",height="2",command=partial(self.changeName, firstname))
                register.place(x = 0, y = 130)
            #formularz 
            pygame.display.update()

            if root:
                root.mainloop()
            
if __name__ == "__main__":
    game = Game()
    game.main(WIN)
