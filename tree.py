import os
import pygame
import tkinter as tk
from tkinter import *
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox

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
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.heigth))
        pygame.draw.rect(win,self.buttonColor,(self.x+self.button,self.y+(self.heigth-self.button)//2,self.button,self.button))
        pygame.draw.rect(win,self.buttonColor,(self.x+3*self.button,self.y+(self.heigth-self.button)//2,self.button,self.button))
        pygame.draw.rect(win,self.buttonColor,(self.x+5*self.button,self.y+(self.heigth-self.button)//2,self.button,self.button))


menu = MainMenu()

class Person:
    def __init__(self,x,y,r,name = "Adam",surname = "Kowalski",bornYear = "2000",img = []) -> None:
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

    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.r)
        for relation in list(self.relations):
            pygame.draw.line(win,self.color,(self.x,self.y),(relation.x,relation.y))
        s = FONT1.render(self.name + " " + self.surname + " " + "(" + self.bornYear + ")", 1, (0,255,255))
        win.blit(s,(self.x -s.get_width()//2,(self.y-s.get_height()//2)+50))


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

    def addPerson(self,x,y,r):
        self.persons.append(Person(x,y,r))

    def main(self,win):
        clock = pygame.time.Clock()
        run = True
        root = None
        relationBool = False
        tempSet = set()
        person = Person(100,100,50)
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

                if event.type == pygame.MOUSEMOTION:
                    x,y = pygame.mouse.get_pos()
                    p = False
                    for person in self.persons:
                        if ((x-person.x)**2 + (y-person.y)**2)**0.5 <= person.r:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                            p = True
                        
                    if not p:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    for person in self.persons:
                        if ((x-person.x)**2 + (y-person.y)**2)**0.5 <= person.r and not relationBool:
                            person.bool = True
                        elif ((x-person.x)**2 + (y-person.y)**2)**0.5 <= person.r and relationBool:
                            tempSet.add(person)

                if event.type == pygame.MOUSEBUTTONUP:
                    for person in self.persons:
                        person.bool = False

            
                if event.type == pygame.MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    if x in range(menu.x,menu.x + menu.width) and y in range(menu.y,menu.y + menu.heigth):
                        if x in range(menu.x+menu.button,menu.x+2*menu.button) and y in range(menu.y+(menu.heigth-menu.button)//2,menu.y+(menu.heigth-menu.button)//2+menu.button):
                            self.addPerson(300,300,100)
                        elif x in range(menu.x+3*menu.button,menu.x+4*menu.button) and y in range(menu.y+(menu.heigth-menu.button)//2,menu.y+(menu.heigth-menu.button)//2+menu.button):
                            relationBool = True
                        elif x in range(menu.x+5*menu.button,menu.x+6*menu.button) and y in range(menu.y+(menu.heigth-menu.button)//2,menu.y+(menu.heigth-menu.button)//2+menu.button):
                            self.button3 = True
                            if root:
                                root.quit()
                                


                if event.type == pygame.MOUSEMOTION:
                    x,y = pygame.mouse.get_pos()
                    if x in range(menu.x,menu.x + menu.width) and y in range(menu.y,menu.y + menu.heigth):
                        if any([x in range(menu.x+menu.button,menu.x+2*menu.button),x in range(menu.x+3*menu.button,menu.x+4*menu.button),x in range(menu.x+5*menu.button,menu.x+6*menu.button)]) and y in range(menu.y+(menu.heigth-menu.button)//2,menu.y+(menu.heigth-menu.button)//2+menu.button):
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                        else:
                            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

                
            menu.draw(win)
            if len(list(tempSet)) >= 2:
                print(tempSet)
                list(tempSet)[0].relations.add(list(tempSet)[1])
                list(tempSet)[1].relations.add(list(tempSet)[0])
                tempSet.clear()
                relationBool = False
            
            for person in self.persons:
                x,y = pygame.mouse.get_pos()
                if person.bool:
                    person.x = x
                    person.y = y
                person.draw(win)

            if self.button3:
                root = tk.Tk()
                root.geometry("500x500") 
            
            pygame.display.update()

            if root:
                root.mainloop()
            

            
            
if __name__ == "__main__":
    game = Game()
    game.main(WIN)