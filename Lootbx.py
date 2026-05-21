import pyxel
from random import randint

class elements_obtenable:
    def __init__(self, nombre, boosts):
        self.nombre = []
        self.boosts = []
        self.tmp = pyxel.frame_count
    def update(self):
        if len(self.nombre) == 0:
            self.nombre.append(chest(randint(0,242), randint(0,242), randint(0,2), 2))
        for elem in self.nombre:
            elem.update() 
            elem.mort(self.nombre, self.boosts)  
        for truc in self.boosts:
            truc.mort(self.tmp, self.boosts)
        print(self.boosts)
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
        pyxel.load("U2.pyxres")
        self.boite = elements_obtenable(0, 0)
        pyxel.run(self.update, self.draw)

    def update(self):
        self.boite.update()

    def draw(self):
        pyxel.cls(4)
        self.boite.draw()
        

game()