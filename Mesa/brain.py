from mesa import Agent, Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from random import choice
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from mesa.datacollection import DataCollector
from mesa.visualization.modules import ChartModule
from tornado.gen import sleep
from .utils import AStar

import sys
sys.path.insert(0,'../Utils')

#Avance M5
class WallBlock(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.posicion_x = pos[0]
        self.posicion_y = pos[1]
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
    
    def step(self): 
        pass 

class Interseccion(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.posicion_x = pos[0]
        self.posicion_y = pos[1]
    def step(self):
        pass
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

        self.sentido = choice([1, 2])
        self.valor = None # Ayuda a la interseccion a decidir cuantos autos hay
        self.orientacion = None # Para calcular la rotación del auto


        self.currentState = currentState
    
    def step(self):
        
        if(self.posicion_x == self.destino_x and self.posicion_y == self.destino_y):
            self.completedDestination()
        else:
            self.setNextAction()
    
    def evaluateNearCars(self):
        # Revisar si no hay ningún auto en el lugar que toca visitar 
        for neighbor in self.model.grid.iter_neighbors((self.posicion_x, self.posicion_y), False):
            if neighbor.posicion_x == self.destino_tmp_x and neighbor.posicion_y == self.destino_tmp_y and type(neighbor) is Auto:
                # No puedo ocupar la posición que me correspondía.
                return False
        return True

    def setNextAction(self):
        self.movimientos = AStar(self.posicion_y, self.posicion_x, self.destino_y, self.destino_x, self.model.matrix) 
        if(len(self.movimientos) > 1):     
            self.destino_tmp_x =  self.movimientos[1][1]
            self.destino_tmp_y =  self.movimientos[1][0]
            
            if self.evaluateNearCars() and not self.detenido:
                self.posicion_x = self.destino_tmp_x
                self.posicion_y = self.destino_tmp_y
                self.model.grid.move_agent(self, (self.posicion_x, self.posicion_y))

        
            

    def completedDestination(self):
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)
    
class Sentido1(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.posicion_x = pos[0]
        self.posicion_y = pos[1]
    def step(self):
        pass
class Sentido2(Agent):
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.posicion_x = pos[0]
        self.posicion_y = pos[1]
    def step(self):
        pass

class Vecindad(Model):
    def __init__(self):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(36, 35, torus=False)

        self.origenYDestinos = {
            (13, 34) : [(35,18),(0,17),(21,0)],
            (35, 19) : [(14,34),(0,17),(21,0)],
            (22, 0)  : [(35,18),(0,17),(14,34)],
            (0 , 16) : [(35,18),(14,34),(21,0)],
        }
        self.paso = 0
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

        self.matrix = [
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,4,2,2,3,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,2,4,1,1,3,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,2,1,0,0,0,0,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,4,1,3,3,3,3,1,1,4,1,3,3,3,3,1,4,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,1,4,2,3,3,3,3,2,2,4,2,3,3,3,3,2,4,1,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,1,2,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,2,1,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,1,2,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,2,1,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 4,4,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,4,4, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 3,3,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,2,1, 0,0,0,0,0,0],
            [1,1,1,4,1,3, 3,3,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,2,1, 0,0,0,0,0,0],
            [2,2,2,4,2,3, 3,3,0,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,0,3,3, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 3,3,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,3,3, 3,1,4,1,1,1],
            [0,0,0,0,0,0, 2,1,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,3,3, 3,2,4,2,2,2],
            [0,0,0,0,0,0, 4,4,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,3,3, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,2,1,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,4,4,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,2,1,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,1,2,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,2,4,1,3,3,3,3,1,1,4,1,3,3,3,3,1,4,2,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,4,2,3,3,3,3,2,2,4,2,3,3,3,3,2,4,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,2,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,3,2,2,4,1,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,3,1,1,4,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
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
            elif self.matrix[y][x] == 3:
                interSecc = Interseccion(self, (x, y))
                self.grid.place_agent(interSecc, interSecc.pos)
                self.schedule.add(interSecc)
            elif self.matrix[y][x] == 4:
                checkP = CheckPoint(self, (x, y), "1")
                self.grid.place_agent(checkP, checkP.pos)
                self.schedule.add(checkP)
        carrito = Auto(self.next_id(), self, "1")
        self.grid.place_agent(carrito, (carrito.posicion_x, carrito.posicion_y))
        self.schedule.add(carrito)



                
    def step(self):
        self.paso += 1
        self.schedule.step()
        if self.paso % 5 == 0:
            carrito = Auto(self.next_id(), self, "1")
            self.grid.place_agent(carrito, (carrito.posicion_x, carrito.posicion_y))
            self.schedule.add(carrito)

        

def agent_portrayal(agent):
    if type(agent) is WallBlock:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 0}
    elif type(agent) is Auto:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Yellow", "Layer": 0}
    elif type(agent) is Sentido1:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Black", "Layer": 0}
    elif type(agent) is EdgePoint:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "#101010", "Layer": 0}
    elif type(agent) is EdgePoint:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Green", "Layer": 0}
    elif type(agent) is CheckPoint:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "#000055", "Layer": 0}
    elif type(agent) is Interseccion:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "#550055", "Layer": 0}



grid = CanvasGrid(agent_portrayal, 36, 35, 400, 400)

server = ModularServer(Vecindad, [grid], "Reto_Equipo2", {})
server.port = 8522
server.launch()