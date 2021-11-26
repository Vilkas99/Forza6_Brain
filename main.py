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
    AUTOSV = []
    AUTOSL = []
    AUTOS4 = []

    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos

        self.posicionesL = self.model.interseccionLateral
        self.posicionesV = self.model.interseccionVertical
        self.posiciones4 = self.model.interseccionCuatro

        self.value = self.VALUE
        self.ordenamientoV = self.AUTOSV
        self.ordenamientoL = self.AUTOSL
        self.ordenamiento4 = self.AUTOS4
        self.evaluarEntorno()

    def evaluarEntorno(self):
        countCars = 0
        
        # ||||||||||||||||| EVALUA LAS INTERSECCIONES LATERALES ||||||||||||||||||||||

        for i in self.posicionesL:

            for neighbor in self.model.grid.iter_neighbors(i, moore=True):
                
                if neighbor.pos[0] == i[0] & neighbor.pos[1] != i[1]: #SIGNIFICA QUE ES VERTICAL --> Valor de 1
                    neighbor.orien = 1 #Significa que viene de una calle en vertical

                    if neighbor.value == 4: #Si el valor es 4 significa que es un Agente Automovilistico :O
                        countCars += 1 #Cuando se detectan más de un auto

                        if countCars > 1:
                            #Se ingresan los autos en la lista
                            self.ordenamientoL.append(neighbor)
                            #Agregar que no se repitan en la lista
                            
                            #Se detienen los autos
                            #Automovil.detenido = True

                elif neighbor.pos[0] != i[0] & neighbor.pos[1] == i[1]: #SIGNIFICA QUE ES HORIZONTAL --> Valor de 2

                    neighbor.orien = 2 #Significa que viene de una calle en horizontal

                    if neighbor.value == 4: #Si el valor es 4 significa que es un Agente Automovilistico :O
                        countCars += 1 #Cuando se detectan más de un auto

                        if countCars > 1:
                            #Se ingresan los autos en la lista
                            self.ordenamientoL.append(neighbor)
                            #Agregar que no se repitan en la lista

                            #Se detienen los autos
                            #Automovil.detenido = True

        # ||||||||||||||||| EVALUA LAS INTERSECCIONES VERTICALES ||||||||||||||||||||||

        for i in self.posicionesV:

            for neighbor in self.model.grid.iter_neighbors(i, moore=True):
                
                if neighbor.pos[0] == i[0] & neighbor.pos[1] != i[1]: #SIGNIFICA QUE ES VERTICAL --> Valor de 1
                    neighbor.orien = 1 #Significa que viene de una calle en vertical

                    if neighbor.value == 4: #Si el valor es 4 significa que es un Agente Automovilistico :O
                        countCars += 1 #Cuando se detectan más de un auto

                        if countCars > 1:
                            #Se ingresan los autos en la lista
                            self.ordenamientoV.append(neighbor)
                            #Agregar que no se repitan en la lista
                            
                            #Se detienen los autos
                            #Automovil.detenido = True

                elif neighbor.pos[0] != i[0] & neighbor.pos[1] == i[1]: #SIGNIFICA QUE ES HORIZONTAL --> Valor de 2

                    neighbor.orien = 2 #Significa que viene de una calle en horizontal

                    if neighbor.value == 4: #Si el valor es 4 significa que es un Agente Automovilistico :O
                        countCars += 1 #Cuando se detectan más de un auto

                        if countCars > 1:
                            #Se ingresan los autos en la lista
                            self.ordenamientoV.append(neighbor)
                            #Agregar que no se repitan en la lista

                            #Se detienen los autos
                            #Automovil.detenido = True

        # ||||||||||||||||| EVALUA LAS INTERSECCIONES DE CRUCE 4 ||||||||||||||||||||||

        for i in self.posiciones4:

            for neighbor in self.model.grid.iter_neighbors(i, moore=True):
                
                if neighbor.pos[0] == i[0] & neighbor.pos[1] != i[1]: #SIGNIFICA QUE ES VERTICAL --> Valor de 1
                    neighbor.orien = 1 #Significa que viene de una calle en vertical

                    if neighbor.value == 4: #Si el valor es 4 significa que es un Agente Automovilistico :O
                        countCars += 1 #Cuando se detectan más de un auto

                        if countCars > 1:
                            #Se ingresan los autos en la lista
                            self.ordenamiento4.append(neighbor)
                            #Agregar que no se repitan en la lista
                            
                            #Se detienen los autos
                            #Automovil.detenido = True

                elif neighbor.pos[0] != i[0] & neighbor.pos[1] == i[1]: #SIGNIFICA QUE ES HORIZONTAL --> Valor de 2

                    neighbor.orien = 2 #Significa que viene de una calle en horizontal

                    if neighbor.value == 4: #Si el valor es 4 significa que es un Agente Automovilistico :O
                        countCars += 1 #Cuando se detectan más de un auto

                        if countCars > 1:
                            #Se ingresan los autos en la lista
                            self.ordenamiento4.append(neighbor)
                            #Agregar que no se repitan en la lista

                            #Se detienen los autos
                            #Automovil.detenido = True
                                 
                    
    #Una vez realizado todo, esta función se encargará de hacer que los automoviles se muevan de acuerdo a su orden
    def aignacionDesplazamiento(self):
        for i in self.ordenamiento4:
            print(i)
            #i.detenido = False

            #------ REGLAS PARA EL CRUCE DE 4 CAMINOS -----

            #if i.orien == 1 Significa que es Vertical
                #if i.destino_temporal == 1
                    #i.sentido SE MANTIENE
            #elif i.orien == 2 Significa que es horizontal
                #if i.destino_temporal == 1
                    #i.sentido SE MANTIENE
                #elif i.destino_temporal == 2
                    #i.sentido SE CAMBIA

        for i in self.ordenamientoV:
            print(i)
            #i.detenido = False

            #------ REGLAS PARA EL CRUCE VERTICAL -----

            #if i.orien == 1 Significa que es Vertical
                #if i.destino_temporal == 1
                    #i.sentido SE MANTIENE
                #elif i.destino_temporal == 2
                    #i.sentido SE CAMBIA
            #elif i.orien == 2 Significa que es horizontal
                #if i.destino_temporal == 1
                    #i.sentido SE MANTIENE
                #elif i.destino_temporal == 2
                    #i.sentido SE CAMBIA

        for i in self.ordenamientoL:
            print(i)
            #i.detenido = False

            #------ REGLAS PARA EL CRUCE LATERAL -----

            #if i.orien == 1 Significa que es Vertical
                #if i.destino_temporal == 1
                    #i.sentido SE MANTIENE
                #elif i.destino_temporal == 2
                    #i.sentido SE CAMBIA
            #elif i.orien == 2 Significa que es horizontal
                #if i.destino_temporal == 1
                    #i.sentido SE MANTIENE
                #elif i.destino_temporal == 2
                    #i.sentido SE CAMBIA

class Automovil(Agent):
    VALUE = 4
    ORDEN = 0
    Orientacion = True
    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.value = self.VALUE
        self.orden = self.ORDEN
        self.orien = self.Orientacion
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
        self.interseccionLateral = [(5,16),(5,17),(6,18),(7,18),(6,15),(7,15),(29,17),(30,17),(29,20),(30,20),(31,19),(31,18)]
        self.interseccionCuatro = [(13,25),(14,25),(12,24),(12,23),(15,24),(15,23),(13,22),(14,22),(12,11),(12,10),(15,11),(15,10),(13,12),(14,12),(13,9),(14,9),(20,24),(20,23),(21,25),(22,25),(21,22),(22,22),(23,24),(23,23),(20,11),(20,10),(23,11),(23,10),(21,12),(22,12),(21,9),(22,9)]
        self.interseccionVertical = [(21,2),(22,2),(21,5),(22,5),(20,3),(20,4),(13,32),(14,32),(13,29),(14,29),(15,30),(15,31)]
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