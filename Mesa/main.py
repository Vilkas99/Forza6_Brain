from mesa import Agent, Model
from mesa.space import Grid
from mesa.time import RandomActivation

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from Utils.index import AStar
from random import choice as choice

from mesa.datacollection import DataCollector
from mesa.visualization.modules import ChartModule
from tornado.gen import sleep


class Checkpoint(Agent):
    def __init__(self, unique_id: int, model: Model, x:int, y: int, caminoID: str): 
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.caminoID = caminoID
        self.siguiente = None 
    
    def step(self): 
        pass 


class Auto(Agent):
    def __init__(self, unique_id: int, model: Model, x : int, y : int, currentState  : str):
        super().__init__(unique_id, model)
        
        destinos = self.model.destinations
        destino = choice(destinos)
        self.destino_x = destino[0]
        self.destino_y = destino[1]
        self.destino_tmp_x = self.destino_x
        self.destino_tmp_y = self.destino_y

        destinos.remove(destino)
        origen = choice(destinos)
        self.posicion_x = origen[0]
        self.posicion_y = origen[1]

        self.detenido = False #Para ver si la intersección permite que el auto avance en este momento

        self.sentido = choice([1, 2]);

        #TODO: mover esto a set next action si después surge la necesidad de recalcular rutas
        self.movimientos = AStar(self.posicion_x, self.posicion_y, self.destino_x, self.destino_y, self.model.matrix)

        self.currentState = currentState
    
    def step(self):
        setNextAction()
    
    def evaluateNearCars(self):
        # Revisar si no hay ningún auto en el lugar que toca visitar 
        for neighbor in self.model.space.get_neighbors((self.posicion_x, self.posicion_y), False):
            if neighbor.posicion_x == self.destino_tmp_x and neighbor.posicion_y == self.destino_tmp_y:
                # No puedo ocupar la posición que me correspondía.
                return False
        return True

    def setNextAction(self):
        
        #astar
        
        self.destino_tmp_x =  movimientos[0][0]
        self.destino_tmp_y =  movimientos[0][1]
        
        if not evaluateNearCars() and not self.detenido:
            self.posicion_x = self.destino_tmp_x
            self.posicion_y = self.destino_tmp_y
            

    def completedDestination(self):
        self.model.grid.remove_agent(self)


class Vecindad(Model):
    def __init__(self):
        super().__init__()
        self.paso = 0
        self.destinos = [(22, 0), (0, 15), (14, 33), (33, 17)]
        
    
    def step(self):
        self.paso += 1

        

def agent_portrayal(agent):
    if agent.condition == "Hello":
        portrayal = {"Shape": "circle", "Filled": "true", "Color": "Green", "r": 0.75, "Layer": 0}
    return portrayal

chart = ChartModule([{"Label": "Percent burned", "Color": "Black"}], data_collector_name='datacollector')
grid = CanvasGrid(agent_portrayal, 50, 50, 450, 450)