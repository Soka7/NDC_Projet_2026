import pyxel
from random import randint
from pyxel import *
from math import degrees, atan2

BulletBase : dict = {
    "AtlasX" : 0,
    "AtlasY" : 128,
    "AtlasWidth" : 16,
    "AtlasHeight" : 16,
    "RotationOffset" : 90,
    "Speed" : 1,
    "Lifetime" : 180,
    "Damage" : 1,
}

EnnemyBase : dict = {
    "PosX" : 64,
    "PosY" : 64,
    "AtlasX" : 96,
    "AtlasY" : 128,
    "AtlasWidth" : 16,
    "AtlasHeight" : 16,
    "Health" : 5,
    "Speed" : 16,
    "Cooldown" : 75,
    "MoveCooldown" : 30,
    "BulletData" : BulletBase
}

class Bullet:
    def __init__(self, Data : dict, CurrentFrame : int, PosX : int, PosY : int, DirX : int, DirY : int):
        self.PosX = PosX
        self.PosY = PosY
        self.AtlasX = Data["AtlasX"]
        self.AtlasY = Data["AtlasY"]
        self.AtlasWidth = Data["AtlasWidth"]
        self.AtlasHeight = Data["AtlasHeight"]
        self.RotationOffset = Data["RotationOffset"]
        self.Speed = Data["Speed"]
        self.Lifetime = Data["Lifetime"]
        self.Damage = Data["Damage"]
        self.SpawnedAtFrame = CurrentFrame
        self.DirX = DirX
        self.DirY = DirY

    def update(self):
        self.PosX += self.Speed * self.DirX
        self.PosY += self.Speed * self.DirY

    def checkDead(self):
        if pyxel.frame_count >= self.SpawnedAtFrame + self.Lifetime:
            return True
        return False

    def DetermineDir(self):
        if self.DirX == 0 and self.DirY == 0:
            return 0
        elif self.DirX == 0 and self.DirY == 1:
            return 90
        elif self.DirX == 0 and self.DirY == -1:
            return 270
        elif self.DirX == -1 and self.DirY == 0:
            return 180
        elif self.DirX == -1 and self.DirY == 1:
            return 225
        elif self.DirX == -1 and self.DirY == -1:
            return 135
        elif self.DirX == 1 and self.DirY == 0:
            return 0
        elif self.DirX == 1 and self.DirY == -1:
            return 45
        elif self.DirX == 1 and self.DirY == 1:
            return 315

    def draw(self):
        Image : int = 0
        rotation = self.RotationOffset + self.DetermineDir()
        pyxel.blt(self.PosX, self.PosY, Image, self.AtlasX, self.AtlasY, self.AtlasWidth, self.AtlasHeight, pyxel.COLOR_BROWN, rotate = (rotation))


class Ennemy:
    def __init__(self, Data : dict):
        self.PosX = Data["PosX"]
        self.PosY = Data["PosY"]
        self.AtlasX = Data["AtlasX"]
        self.AtlasY = Data["AtlasY"]
        self.AtlasWidth = Data["AtlasWidth"]
        self.AtlasHeight = Data["AtlasHeight"]
        self.Health = Data["Health"]
        self.Speed = Data["Speed"]
        self.Cooldown = Data["Cooldown"]
        self.Movecooldown = Data["MoveCooldown"]
        self.BulletData = Data["BulletData"]
        self.Shootlist = []
        self.DirX = 1
        self.DirY = 0

    def Move(self):
        self.PosX += self.Speed * self.DirX
        self.PosY += self.Speed * self.DirY

    def Update(self):
        if self.CheckCollisions():
            self.HandleCollisions()
        if pyxel.frame_count % self.Movecooldown == 0:
            self.Move()
        self.Shoot()
        for i in self.Shootlist:
            i.update()
        self.DeleteBullets()

    def Draw(self):
        Image : int = 0
        pyxel.blt(self.PosX, self.PosY, Image, self.AtlasX, self.AtlasY, self.AtlasWidth, self.AtlasHeight, pyxel.COLOR_BROWN)
        for i in self.Shootlist:
            i.draw()

    def Shoot(self):
        if pyxel.frame_count % self.Cooldown == 0:
            self.Shootlist.append(Bullet(self.BulletData, pyxel.frame_count, self.PosX, self.PosY, self.DirX, self.DirY))

    def DeleteBullets(self):
        ToRemove = []
        for i in range(0, len(self.Shootlist)):
            if self.Shootlist[i].checkDead():
                ToRemove.append(i)
        
        for i in range(len(ToRemove) - 1, -1, -1):
            self.Shootlist.pop(ToRemove[i])

    def CheckCollisions(self):
        if pyxel.pget(self.PosX + self.Speed * self.DirX, self.PosY + self.Speed * self.DirY) != 0 or \
            self.PosX + self.Speed * self.DirX <= 0 or self.PosY + self.Speed * self.DirY <= 0 or\
            self.PosX + self.Speed * self.DirX >= 256 or self.PosY + self.Speed * self.DirY >= 256:
            print("detected")
            return True
        return False

    def HandleCollisions(self):
        newDirX = pyxel.rndi(-1, 1)
        newDirY = pyxel.rndi(-1, 1)
        while newDirX == self.DirX or newDirY == self.DirY or newDirX == newDirY or (newDirX != 0 and newDirY != 0) or (newDirY != 0 and newDirX != 0):
            newDirX = pyxel.rndi(-1, 1)
            newDirY = pyxel.rndi(-1 ,1)
        
        self.DirX = newDirX
        self.DirY = newDirY


