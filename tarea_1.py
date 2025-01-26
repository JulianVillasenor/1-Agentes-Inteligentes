#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------
Revisa el archivo README.md con las instrucciones de la tarea.
"""
__author__ = 'Julian_Villaseñor'

import entornos_o
import random  # Importa random para el agente aleatorio


class NueveCuartos(entornos_o.Entorno):
    """
    Implementación del entorno de los nueve cuartos.
    """
    def __init__(self, x0=None):
        if x0 is None:
            x0 = ['sucio'] * 9 + ['A']  # Estado inicial: todo sucio y el agente en A
        self.x = x0
        self.desempeño = 0
        self.conexiones = {
            'A': {'derecha': 'B', 'subir': None, 'izquierda': None, 'bajar': None},
            'B': {'derecha': 'C', 'subir': None, 'izquierda': 'A', 'bajar': None},
            'C': {'derecha': None, 'subir': 'F', 'izquierda': 'B', 'bajar': None},
            'D': {'derecha': 'E', 'subir': None, 'izquierda': None, 'bajar': 'A'},
            'E': {'derecha': 'F', 'subir': None, 'izquierda': 'D', 'bajar': None},
            'F': {'derecha': None, 'subir': 'I', 'izquierda': 'E', 'bajar': None},
            'G': {'derecha': 'H', 'subir': None, 'izquierda': None, 'bajar': 'D'},
            'H': {'derecha': 'I', 'subir': None, 'izquierda': 'G', 'bajar': None},
            'I': {'derecha': None, 'subir': None, 'izquierda': 'H', 'bajar': None}
        }

    def accion_legal(self, accion):
        if accion == 'limpiar':
            return True
        pos = self.x[9]
        return self.conexiones[pos].get(accion.lower()) is not None

    def transicion(self, accion):
        pos = self.x[9]
        if not self.accion_legal(accion):
            return
        if accion == "limpiar":
            indice = ord(pos) - ord('A')
            if self.x[indice] == 'sucio':
                self.x[indice] = 'limpio'
                self.desempeño += 10
        elif accion.lower() in ["derecha", "izquierda", "subir", "bajar"]:
            self.x[9] = self.conexiones[pos][accion.lower()]
            self.desempeño -= 1 if accion.lower() in ["derecha", "izquierda"] else 2
        elif accion == "nada":
            pass

    def percepcion(self):
        pos = self.x[9]
        indice = ord(pos) - ord('A')
        return (self.x[indice], pos)

class NueveCuartosCiego(NueveCuartos):
    def percepcion(self):
        # El agente ciego no puede percibir si la habitación está sucia o limpia,
        # solo conoce su posición actual.
        return self.x[9]
    
class NueveCuartosEstocastico(NueveCuartos):
    def transicion(self, accion):
        
        probabilidad = random.random()  # Genera un número aleatorio entre 0 y 1
        # Si la acción es limpiar
        if accion == "limpiar":
            if probabilidad < 0.8:  # 80% limpia correctamente
                super().transicion(accion)
            # 20% no limpia (hacer nada)
            return
        elif accion in ["derecha", "izquierda", "subir", "bajar"]:
            if probabilidad < 0.8:  # 80% se mueve correctamente
                super().transicion(accion)
            elif probabilidad < 0.9:  # 10% se queda en el mismo lugar
                return
            else:  # 10% realiza una acción legal aleatoria
                acciones = ["derecha", "izquierda", "subir", "bajar", "limpiar", "nada"]
                accion_aleatoria = random.choice(acciones)
                if self.accion_legal(accion_aleatoria):
                    super().transicion(accion_aleatoria)
            return
        # Si la acción es 'nada' 
        super().transicion(accion)

class AgenteAleatorio(entornos_o.Agente):
    def programa(self, percepcion):
        acciones = ["derecha", "izquierda", "subir", "bajar", "limpiar", "nada"]
        return random.choice(acciones)


class AgenteReactivo(entornos_o.Agente):
    def programa(self, percepcion):
        estado, posicion = percepcion  # Recibe ['sucio', 'A']
        probabilidad = random.random()
        if estado == 'sucio':
            return 'limpiar'
        elif posicion in ['B','E','H'] and probabilidad < .5:
            return 'izquierda'
        elif posicion in ['B','E','H'] and probabilidad > .5:
            return 'derecha'
        elif posicion in ['C','F'] and probabilidad <.5:
            return 'izquierda'
        elif posicion in ['C','F'] and probabilidad >.5:
            return 'subir'
        elif posicion in ['D','G'] and probabilidad <.5:
            return 'derecha'
        elif posicion in ['D','G'] and probabilidad >.5:
            return 'bajar'
        elif posicion == 'A':
            return 'derecha'
        else: 
            return 'izquierda'# caso I



class AgenteRacional_Modelo(entornos_o.Agente):
    def __init__(self):
        """
        Inicializa el agente con un modelo interno del entorno.
        El modelo interno incluye el estado de limpieza de los cuartos
        y la posición actual del agente.
        """
        # Inicializar el modelo con todos los cuartos como sucios
        self.modelo = {
            'A': 'sucio',  #A B C
            'B': 'sucio',  # d e f
            'C': 'sucio',  # g h i
            'F': 'sucio',
            'E': 'sucio',
            'D': 'sucio',
            'I': 'sucio',
            'H': 'sucio',
            'G': 'sucio'
        }
        self.posicion_actual = 'A'  # Comienza en A por defecto

    def programa(self, percepcion):
        estado, posicion = percepcion
        # Actualizar el modelo interno con la percepción actual
        self.modelo[posicion] = estado
        self.posicion_actual = posicion  # Actualizar la posición actual
        if estado == 'sucio':
            return 'limpiar'

        # Si todos los cuartos están limpios, detenerse
        if all(estado == 'limpio' for estado in self.modelo.values()):
            return 'nada'

        # Obtener las conexiones del entorno para decidir el movimiento
        conexiones = entorno.conexiones[self.posicion_actual]
        for direccion, cuarto in conexiones.items():
            if cuarto is not None and self.modelo[cuarto] == 'sucio':
                return direccion  # Moverse hacia el cuarto sucio más cercano

        # Si no hay cuartos sucios conectados directamente, moverse a cualquier otro cuarto
        for direccion, cuarto in conexiones.items():
            if cuarto is not None:
                return direccion

        # Si no queda nada más que hacer
        return 'nada'

            

class AgenteRacional_Ciego(entornos_o.Agente):
    def __init__(self):
        self.modelo = {
            'A': 'sucio',  #A B C
            'B': 'sucio',  # d e f
            'C': 'sucio',  # g h i
            'F': 'sucio',
            'E': 'sucio',
            'D': 'sucio',
            'I': 'sucio',
            'H': 'sucio',
            'G': 'sucio'
        }
        self.posicion_actual = 'A'
    def programa(self, percepcion):
        self.posicion_actual = percepcion
        if self.modelo[self.posicion_actual] == 'sucio':
            self.modelo[self.posicion_actual] = 'limpio'
            return 'limpiar'
         # Si el cuarto actual ya está limpio, buscar a dónde moverse
        conexiones = entorno.conexiones[self.posicion_actual]
        for direccion, cuarto in conexiones.items():
            if cuarto is not None and self.modelo[cuarto] == 'sucio':
                return direccion #accion que hace el robot

        for direccion, cuarto in conexiones.items():
            if cuarto is not None: #muevete hacia la conexion si no hay chamba
                return direccion
        return 'nada'
        
        

"""
    Diseña un Agente reactivo basado en modelo para este entorno y compara su desempeño
    con un agente aleatorio después de 200 pasos de simulación.

    NueveCuartosCiego: Diseña un agente racional para este problema,
    pruébalo y compáralo con el agente aleatorio.

    Al modelo original de NueveCuartos modifícalo para que cuando el agente decida aspirar,
    el 80% de las veces limpie pero el 20% (aleatorio) deje sucio el cuarto.
    Igualmente, cuando el agente decida cambiar de cuarto, se cambie correctamente de cuarto el 80% de la veces,
    el 10% de la veces se queda en su lugar y el 10% de las veces realiza una acción legal aleatoria.
    Diseña un agente racional para este problema, pruébalo y compáralo con el agente aleatorio.

    """
entorno = NueveCuartos()
agente = AgenteReactivo()
_,_,desempeño= entornos_o.simulador(entorno, agente, pasos=200,verbose=True)
desempeñosReactivo = desempeño[-1] #toma el ultimo valor en desempeño

entorno = NueveCuartos()
agente = AgenteRacional_Modelo()
_,_,desempeño= entornos_o.simulador(entorno, agente, pasos=200,verbose=True)
desempeñoRacModelo = desempeño[-1]
#historial_estados, historial_acciones, historial_desempeño

entorno = NueveCuartos()
agente = AgenteAleatorio()
_,_,desempeño= entornos_o.simulador(entorno, agente, pasos=200,verbose=True)
desempeñoAleatorio = desempeño[-1]

#********Ejercicio numero 2 compara ajente aleatorio con racional es entorno ciego


entorno = NueveCuartosCiego()
agente = AgenteRacional_Ciego()
_,_,desempeño= entornos_o.simulador(entorno, agente, pasos=200,verbose=True)
desempeñoRacionalCiego = desempeño[-1]

entorno = NueveCuartosCiego()
agente = AgenteAleatorio()
_,_,desempeño= entornos_o.simulador(entorno, agente, pasos=200,verbose=True)
desempeñoAleatorioCiego = desempeño[-1]
#Ejemplo de entorno estocastico
entorno = NueveCuartosEstocastico()
agente = AgenteRacional_Modelo()
_,_,desempeño = entornos_o.simulador(entorno, agente, pasos=200, verbose=True)
desempeñoRacionalEstocastico = desempeño[-1]

entorno = NueveCuartosEstocastico()
agente = AgenteAleatorio()
_,_,desempeño= entornos_o.simulador(entorno, agente, pasos=200,verbose=True)
desempeñoAleatorioEstocastico = desempeño[-1]

print(f"Desempeño final después de 200 pasos del reactivo es: {desempeñosReactivo}")
print(f"Desempeño final del modelo reactivo con modelo: {desempeñoRacModelo}")
print(f"Desempeño final del robot aleatorio: {desempeñoAleatorio}")
print(f"El robot aleatorio tiene un desempeño de: {(desempeñoAleatorio + 300)/(desempeñosReactivo + 300)} después de 200 pasos respecto al robot reactivo")
print(f"El robot aleatorio tiene un desempeño de: {(desempeñoAleatorio + 300)/(desempeñoRacModelo + 300)} después de 200 pasos respecto al modelo reactivo")


#Entorno ciego
print(f"Desempeño final después de 200 pasos: {desempeñoRacionalCiego}")
print(f"Desempeño final del modelo aleatorio: {desempeñoAleatorioCiego}")
print(f"El robot aleatorio tiene un desempeño de: {(desempeñoAleatorioCiego + 300)/(desempeñoRacionalCiego + 300)} después de 200 pasos respecto al modelo reactivo")

#Entorno estocastico
print(f"Desempeño final después de 200 pasos: {desempeñoRacionalEstocastico}")
print(f"Desempeño final del robot aleatorio en el entorno estocastico: {desempeñoAleatorioEstocastico}")
print(f"El robot aleatorio tiene un desempeño de: {(desempeñoAleatorioEstocastico + 300)/(desempeñoRacionalEstocastico + 300)} después de 200 pasos respecto al modelo reactivo")
