import random
import numpy as np

class Field:
    def __init__(self,population=100):
        self.population = population
        self.coords = np.random.random((self.population,2))
        self.mass = np.random.random((self.population,1))
    def get_distances(self,deltas):
        x_coords = deltas[...,0].reshape(self.population,1)
        y_coords = deltas[...,1].reshape(self.population,1)
        distances = (x_coords**2 + y_coords**2)**.5
        return distances
    def move(self):
        mass_products = self.mass.dot(self.mass.T)
        coords_repeat = self.coords.reshape(self.population,2,1)
        coords_repeat = np.repeat(coords_repeat,self.population,axis=3)
        # self.coords may need reshaped here
        coordinate_deltas = self.coords - coords_repeat
        coordinate_deltas = coordinate_deltas.reshape(self.population**2,2)
        distances = self.get_distances(coordinate_deltas)
        