class Perso:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.Rotation = None
        self.compteur = 0
        self.dgts = 1
        
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
        
    def IfDgts(self, Ennemy):
        Ennemy.rotation = degrees(atan2(self.y - Ennemy.PosX, self.x - Ennemy.PosX))
        if self.Rotation == Ennemy.rotation and ((Ennemy.PosX - self.x)**2 + (Ennemy.PosY - self.y)**2) <= 8**2:
            "Une fonction fait degats"
        


class elements_obtenable:
    def __init__(self, nombre, boosts):
        self.nombre = []
        self.boosts = []
        self.tmp = pyxel.frame_count
    def update(self):
        if len(self.nombre) == 0:
            self.nombre.append(chest(randint(0,242), randint(0,242), randint(0,2), 2))
        for elem in self.nombre:
             
            elem.mort(self.nombre, self.boosts)  
        for truc in self.boosts:
            truc.mort(self.tmp, self.boosts)
    def degat(self):
        for elem in self.nombre:
            elem.update()  

    def draw(self):
        for elem in self.nombre:
            elem.draw()
        for truc in self.boosts:
            truc.draw()


class chest(elements_obtenable):
        def __init__(self, x, y, objet, health):
            elements_obtenable.__init__(self, 0, 0)
            self.x = x
            self.y = y
            self.obj = objet
            self.health = health
        def update(self):
            if pyxel.btn(pyxel.KEY_F):
                self.health -= 1
        def mort(self, liste, nv):
            if self.health <= 0:
                liste.pop(0)
                nv.append(boost(self.x,self.y,self.obj))
        def draw(self):
            pyxel.blt(self.x, self.y, 0, 96, 96, 32, 32, 4)
        


class boost(elements_obtenable):
        def __init__(self, x, y, boost):
            elements_obtenable.__init__(self, 0, 0)
            self.x = x
            self.y = y
            self.boost = boost
            self.pv = 1            
        def mort(self, tmp, nv):
            if abs(self.tmp - pyxel.frame_count) >= 300:
                nv.pop(0)
        def draw(self):
            if self.boost == 0:
                pyxel.blt(self.x, self.y, 0, 0, 160, 16, 16, 4)
            elif self.boost == 1:
                pyxel.blt(self.x, self.y, 0, 16, 160, 16, 16, 4)
            else:
                pyxel.blt(self.x, self.y, 0, 32, 160, 16, 16, 4)



class game:
    def __init__(self):
        pyxel.init(256,256,"hell yeah", 60)
        pyxel.rseed(45510)
        pyxel.load("U2.pyxres")
        self.Ennemi = Ennemy(EnnemyBase)
        self.boite = elements_obtenable(0, 0)
        self.Main = Perso(16, 16)
        pyxel.run(self.update, self.draw)
        

    def update(self):
        self.boite.update()
        self.Main.Angle()
        self.Main.compteur = (self.Main.compteur + 1)%8
        self.Ennemi.Update()
        if self.Main.compteur == 0:
            self.Main.Go()

    def draw(self):
        pyxel.cls(4)
        pyxel.mouse(True)
        self.Main.Draw()
        self.boite.draw()
        self.Ennemi.Draw()
        self.Main.Zone()
        
        
        

game()