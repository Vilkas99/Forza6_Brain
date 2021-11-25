from mesa import Agent, Model
from mesa.space import Grid
from mesa.time import RandomActivation

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from mesa.datacollection import DataCollector
from mesa.visualization.modules import ChartModule
from tornado.gen import sleep


class Checkpoint(Agent):
    def __init__(self, unique_id: int, model: Model, x:int, y: int): 
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.siguiente = None 
    
    def step(self): 
        pass 


class Auto(Agent):
    def __init__(self, unique_id: int, model: Model, x : int, y : int, currentState  : str):
        super().__init__(unique_id, model)
        self.x = x
        self.y = y
        self.currentState = currentState
    
    def step(self):
        pass


class Vecindad(Model):
    def __init__(self):
        super().__init__()
        self.paso = 0
    
    def step(self):
        self.paso += 1

        

def agent_portrayal(agent):
    if agent.condition == "Hello":
        portrayal = {"Shape": "circle", "Filled": "true", "Color": "Green", "r": 0.75, "Layer": 0}
    return portrayal

chart = ChartModule([{"Label": "Percent burned", "Color": "Black"}], data_collector_name='datacollector')
grid = CanvasGrid(agent_portrayal, 50, 50, 450, 450)