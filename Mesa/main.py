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
        
        self.posicion_x = x
        self.posicion_y = y
        self.destino_x = choice(self.model.destinations)[0]
        self.destino_y = choice(self.model.destinations)[1]
        self.destino_tmp_x = self.destino_x
        self.destino_tmp_y = self.destino_y


        self.currentState = currentState
    
    def step(self):
        pass
    
    def evaluateNearCars(self):
        for neighbor in self.model.space.get_neighbors(self.pos,1):
            pass
            

    def setNextAction(self):
        
        #astar
        movimientos = AStar(self.posicion_x, self.posicion_y, self.destino_x, self.destino_y, self.model.matrix)
        
        #llamar a  evaluateNearCars
        
        
        

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