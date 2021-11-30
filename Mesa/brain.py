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
from utils import AStar


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

class Interseccion(Agent):

    AUTOSV = []
    AUTOSL = []
    AUTOS4 = []

    def __init__(self, model, pos):
        super().__init__(model.next_id(), model)
        self.pos = pos
        self.valor = 3
        self.posicionesL = self.model.interseccionLateral
        self.posicionesV = self.model.interseccionVertical
        self.posiciones4 = self.model.interseccionCuatro
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
                    neighbor.orientacion = 1 #Significa que viene de una calle en vertical

                    if neighbor.valor == 5: #Si el valor es 4 significa que es un Agente Automovilistico :O
                        countCars += 1 #Cuando se detectan más de un auto

                        if countCars > 1:
                            #Se ingresan los autos en la lista
                            self.ordenamientoL.append(neighbor)
                            #Agregar que no se repitan en la lista
                            
                            #Se detienen los autos
                            #Automovil.detenido = True

                elif neighbor.pos[0] != i[0] & neighbor.pos[1] == i[1]: #SIGNIFICA QUE ES HORIZONTAL --> Valor de 2

                    neighbor.orientacion = 2 #Significa que viene de una calle en horizontal

                    if neighbor.valor == 5: #Si el valor es 4 significa que es un Agente Automovilistico :O
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
                    neighbor.orientacion = 1 #Significa que viene de una calle en vertical

                    if neighbor.valor == 5: #Si el valor es 4 significa que es un Agente Automovilistico :O
                        countCars += 1 #Cuando se detectan más de un auto

                        if countCars > 1:
                            #Se ingresan los autos en la lista
                            self.ordenamientoV.append(neighbor)
                            #Agregar que no se repitan en la lista
                            
                            #Se detienen los autos
                            #Automovil.detenido = True

                elif neighbor.pos[0] != i[0] & neighbor.pos[1] == i[1]: #SIGNIFICA QUE ES HORIZONTAL --> Valor de 2

                    neighbor.orientacion = 2 #Significa que viene de una calle en horizontal

                    if neighbor.valor == 5: #Si el valor es 4 significa que es un Agente Automovilistico :O
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
                    neighbor.orientacion = 1 #Significa que viene de una calle en vertical

                    if neighbor.valor == 5: #Si el valor es 4 significa que es un Agente Automovilistico :O
                        countCars += 1 #Cuando se detectan más de un auto

                        if countCars > 1:
                            #Se ingresan los autos en la lista
                            self.ordenamiento4.append(neighbor)
                            #Agregar que no se repitan en la lista
                            
                            #Se detienen los autos
                            #Automovil.detenido = True

                elif neighbor.pos[0] != i[0] & neighbor.pos[1] == i[1]: #SIGNIFICA QUE ES HORIZONTAL --> Valor de 2

                    neighbor.orientacion = 2 #Significa que viene de una calle en horizontal

                    if neighbor.valor == 5: #Si el valor es 4 significa que es un Agente Automovilistico :O
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
            i.detenido = False

            #------ REGLAS PARA EL CRUCE DE 4 CAMINOS -----

            if i.orientacion == 1: #Significa que es Vertical
                if i.destino_temporal == 1:
                    i.sentido #SE MANTIENE
            elif i.orientacion == 2: #Significa que es horizontal
                if i.destino_temporal == 1:
                    i.sentido #SE MANTIENE
                elif i.destino_temporal == 2:
                    i.sentido #SE CAMBIA

        for i in self.ordenamientoV:
            print(i)
            #i.detenido = False

            #------ REGLAS PARA EL CRUCE VERTICAL -----

            if i.orientacion == 1: #Significa que es Vertical
                if i.destino_temporal == 1:
                    i.sentido #SE MANTIENE
                elif i.destino_temporal == 2:
                    i.sentido #SE CAMBIA
            elif i.orientacion == 2: #Significa que es horizontal
                if i.destino_temporal == 1:
                    i.sentido #SE MANTIENE
                elif i.destino_temporal == 2:
                    i.sentido #SE CAMBIA

        for i in self.ordenamientoL:
            print(i)
            #i.detenido = False

            #------ REGLAS PARA EL CRUCE LATERAL -----

            if i.orientacion == 1: #Significa que es Vertical
                if i.destino_temporal == 1:
                    i.sentido #SE MANTIENE
                elif i.destino_temporal == 2:
                    i.sentido #SE CAMBIA
            elif i.orientacion == 2: #Significa que es horizontal
                if i.destino_temporal == 1:
                    i.sentido #SE MANTIENE
                elif i.destino_temporal == 2:
                    i.sentido #SE CAMBIA
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


        self.currentState = currentState
    
    def step(self):
        
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

    def setNextAction(self):
        print(self.posicion_x, self.posicion_y)
        self.movimientos = AStar(self.posicion_y, self.posicion_x, self.destino_y, self.destino_x, self.model.matrix, self.sentido) 
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
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,2,2,4,3,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,2,1,1,4,3,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,2,1,0,0,0,0,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,0,2,1,0,0,0,0,0,4,4,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,1,4,3,3,3,3,4,1,1,4,3,3,3,3,4,1,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,1,2,4,3,3,3,3,4,2,2,4,3,3,3,3,4,2,1,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,1,2,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,2,1,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,1,2,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,2,1,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 4,4,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,2,1, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 3,3,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,2,1, 0,0,0,0,0,0],
            [1,1,1,1,4,3, 3,3,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,4,4, 0,0,0,0,0,0],
            [2,2,2,2,4,3, 3,3,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,3,3, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 3,3,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,3,3, 3,4,1,1,1,1],
            [0,0,0,0,0,0, 4,4,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,3,3, 3,4,2,2,2,2],
            [0,0,0,0,0,0, 2,1,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,3,3, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,2,1,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,4,4,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,2,1,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,1,2,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,2,1,4,3,3,3,3,4,1,1,4,3,3,3,3,4,1,2,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,2,4,3,3,3,3,4,2,2,4,3,3,3,3,4,2,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,4,4,0,0,0,0,0,0,4,4,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,2,1,0,0,0,0,0,0,2,1,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,4,4,0,0,0,0,0,2,1,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,0,0,0,0,2,1,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,3,4,2,2,1,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
            [0,0,0,0,0,0, 0,0,0,0,0,0,0,3,3,3,4,1,1,0,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0],
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
                
        self.mapOfPaths = {
            "A" : [(22,1),(22,6),(22,8),(24,10),(29,16),(31,18)],
            "B" : [(22,1),(22,6),(22,8),(22,13),(22,21),(22,26),(16,31),(14,33)],
            "C" : [(22,21),(22,6),(22,8),(19,11), (16,11), (11,11), (7,14), (4,17)],
            
            "D" : [(4,16),(7,19),(11,23),(16,23),(19,23),(24,23),(27,21),(31,18)],
            "E" : [(4,16),(6,14),(11,10),(13,8),(19,3),(21,1)],
            "F" : [(4,16),(7,19),(11,23),(14,26),(14,28),(14,33)],
            
            "G" : [(31,19),(28,16),(24,11),(21,8),(21,6),(21,1)],
            "H" : [(31,19),(28,21),(24,24),(19,24),(16,24),(11,24),(6,19),(4,17)],
            "I" : [(31,19),(28,21),(24,24),(22,26),(16,31),(14,33)],
            
            "J" : [(13,33),(13,28),(13,26),(13,21),(13,13),(13,8),(19,3), (21,1)],
            "K" : [(13,33),(13,28),(13,26),(11,24),(6,19),(4,17)],
            "L" : [(13,33),(16,30),(21,26),(24,23),(27,21),(31,18)]
        }

        carrito = Auto(self.next_id(), self, "1")
        self.grid.place_agent(carrito, (carrito.posicion_x, carrito.posicion_y))
        self.schedule.add(carrito)
        self.autos.append(carrito)



                
    def step(self):
        self.paso += 1
        self.schedule.step()
        if self.paso % 5 == 0:
            carrito = Auto(self.next_id(), self, "1")
            self.grid.place_agent(carrito, (carrito.posicion_x, carrito.posicion_y))
            self.schedule.add(carrito)
            self.autos.append(carrito)
    
    def updateInfo(self):
        data = []
        for auto in self.autos: 
            newDataAuto = {'posX': auto.posicion_x, 'posY': auto.posicion_y, 'finalizo': auto.finalizo, "angulo": auto.orientacion}
            data.append(newDataAuto)
        
        return data
            

        

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