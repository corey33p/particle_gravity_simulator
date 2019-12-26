import random
import numpy as np

np.set_printoptions(suppress=True, precision=2, linewidth=140)

class Field:
    def __init__(self,parent,population=100):
        self.parent = parent
        self.population = population
        self.coords = np.random.random((self.population,2))
        self.mass = np.random.random((self.population,1))*10
        self.velocity = np.zeros((self.population,2))
        self.acceleration = np.zeros((self.population,2))
        self.gravitational_constant = .00005
        self.density = 500
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
        collisions = True
        while collisions:
            # repeat all coordinates p times, 111222333...
            coords1 = np.repeat(self.coords,self.population,0)
            
            # repeat all coordinates p times, 123123123...
            coords2 = np.concatenate([[self.coords]] * self.population, axis=0)
            coords2 = coords2.reshape(self.population**2,2)
            
            # compute radii
            radii = (.75/3.14159*self.mass*self.density)**(1/3)
            
            # repeat all radii p times, 111222333...
            radii1 = np.repeat(radii,self.population,0)
            
            # repeat all radii p times, 123123123...
            radii2 = np.concatenate([[radii]] * self.population, axis=0)
            radii2 = radii2.reshape(self.population**2,1)
            
            # get sums of radii of every pair of masses
            radius_sums = radii1 + radii2
            
            # find which masses have collided
            coordinate_deltas = coords1 - coords2
            distances = (coordinate_deltas[:,0]**2+coordinate_deltas[:,1]**2)**.5
            distances = distances.reshape((self.population**2,1))
            distances = distances - radius_sums
            print("distances: " + str(distances))
            collisions = np.any(distances<0)
            
            if collisions:
                # create a mask for pairs of the same mass
                mask = np.zeros((self.population+1))
                mask[0]=1
                times_to_repeat = int((self.population**2/(self.population+1))//1+1)
                mask = np.concatenate([[mask]] * times_to_repeat, axis=1).T
                mask = mask.reshape(mask.shape[0],1)
                mask = mask[:self.population**2,0]
                
                # set the distances between the same masses as 1 so they don't count as collisions
                distances[mask==1] = 1
                
                # repeat all masses p times, 111222333...
                mass1 = np.repeat(self.mass,self.population,0)
                
                # repeat all masses p times, 123123123...
                mass2 = np.concatenate([[self.mass]] * self.population, axis=0)
                mass2 = mass2.reshape(self.population**2,1)
                
                # sum of every pair of masses
                mass_sums = mass1 + mass2
                
                # find center of mass between every pair of particles
                # (m1*x1+m2*x2)/(x1+x2), (m1*y1+m2*y2)/(y1+y2)
                x_components_1 = coords1[:,0].reshape(self.population**2,1)
                y_components_1 = coords1[:,1].reshape(self.population**2,1)
                x_components_2 = coords2[:,0].reshape(self.population**2,1)
                y_components_2 = coords2[:,1].reshape(self.population**2,1)
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
                x_components_1 = velocity1[:,0].reshape(self.population**2,1)
                y_components_1 = velocity1[:,1].reshape(self.population**2,1)
                x_components_2 = velocity2[:,0].reshape(self.population**2,1)
                y_components_2 = velocity2[:,1].reshape(self.population**2,1)
                x_component_new_velocity = (mass1*x_components_1+mass2*x_components_2)/mass_sums
                y_component_new_velocity = (mass1*y_components_1+mass2*y_components_2)/mass_sums
                # new_velocity = np.concatenate((x_component_new_velocity,y_component_new_velocity),1)
                
                # create parent labels, to prevent the same mass being included into multiple collisions
                numbers = np.arange(self.population).reshape(self.population,1)
                # repeat parent labels p times, 111222333...
                parents1 = np.repeat(numbers,self.population,0)
                # repeat all parent labels p times, 123123123...
                parents2 = np.concatenate([[numbers]] * self.population, axis=0)
                parents2 = parents2.reshape(self.population**2,1)
                
                
                # objects after collision
                # parent 1, parent 2, locX, locY, mass, velocityX, velocityY
                distances_mask = [distances < 0][0].reshape(self.population**2)
                new_masses = np.zeros((self.population**2,7))
                print("new_masses:\n" + str(new_masses))
                new_masses[:,0] = parents1.reshape(self.population**2)
                new_masses[:,1] = parents2.reshape(self.population**2)
                new_masses[:,2][distances_mask] = np.squeeze(x_component_centers_of_mass[distances_mask])
                new_masses[:,3][distances_mask] = np.squeeze(y_component_centers_of_mass[distances_mask])
                new_masses[:,4][distances_mask] = np.squeeze(mass_sums[distances_mask])
                new_masses[:,5][distances_mask] = np.squeeze(x_component_new_velocity[distances_mask])
                new_masses[:,6][distances_mask] = np.squeeze(y_component_new_velocity[distances_mask])
                print("new_masses:\n" + str(new_masses))
                unique_keys, indices = np.unique(new_masses[:,0], return_index=True)
                print("unique_keys: " + str(unique_keys))
                print("indices: " + str(indices))
                new_masses = new_masses[indices]
                print("new_masses:\n" + str(new_masses))
                
                # delete the masses that made the collision
                self.mass[indices] = 0
                self.mass = self.mass[self.mass[:,0]!=0]
                self.coords = self.coords[self.mass[:,0]!=0]
                self.velocity = self.velocity[self.mass[:,0]!=0]
                
                # add the new masses to the existing masses
                self.mass = np.concatenate((self.mass, new_masses[:,4]),axis=0)
                self.coords = np.concatenate((self.coords, new_masses[:,2:4]),axis=0)
                self.velocity = np.concatenate((self.velocity, new_masses[:,5:]),axis=0)
                
                # check if the arrays are the same size
                assert(self.mass.shape[0]==self.coords.shape[0]==self.velocity.shape[0])
