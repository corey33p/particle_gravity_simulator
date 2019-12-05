import random
import numpy as np

class Field:
    def __init__(self,population=100):
        self.population = population
        self.coords = np.random.random((self.population,2))
        self.mass = np.random.random((self.population,1))
    def distance_from(self,coords):
        deltas = coords - self.coords
        x_coords = coords[...,0].reshape(self.population,1)
        y_coords = coords[...,1].reshape(self.population,1)
        distances = (x_coords**2 + y_coords**2)**.5
        return distances
    def move(self):
        gravitational_energy = 