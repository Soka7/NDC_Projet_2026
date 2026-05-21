import pyxel
from pyxel import *
from math import degrees, atan2

pyxel.init(256, 256, title = "jeu")
pyxel.fullscreen(False)
pyxel.mouse(True)
pyxel.load("U2.pyxres")

class Perso:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Rotation = None
        self.compteur = 0
        
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
        blt(self.x-8, self.y-2, 0, 32, 128, 32, 16, 4, rotate = self.Rotation)
        
Main = Perso(24, 24)

def draw():
    pyxel.cls(4)
    Main.Draw()
    Main.Zone()
def upt():
    Main.Angle()
    Main.compteur = (Main.compteur + 1)%2
    if Main.compteur == 0:
        Main.Go()

pyxel.run(draw, upt)