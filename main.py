from mesa import Agent, Model
from mesa.space import Grid, MultiGrid
from mesa.time import RandomActivation

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from mesa.datacollection import DataCollector
from mesa.visualization.modules import ChartModule
from tornado.gen import sleep


class WallBlock(Agent):
    VALUE = 0
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.value = self.VALUE
    def step(self):
        pass
class EdgePoint(Agent):
    VALUE = 1
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.value = self.VALUE
    def step(self):
        pass
class CheckPoint(Agent):
    VALUE = 2
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.value = self.VALUE
    def step(self):
        pass

class Interseccion(Agent):

    VALUE = 3
    ORDEN_AUTOS = []

    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.value = self.VALUE
        self.ordenamiento = self.ORDEN_AUTOS
        self.evaluarEntorno()

    def evaluarEntorno(self):
        countCars = 0
        for neighbor in self.model.grid.get_neighbors(self.pos, moore=True):
            if neighbor.value == 4:
                countCars += 1
                if countCars > 1:
                    self.ordenamiento.append(neighbor)
                    #Agregar que no se repitan en la lista
                    Automovil.ORDEN += 1
                    Automovil.pos = neighbor.pos
                    #Aumentar el orden en el Agente de Automovil

    #Una vez realizado todo, esta función se encargará de hacer que los automoviles se muevan de acuerdo a su orden
    def aignacionDesplazamiento(self):
        for i in self.ordenamiento:
            Automovil.step()

class Automovil(Agent):
    VALUE = 4
    ORDEN = 0
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.value = self.VALUE
        self.orden = self.ORDEN
    def step(self):
        pass
class Sentido1(Agent):
    VALUE = 5
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.value = self.VALUE
    def step(self):
        pass
class Sentido2(Agent):
    VALUE = 6
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.value = self.VALUE
    def step(self):
        pass

class Vecindad(Model):
    def __init__(self):
        super().__init__()
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(36, 35, torus=False)
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
                checkP = CheckPoint(self, (x, y))
                self.grid.place_agent(checkP, checkP.pos)
                self.schedule.add(checkP)
                
    def step(self):
        self.schedule.step()
        

def agent_portrayal(agent):
    if type(agent) is WallBlock:
        return {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Color": "Gray", "Layer": 0}
    elif type(agent) is Automovil:
        return {"Shape": "automovil.png","Layer": 0}
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
server.port = 8521
server.launch()