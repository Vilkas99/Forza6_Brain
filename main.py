from mesa import Agent, Model
from mesa.space import Grid
from mesa.time import RandomActivation

from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from mesa.datacollection import DataCollector
from mesa.visualization.modules import ChartModule
from tornado.gen import sleep



class Vecindad(Model):
    def __init__(self):
        super().__init__()
        

def agent_portrayal(agent):
    if agent.condition == "Hello":
        portrayal = {"Shape": "circle", "Filled": "true", "Color": "Green", "r": 0.75, "Layer": 0}
    return portrayal

chart = ChartModule([{"Label": "Percent burned", "Color": "Black"}], data_collector_name='datacollector')
grid = CanvasGrid(agent_portrayal, 50, 50, 450, 450)
server = ModularServer(Vecindad,
                       [grid, chart],
                       "Forest",
                       {"density": UserSettableParameter("slider", "Tree density", 0.45, 0.01, 1.0, 0.01), 
                        "width":50, "height":50})

server.port = 8522 # The default
server.launch()