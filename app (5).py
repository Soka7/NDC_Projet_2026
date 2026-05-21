import pyxel
from pyxel import *
from math import degrees, atan2

pyxel.init(256, 256, title = "jeu")
pyxel.fullscreen(True)
pyxel.mouse(True)
pyxel.load("U2.pyxres")

class Perso:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Rotation = None
        self.compteur = 0
        self.dgts = 1
        self.vie = 20
        self.hit = False
        
    def Angle(self):
        self.Rotation = degrees(atan2(self.y - pyxel.mouse_y, self.x - pyxel.mouse_x))
    def Zone(self):
        cx = self.x + 8
        cy = self.y + 8
        r=50
        rect(0, 0, 256, cy-r, 0)
        rect(0, cy+r, 256, 256, 0)
        rect(0, 0, cx-r, 256, 0)
        rect(cx+r, 0, 256, 256, 0)
    def Go(self):
        liste = [0]
        if btn(KEY_RIGHT) and pget(self.x + 16, self.y + 0) in liste:
            self.x += 16
            self.y += 0
        if btn(KEY_UP) and pget(self.x + 0, self.y - 16) in liste:
            self.x += 0
            self.y -= 16
        if btn(KEY_DOWN) and pget(self.x + 0, self.y + 16) in liste:
            self.x += 0
            self.y += 16
        if btn(KEY_LEFT) and pget(self.x -12, self.y + 0) in liste:
            self.x -= 16
            self.y += 0
    def Draw(self):
        bltm(0, 0, 0, 0, 0, 256, 256, colkey=4, scale=1)
        blt(self.x, self.y, 0, 96, 128, 16, 16, 4)
        blt(self.x-8, self.y-2, 0, 48, 160, 32, 16, 4, rotate = self.Rotation)
        
    def UpDgts(self):
        self.dgts += 1
        
    def IfDgts(self, Ennemie):
        Ennemy.rotation = degrees(atan2(self.y - Ennemie.PosX, self.x - Ennemie.PosX))
        if self.Rotation == Ennemy.rotation and ((Ennemie.PosX - self.x)**2 + (Ennemy.PosY - self.y)**2) <= 8**2:
            "Une fonction fait degats"
    
    def DrawVie(self):
        rect(self.x, self.y+20, self.vie*1.2, 4, 3)
        
    def PrendreCoup(self, Projectile):
        if ((Projectile.PosX - self.x)**2 + (Projectile.PosY - self.y)**2) <= 8**2:
            self.vie -= 5
        
    def Animation(self):
        if self.hit == True:
            self.x += 2
            for i in range(4):
                self.x += 4
                time.sleep(50)
                self.x -= 4
                
    def GetBoost(self):
        for element in ListeBoosts:
            if element.Boost == 0:
                self.dgts += 1
            if element.Boost == 1:
                self.vie += 1
            if element.Boost == 0:
                self.vie += 2
            
        
Main = Perso(24, 24)

def draw():
    pyxel.cls(4)
    Main.Draw()
    Main.Zone()
    Main.DrawVie()
def upt():
    Main.Angle()
    Main.compteur = (Main.compteur + 1)%2
    if Main.compteur == 0:
        Main.Go()
    Main.PrendreCoup(Stuff)

pyxel.run(draw, upt)