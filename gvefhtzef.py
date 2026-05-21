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
    "Cooldown" : 150,
    "MoveCooldown" : 12,
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

    # def DetermineDir(self):
    #     if self.DirX == 0 and self.DirY == 0:
    #         return 0
    #     elif self.DirX == 0 and self.DirY == 1:
    #         return 90
    #     elif self.DirX == -1 and self.DirY == -1:
    #         return 180
    #     elif self.DirX == -1 and self.DirY == 0:
    #         return 0

    def draw(self):
        Image : int = 0
        rotation = self.RotationOffset
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
        while newDirX == self.DirX or newDirY == self.DirY or newDirX == newDirY:
            newDirX = pyxel.rndi(-1, 1)
            newDirY = pyxel.rndi(-1 ,1)
        
        self.DirX = newDirX
        self.DirY = newDirY

class Game:
    def __init__(self):
        pyxel.init(256, 256, "Moi", 30)
        pyxel.rseed(45510)
        pyxel.load("U2.pyxres")
        self.Ennemi = Ennemy(EnnemyBase)
        pyxel.run(self.update, self.draw)
    
    def draw(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        pyxel.bltm(0, 0, 0, 0, 0, 256, 256)
        self.Ennemi.Draw()
    
    def update(self):
        self.Ennemi.Update()

Game()
    