import random
import numpy as np

class Field:
    def __init__(self,parent,population=100):
        self.parent = parent
        self.population = population
        self.coords = np.random.random((self.population,2))
        self.mass = np.random.random((self.population,1))
        self.velocity = np.zeros((self.population,2))
        self.acceleration = np.zeros((self.population,2))
        self.gravitational_constant = .001
        self.radius_per_mass = .005
    def step(self):
        # find product of all masses multiplied by all other masses
        mass_products = self.mass.dot(self.mass.T)
        mass_products = mass_products.reshape(self.population**2,1)
        mass_products = np.repeat(mass_products,2,1)
        
        # repeat all coordinates p times, 111222333...
        coords1 = np.repeat(self.coords,self.population,0)
        
        # repeat all coordinates p times, 123123123...
        coords2 = np.concatenate([[self.coords]] * self.population, axis=0)
        coords2 = coords2.reshape(self.population**2,2)
        
        # find coordinate deltas for each particle to each other particle
        coordinate_deltas = coords1 - coords2
        
        # find the signs of the coordinate deltas, IE, directions of the vectors
        vector_signs = np.ones(coordinate_deltas.shape)
        vector_signs[coordinate_deltas < 0] = vector_signs[coordinate_deltas < 0] * -1
        
        # calculate r
        radius = (coordinate_deltas[:,0]**2 + coordinate_deltas[:,1]**2)**.5
        radius = radius.reshape(self.population**2,1)
        radius = np.repeat(radius,2,1)
        
        # find acceleration G*m1*m2/r for x and y components for each particle
        acceleration = np.zeros((self.population**2,2))
        acceleration[coordinate_deltas!=0] = self.gravitational_constant * mass_products[coordinate_deltas!=0] * 1/(radius[coordinate_deltas!=0])
        acceleration = acceleration * coordinate_deltas
        acceleration = acceleration.reshape(self.population,self.population,2)
        self.acceleration = np.mean(acceleration,0)*self.population/(self.population-1)
        
        # update velocity 
        self.velocity = self.velocity + self.acceleration
        
        # update coords
        self.coords = self.coords + self.velocity
    def collisions(self):
        # repeat all coordinates p times, 111222333...
        coords1 = np.repeat(self.coords,self.population,0)
        
        # repeat all coordinates p times, 123123123...
        coords2 = np.concatenate([[self.coords]] * self.population, axis=0)
        coords2 = coords2.reshape(self.population**2,2)
        
        # compute radii
        radii = self.mass * self.radius_per_mass
        
        # repeat all radii p times, 111222333...
        radii1 = np.repeat(radii,self.population,0)
        
        # repeat all radii p times, 123123123...
        radii2 = np.concatenate([[radii]] * self.population, axis=0)
        radii2 = radii2.reshape(self.population**2,2)
        
        # get sums of radii of every pair of masses
        radius_sums = radii1 + radii2
        
        # find which masses have collided
        coordinate_deltas = coords1 - coords2
        distances = (coordinate_deltas[:,0]**2+coordinate_deltas[:,1]**2)**.5
        distances = distances - radius_sums
        
        # create a mask for pairs of the same mass
        mask = np.zeros(self.population+1)
        mask[0,0]=1
        times_to_repeat = (self.population**2/(self.population+1))//1+1
        mask = np.concatenate([[mask]] * times_to_repeat, axis=0)
        mask = mask.reshape(times_to_repeat,1)
        mask = mask[:self.population**2,0]
        
        # set the distances between the same masses as 1 so they don't count as collisions
        distances[mask==1] = 1
        
        # repeat all masses p times, 111222333...
        mass1 = np.repeat(self.mass,self.population,0)
        
        # repeat all masses p times, 123123123...
        mass2 = np.concatenate([[self.mass]] * self.population, axis=0)
        mass2 = mass2.reshape(self.population**2,2)
        
        # sum of every pair of masses
        mass_sums = mass1 + mass2
        
        # find center of mass between every pair of particles
        # (m1*x1+m2*x2)/(x1+x2), (m1*y1+m2*y2)/(y1+y2)
        x_components_1 = coords1[:,0]
        y_components_1 = coords1[:,1]
        x_components_2 = coords2[:,0]
        y_components_2 = coords2[:,1]
        x_component_centers_of_mass = (mass1*x_components_1+mass2*x_components_2)/(x_components_1+x_components_2)
        y_component_centers_of_mass = (mass1*y_components_1+mass2*y_components_2)/(y_components_1+y_components_2)
        # centers_of_mass = np.concatenate((x_component_centers_of_mass,y_component_centers_of_mass),1)
        
        # repeat all velocities p times, 111222333...
        velocity1 = np.repeat(self.velocity,self.population,0)
        
        # repeat all velocities p times, 123123123...
        velocity2 = np.concatenate([[self.velocity]] * self.population, axis=0)
        velocity2 = velocity2.reshape(self.population**2,2)
        
        # compute new velocity for each pair, to use if they have collided
        # (m1*vx1+m2*vx2)/mt, (m1*vy1+m2*vy2)/mt
        x_components_1 = velocity1[:,0]
        y_components_1 = velocity1[:,1]
        x_components_2 = velocity2[:,0]
        y_components_2 = velocity2[:,1]
        x_component_new_velocity = (mass1*x_components_1+mass2*x_components_2)/mass_sums
        y_component_new_velocity = (mass1*y_components_1+mass2*y_components_2)/mass_sums
        # new_velocity = np.concatenate((x_component_new_velocity,y_component_new_velocity),1)
        
        # for each collision, update with new coordinates, mass, and velocity
        self.coords[:,0][distances < 0] = x_component_centers_of_mass[distances < 0]
        self.coords[:,1][distances < 0] = y_component_centers_of_mass[distances < 0]
        self.mass[distances < 0] = mass_sums[distances < 0]
        self.velocity[:,0][distances < 0] = x_component_new_velocity[distances < 0]
        self.velocity[:,1][distances < 0] = y_component_new_velocity[distances < 0]
        
        # remove one member of the population for every collision, and update self.population accordingly
        
        