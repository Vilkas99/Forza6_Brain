from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import BaseScheduler, RandomActivation

from random import choice
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from mesa.datacollection import DataCollector
from mesa.visualization.modules import ChartModule
from tornado.gen import sleep
from .utils import AStar


#Avance M5
class WallBlock(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.posicion_x = pos[0]
        self.posicion_y = pos[1]
        self.valor = 0
    def step(self):
        pass
class EdgePoint(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.posicion_x = pos[0]
        self.posicion_y = pos[1]
    def step(self):
        pass
    
class CheckPoint(Agent):
    def __init__(self, model: Model, pos, caminoID: str): 
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.posicion_x = pos[0]
        self.posicion_y = pos[1]
        self.caminoID = caminoID
        self.siguiente = None 
        self.valor = 4
    def step(self): 
        pass 

    
    def step(self): 
        pass 

class InterCell(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.valor = 3

class Interseccion(Agent):
    def __init__(self, model, pos, tipo):
        super().__init__(model.next_id(), model)
        self.blockOfPos = pos
        self.valor = 3
        self.autoEspera = []
        self.tipo = tipo
        self.stillFindFirst = False
    def evaluarEntorno(self):
        countCars = 0
        for i in self.blockOfPos:
            for neighbor in self.model.grid.iter_neighbors(i, moore=False):    
                if neighbor.valor == 5 and neighbor not in self.autoEspera: #Si el valor es 4 significa que es un Agente Automovilistico :O
                    countCars += 1 #Cuando se detectan más de un auto
                    self.autoEspera.append(neighbor)
                    if countCars == 1:
                        self.stillFindFirst = True
                    neighbor.detenido = True
                    if neighbor.posicion_x == i[0] and neighbor.posicion_y != i[1]: #SIGNIFICA QUE ES VERTICAL --> Valor de 1
                        neighbor.orientacion = 1 #Significa que viene de una calle en vertical

                    elif neighbor.posicion_x != i[0] and neighbor.posicion_y == i[1]: #SIGNIFICA QUE ES HORIZONTAL --> Valor de 2
                        neighbor.orientacion = 2 #Significa que viene de una calle en horizontal
                    
                elif neighbor.valor == 5 and neighbor in self.autoEspera:
                    if neighbor == self.autoEspera[0]:
                        self.stillFindFirst = True


    def cambiarSentido(self, valor):
        if valor == 1:
            return 2
        return 1

    def asignacionDesplazamiento(self):
                # Reglas para crucero de 4 caminos:
                    # 1.- Si el carro se encuentra la interseccion desde la parte vertical
                    #   Seguir derecho O doblar hacia la derecha del carro -> mantiene el sentido 
                    #   Doblar hacia la izquierda del carro -> cambia el sentido
                    # 2.- Si el carro se encuentra la interseccion desde la parte horizontal
                    #   Seguir derecho O doblar hacia la izquierda del carro -> mantiene el sentido 
                    #   Doblar hacia la derecha del carro -> cambia el sentido

                    #Reglas para crucero 3 caminos (calles laterales):
                    # 1.- Si el carro no cuenta con calle si quisiera seguir derecho
                    #   Doblar hacia cualquier lado -> mantiene el sentido
                    # 2.- Si el carro puede seguir derecho porque cuenta con calle para hacerlo
                    #   Seguirse derecho -> cambia el sentido
                    #   Doblar -> mantiene el sentido

                    #Reglas para crucero 3 caminos (calles verticales):
                    # 1.- Si el carro no cuenta con calle si quisiera seguir derecho
                    #   Doblar hacia la derecha del carro -> mantiene el sentido
                    #   Doblar hacia la izquierda del carro -> cambia el sentido 
                    # 2.- Si el carro puede seguir derecho porque cuenta con calle para hacerlo
                    #   Seguirse derecho -> mantiene el sentido
                    #   Doblar -> cambia el sentido

        i = self.autoEspera[0]
        i.detenido = False
        if self.tipo == "4Cam":
            if i.camino != "F":
            #2 blanco 1 negro
                if i.orientacion == 1: #Significa que es Vertical
                    if abs(i.posicion_y - i.next_checkpoint[1]) == 1 and abs(i.posicion_x - i.next_checkpoint[0]) == 3:
                        i.sentido = self.cambiarSentido(i.sentido) #Cambiarlo
                elif i.orientacion == 2: #Significa que es horizontal
                    if abs(i.posicion_x - i.next_checkpoint[0]) == 0 and abs(i.posicion_y - i.next_checkpoint[1]) == 2:
                        if i.camino != "G":
                            i.sentido = self.cambiarSentido(i.sentido) #SE CAMBIA

        elif self.tipo == "Vertical":
            #2 blanco 1 negro
            if i.orientacion == 1: #Significa que es Vertical
                if abs(i.posicion_y - i.next_checkpoint[1]) == 0 and abs(i.posicion_x - i.next_checkpoint[0]) == 2:
                    if i.camino != "L":
                        i.sentido = self.cambiarSentido(i.sentido) #Se cambia
            elif i.orientacion == 2: #Significa que es horizontal
                if abs(i.posicion_y - i.next_checkpoint[1]) == 1 and abs(i.posicion_x - i.next_checkpoint[0]) == 3:
                    i.sentido = self.cambiarSentido(i.sentido) #SE CAMBIA

        elif self.tipo == "Hori":
            #2 blanco 1 negro
            if i.orientacion == 1: #Significa que es Vertical
                if abs(i.posicion_y - i.next_checkpoint[1]) == 3 and abs(i.posicion_x - i.next_checkpoint[0]) == 0:
                    i.sentido = self.cambiarSentido(i.sentido) #Se cambia
            elif i.orientacion == 2: #Significa que es horizontal
                    i.sentido #Se mantiene


    def step(self):
        
        self.stillFindFirst = False
        self.evaluarEntorno()
        if self.stillFindFirst == False and self.autoEspera:
            self.autoEspera.pop(0)
        if self.autoEspera:
            self.asignacionDesplazamiento()


class Auto(Agent):
    def __init__(self, unique_id, model, currentState):
        super().__init__(unique_id, model)
        self.model = model
        origen = choice(list(self.model.origenYDestinos))
        self.posicion_x = origen[0]
        self.posicion_y = origen[1]
        destino = choice(self.model.origenYDestinos[origen])
        self.destino_x = destino[0]
        self.destino_y = destino[1]
        self.destino_tmp_x = self.destino_x
        self.destino_tmp_y = self.destino_y
        self.detenido = False #Para ver si la intersección permite que el auto avance en este momento
        self.finalizo = False
        self.sentido = 2
        if self.posicion_x == 22 or self.posicion_y == 16:
            self.sentido = 1
        self.valor = 5 # Ayuda a la interseccion a decidir cuantos autos hay
        self.valor = 5 # Ayuda a la interseccion a decidir cuantos autos hay
        self.orientacion = None # Para calcular la rotación del auto
        self.camino = self.setCamino()
        self.currentCheckpoint = 0
        self.next_checkpoint = self.findCheckpoint()
        self.rotacion = 0

        self.currentState = currentState
    
    def step(self):
        
        print("Auto: " + str(self.unique_id) + ": " + str(self.posicion_x) + "," + str(self.posicion_y))
        
        if(self.posicion_x == self.destino_x and self.posicion_y == self.destino_y):
            self.completedDestination()
            self.finalizo = True
        else:
            self.setNextAction()
    
    def evaluateNearCars(self):
        # Revisar si no hay ningún auto en el lugar que toca visitar 
        for neighbor in self.model.grid.iter_neighbors((self.posicion_x, self.posicion_y), False):
            if type(neighbor) is Auto:
                if neighbor.posicion_x == self.destino_tmp_x and neighbor.posicion_y == self.destino_tmp_y:
                    # No puedo ocupar la posición que me correspondía.
                    return False
        return True
    
    def findCheckpoint(self): 
        direcciones = [(0,1), (1,0), (-1,0), (0,-1)]
        queue = [(self.posicion_x, self.posicion_y)]
        dp = []
        
        while queue: 
            posPorChecar = queue.pop()
            if (self.currentCheckpoint == len(self.model.mapOfPaths[self.camino])):
                return None
            if posPorChecar == self.model.mapOfPaths[self.camino][self.currentCheckpoint]:
                self.currentCheckpoint += 1
                return posPorChecar
            
            if posPorChecar in dp: 
                continue
            
            for direccion in direcciones: 
                nuevoRow = posPorChecar[0] + direccion[0]
                nuevoCol = posPorChecar[1] + direccion[1]
                    
                dentroX = nuevoRow >= 0 and nuevoRow < len(self.model.matrix)
                dentroY = nuevoCol >= 0 and nuevoCol < len(self.model.matrix[0])
                    
                if dentroX and dentroY: 
                    nuevoPos = (nuevoCol, nuevoRow)
                    queue.append(nuevoPos)
                
            dp.append(posPorChecar)
        
        return None

    def setCamino(self):
        
        if (self.posicion_x, self.posicion_y) == (13, 34):
            if (self.destino_x, self.destino_y) == (35, 18):
                return "L"
            if (self.destino_x, self.destino_y) == (0, 17):
                return "K"
            else:
                return "J"

        if (self.posicion_x, self.posicion_y) == (35, 19):
            if (self.destino_x, self.destino_y) == (14, 34):
                return "I"
            if (self.destino_x, self.destino_y) == (0, 17):
                return "H"
            else:
                return "G"

        if (self.posicion_x, self.posicion_y) == (22, 0):
            if (self.destino_x, self.destino_y) == (35, 18):
                return "A"
            if (self.destino_x, self.destino_y) == (0, 17):
                return "C"
            else:
                return "B"

        if (self.posicion_x, self.posicion_y) == (0, 16):
            if (self.destino_x, self.destino_y) == (35, 18):
                return "D"
            if (self.destino_x, self.destino_y) == (14, 34):
                return "F"
            else:
                return "E"

        return ""
                
        

    def setNextAction(self):
        if (self.posicion_x, self.posicion_y) == self.next_checkpoint:
            self.next_checkpoint = self.findCheckpoint()

        if self.next_checkpoint is None:
            self.next_checkpoint = (self.destino_x, self.destino_y)
        self.movimientos = AStar(self.posicion_y, self.posicion_x, self.next_checkpoint[1], self.next_checkpoint[0], self.model.matrix, self.sentido)       
        if(len(self.movimientos) > 1):     
            self.destino_tmp_x =  self.movimientos[1][1]
            self.destino_tmp_y =  self.movimientos[1][0]
            self.setRotacion()
            if self.evaluateNearCars() and not self.detenido:
                self.posicion_x = self.destino_tmp_x
                self.posicion_y = self.destino_tmp_y
                self.model.grid.move_agent(self, (self.posicion_x, self.posicion_y))

    def completedDestination(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

    def setRotacion(self):
        if self.posicion_x < self.destino_tmp_x:
            self.rotacion = 0

        elif self.posicion_x > self.destino_tmp_x:
            self.rotacion = 180

        elif self.posicion_y < self.destino_tmp_y:
            self.rotacion = 90

        elif self.posicion_y > self.destino_tmp_y:
            self.rotacion = 270

        else:
            self.rotacion = 0

    
class Sentido1(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.posicion_x = pos[0]
        self.posicion_y = pos[1]
        self.valor = 1
    def step(self):
        pass
class Sentido2(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.posicion_x = pos[0]
        self.posicion_y = pos[1]
        self.valor = 2
    def step(self):
        pass

class Vecindad(Model):
    def __init__(self):
        super().__init__()
        self.schedule = BaseScheduler(self)
        self.grid = MultiGrid(36, 35, torus=False)
        
        self.autos = []

        self.origenYDestinos = {
            (13, 34) : [(35,18),(0,17),(21,0)],
            (35, 19) : [(14,34),(0,17),(21,0)],
            (22, 0)  : [(35,18),(0,17),(14,34)],
            (0 , 16) : [(35,18),(14,34),(21,0)],
        }
        self.paso = 0

        self.interseccionLateral = [[(6,16),(6,17),(7,16),(7,17)],[(29,18),(28,18),(29,19),(28,19)]]
        self.interseccionCuatro = [[(13,10),(14,10),(13,11),(14,11)],[(13,23),(14,23),(13,24),(14,24)],[(21,10),(22,10),(21,11),(22,11)],[(21,23),(22,23),(21,24),(22,24)]]
        self.interseccionVertical = [[(22,3),(21,3),(22,4),(21,4)],[(13,31),(14,31),(13,30),(14,30)]]


        self.matrix = [
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,2,2,2,2,2,4,2,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,1,1,1,1,4,1,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 1,1,1,1,1,4,1,3,3,1,4,1,1,4,1,3,3,1,4,1,1,1,1,1, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 1,2,2,2,2,4,2,3,3,2,4,2,2,4,2,3,3,2,4,2,2,2,2,1, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 1,2,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,2,1, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 1,2,0,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,0,2,1, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 4,4,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,2,1, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 1,2,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,2,1, 0,0,0,0,0,0],
            [1,1,1,1,4,1, 3,3,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,4,4, 0,0,0,0,0,0],
            [2,2,2,2,4,2, 3,3,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,2,1, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 2,1,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,3,3, 1,4,1,1,1,1],
            [0,0,0,0,0,0, 4,4,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,3,3, 2,4,2,2,2,2],
            [0,0,0,0,0,0, 2,1,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,1,2, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 2,1,0,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,0,4,4, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 2,1,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,1,2, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 2,1,1,1,1,4,1,3,3,1,4,1,1,4,1,3,3,1,4,1,1,1,1,2, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 2,2,2,2,2,4,2,3,3,2,4,2,2,4,2,3,3,2,4,2,2,2,2,2, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,2,4,2,2,2,2,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,1,4,1,1,1,1,1,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
        ]
        for _,x,y in self.grid.coord_iter():
            if self.matrix[y][x] == 0:
                block = WallBlock(self, (x, y))
                self.grid.place_agent(block, block.pos)
                self.schedule.add(block)
            elif self.matrix[y][x] == 1:
                block = Sentido1(self, (x, y))
                self.grid.place_agent(block, block.pos)
                self.schedule.add(block)
            elif self.matrix[y][x] == 2:
                block = Sentido2(self, (x, y))
                self.grid.place_agent(block, block.pos)
                self.schedule.add(block)
            elif self.matrix[y][x] == 4:
                checkP = CheckPoint(self, (x, y), "1")
                self.grid.place_agent(checkP, checkP.pos)
                self.schedule.add(checkP)
        
        for i in self.interseccionLateral:
            inter = Interseccion(self, i, "Hori")
            for j in i:
                miniCell = InterCell(self, j)
                self.grid.place_agent(miniCell, miniCell.pos)
            self.schedule.add(inter)

        for i in self.interseccionVertical:
            inter = Interseccion(self, i, "Vertical")
            for j in i:
                miniCell = InterCell(self, j)
                self.grid.place_agent(miniCell, miniCell.pos)
            self.schedule.add(inter)

        for i in self.interseccionCuatro:
            inter = Interseccion(self, i, "4Cam")
            for j in i:
                miniCell = InterCell(self, j)
                self.grid.place_agent(miniCell, miniCell.pos)
            self.schedule.add(inter)

        self.mapOfPaths = {
            "A" : [(22,1),(22,6),(22,8),(24,10),(29,16),(31,18)],
            "B" : [(22,1),(22,6),(22,8),(22,13),(22,21),(22,26),(16,31),(14,33)], #Defectuoso
            "C" : [(22,1),(22,6),(22,8),(19,11), (16,11), (11,11), (7,14), (4,17)],
            
            "D" : [(4,16),(7,19),(11,23),(16,23),(19,23),(24,23),(28,21),(31,18)],
            "E" : [(4,16),(6,14),(11,10),(13,8),(19,3),(21,1)], 
            "F" : [(4,16),(7,19),(11,23),(14,26),(14,28),(14,33)],
            
            "G" : [(31,19),(28,16),(24,11),(21,8),(21,6),(21,1)],
            "H" : [(31,19),(29,21),(24,24),(19,24),(16,24),(11,24),(6,19),(4,17)],
            "I" : [(31,19),(29,21),(24,24),(22,26),(16,31),(14,33)],
            
            "J" : [(13,33),(13,28),(13,26),(13,21),(13,13),(13,8),(19,3), (21,1)],
            "K" : [(13,33),(13,28),(13,26),(11,24),(6,19),(4,17)],
            "L" : [(13,33),(16,30),(21,26),(24,23),(28,21),(31,18)] 
        }

        carrito = Auto(self.next_id(), self, "1")
        self.grid.place_agent(carrito, (carrito.posicion_x, carrito.posicion_y))
        self.schedule.add(carrito)
        self.autos.append(carrito)



                
    def step(self):
        self.paso += 1
        self.schedule.step()
        if self.paso % 12 == 0:
            carrito = Auto(self.next_id(), self, "1")
            self.grid.place_agent(carrito, (carrito.posicion_x, carrito.posicion_y))
            self.schedule.add(carrito)
            self.autos.append(carrito)
    
    def updateInfo(self):
        data = []
        for auto in self.autos: 
            newDataAuto = {'posX': auto.posicion_x, 'posY': auto.posicion_y, 'finalizo': auto.finalizo, "angulo": auto.rotacion}
            data.append(newDataAuto)
        
        return  {'coches': data}
            

        

def agent_portrayal(agent):
    if type(agent) is WallBlock:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 0}
    elif type(agent) is Auto:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Green", "Layer": 0}
    elif type(agent) is Sentido1:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Black", "Layer": 0}
    elif type(agent) is EdgePoint:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "#101010", "Layer": 0}
    elif type(agent) is EdgePoint:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Green", "Layer": 0}
    elif type(agent) is CheckPoint:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "#000055", "Layer": 0}
    elif type(agent) is InterCell:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "#550055", "Layer": 0}



#grid = CanvasGrid(agent_portrayal, 36, 35, 400, 400)

#server = ModularServer(Vecindad, [grid], "Reto_Equipo2", {})
#server.port = 8522
#server.launch()