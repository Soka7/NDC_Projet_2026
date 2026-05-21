import pyxel

BulletBase : dict = {
    "AtlasX" : 0,
    "AtlasY" : 128,
    "AtlasWidth" : 16,
    "AtlasHeight" : 16,
    "RotationOffset" : 90,
    "Speed" : 1,
    "Lifetime" : 180,
    "Damage" : 1,
    "Angle" : 0
}

EnnemyBase : dict = {
    "PosX" : 128,
    "PosY" : 128,
    "AtlasX" : 96,
    "AtlasY" : 128,
    "AtlasWidth" : 16,
    "AtlasHeight" : 16,
    "Health" : 5,
    "Speed" : 0.5,
    "Angle" : 0,
    "Cooldown" : 150,
    "BulletData" : BulletBase
}

class Bullet:
    def __init__(self, Data : dict, CurrentFrame : int, PosX : int, PosY : int):
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
        self.Angle = Data["Angle"]
        self.SpawnedAtFrame = CurrentFrame

    def update(self):
        self.PosX += self.Speed * pyxel.cos(self.Angle)
        self.PosY += self.Speed * pyxel.sin(self.Angle)

    def checkDead(self):
        if pyxel.frame_count >= self.SpawnedAtFrame + self.Lifetime:
            return True
        return False

    def draw(self):
        Image : int = 0
        pyxel.blt(self.PosX, self.PosY, Image, self.AtlasX, self.AtlasY, self.AtlasWidth, self.AtlasHeight, pyxel.COLOR_BROWN, rotate = (self.Angle + self.RotationOffset))


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
        self.BulletData = Data["BulletData"]
        self.Angle = Data["Angle"]
        self.Shootlist = []

    def Move(self):
        self.PosX += self.Speed * pyxel.cos(self.Angle)
        self.PosY += self.Speed * pyxel.sin(self.Angle)

    def Update(self):
        if self.CheckCollisions():
            self.HandleCollisions()
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
            self.Shootlist.append(Bullet(self.BulletData, pyxel.frame_count, self.PosX, self.PosY))

    def DeleteBullets(self):
        ToRemove = []
        for i in range(0, len(self.Shootlist)):
            if self.Shootlist[i].checkDead():
                ToRemove.append(i)
        
        for i in range(len(ToRemove) - 1, -1, -1):
            self.Shootlist.pop(ToRemove[i])

    def CheckCollisions(self):
        for i in range(int(self.PosX), int(self.PosX + self.AtlasWidth)):
            if pyxel.pget(i, self.PosY - 1) != 0 or pyxel.pget(i, self.PosY + self.AtlasHeight + 1) != 0:
                return True
        
        for i in range(int(self.PosY), int(self.PosY + self.AtlasHeight)):
            if pyxel.pget(self.PosX - 1, i) != 0 or pyxel.pget(self.PosX + self.AtlasWidth + 1, i) != 0:
                return True
        return False

    def HandleCollisions(self):
        self.Angle = pyxel.rndi(self.Angle + 45, self.Angle + 315)
        self.Angle %= 360

        

class EnnemyManager:
    def __init__(self):
        self.EnnemyList = []
    
    def update(self):
        for i in self.EnnemyList:
            i.Update()
    
    def draw(self):
        for i in self.EnnemyList:
            i.Draw()

class Game:
    def __init__(self):
        pyxel.init(256, 256, "Moi", 60)
        pyxel.rseed(45510)
        pyxel.load("U2 (1).pyxres")
        self.Ennemi = Ennemy(EnnemyBase)
        pyxel.run(self.update, self.draw)
    
    def draw(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        pyxel.bltm(0, 0, 0, 0, 0, 256, 256)
        self.Ennemi.Draw()
    
    def update(self):
        self.Ennemi.Update()

Game()
    