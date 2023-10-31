import random
import numpy as np
import copy

np.set_printoptions(suppress=True, precision=4, linewidth=140)
np.set_printoptions(threshold=np.inf)

class Field:
    def __init__(self,parent,
                      population=100,
                      gravitational_constant=.0001,
                      density=100000000,
                      time_step=.05,
                      velocity_std=0):
        self.parent = parent
        self.population = population
        self.starting_population = population
        self.gravitational_constant = gravitational_constant
        self.density = density
        self.time_step = time_step
        self.coords = np.random.random((self.population,2))
        self.mass = np.random.random((self.population,1))
        self.total_mass = float(np.sum(self.mass))
        self.get_center_of_mass()
        self.velocity = np.random.normal(0,velocity_std,(self.population,2))
        self.acceleration = np.zeros((self.population,2))
        
        # variables to detect an orbit
        self.orbitting = False
        self.decreasing = False
        self.last_distance = -1
        self.orbit_pattern = []
        self.orbit_threshold = 9 # must be greater than 3
        self.step_number = 0
        self.step_at_last_collision = None
        
        self.collisions()
    def get_center_of_mass(self):
        x_center_of_mass = float(np.sum(self.coords[:,0]*self.mass.flatten()))/self.total_mass
        y_center_of_mass = float(np.sum(self.coords[:,1]*self.mass.flatten()))/self.total_mass
        self.center_of_mass = x_center_of_mass, y_center_of_mass
    def step(self):
        self.step_number += 1
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
        # radius here is the distance between two masses
        radius = (coordinate_deltas[:,0]**2 + coordinate_deltas[:,1]**2)**.5
        radius = radius.reshape(self.population**2,1)
        radius = np.repeat(radius,2,1)
        
        # if there are 2 masses, check if they are orbitting
        if self.population == 2 and not self.orbitting:
            if self.last_distance == -1: self.last_distance = radius[1,0]
            else:
                if self.decreasing:
                    if radius[1,0] > self.last_distance:
                        self.orbit_pattern.append("increasing")
                        self.decreasing = False
                else:
                    if radius[1,0] < self.last_distance:
                        self.orbit_pattern.append("decreasing")
                        self.decreasing = True
            if len(self.orbit_pattern) >= self.orbit_threshold:
                self.orbitting = True
        
        # in general, try to detect a boring state
        if self.step_at_last_collision is not None:
            if self.step_number > 2*self.step_at_last_collision:
                if self.population < self.starting_population/2:
                    self.orbitting = True
        
        # find acceleration G*m1*m2/r for x and y components for each particle
        acceleration = np.zeros((self.population**2,2))
        acceleration[coordinate_deltas!=0] = self.gravitational_constant * mass_products[coordinate_deltas!=0] * 1/(radius[coordinate_deltas!=0]**2)
        acceleration = acceleration * coordinate_deltas
        acceleration = acceleration.reshape(self.population,self.population,2)
        self.acceleration = np.mean(acceleration,0)*self.population/(self.population-1)
        
        # update velocity
        self.velocity = self.velocity + self.acceleration * self.time_step
        
        # update coords
        self.coords = self.coords + self.velocity * self.time_step
        
        # update center of mass
        self.get_center_of_mass()
    def collisions(self):
        if self.population > 1: collisions = True
        else: collisions = False
        while collisions:
            # repeat all coordinates p times, 111222333...
            coords1 = np.repeat(self.coords,self.population,0)
            
            # repeat all coordinates p times, 123123123...
            coords2 = np.concatenate([[self.coords]] * self.population, axis=0)
            coords2 = coords2.reshape(self.population**2,2)
            
            # compute radii
            # radii here are of each individual mass
            radii = (3/4 * self.mass / (3.14159 * self.density))**(1/3)
            
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
            
            # create a mask for pairs of the same mass
            mask = np.zeros((self.population+1))
            mask[0]=1
            times_to_repeat = int((self.population**2/(self.population+1))//1+1)
            mask = np.concatenate([[mask]] * times_to_repeat, axis=1).T
            mask = mask.reshape(mask.shape[0],1)
            mask = mask[:self.population**2,0]
            
            # set the distances between the same masses as 1 so they don't count as collisions
            distances[mask==1] = 1
            
            collisions = np.any(distances<0)
            if collisions:
                self.step_at_last_collision = self.step_number
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
                x_component_centers_of_mass = (mass1*x_components_1+mass2*x_components_2)/(mass_sums)
                y_component_centers_of_mass = (mass1*y_components_1+mass2*y_components_2)/(mass_sums)
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
                new_masses[:,0] = parents1.reshape(self.population**2)
                new_masses[:,1] = parents2.reshape(self.population**2)
                new_masses[:,2][distances_mask] = np.squeeze(x_component_centers_of_mass[distances_mask])
                new_masses[:,3][distances_mask] = np.squeeze(y_component_centers_of_mass[distances_mask])
                new_masses[:,4][distances_mask] = np.squeeze(mass_sums[distances_mask])
                new_masses[:,5][distances_mask] = np.squeeze(x_component_new_velocity[distances_mask])
                new_masses[:,6][distances_mask] = np.squeeze(y_component_new_velocity[distances_mask])
                new_masses_bak = copy.deepcopy(new_masses)
                new_masses = new_masses[new_masses[:,4]!=0]
                
                # make sure same parent doesn't contribute to multiple new masses
                multi_collision_occurred = False
                unique_parents = set()
                for i in range(new_masses.shape[0]):
                    parentA = new_masses[i,0]
                    parentB = new_masses[i,1]
                    if parentA in unique_parents or parentB in unique_parents:
                        new_masses[i,4]=0
                        multi_collision_occurred = True
                    else:
                        unique_parents.add(parentA)
                        unique_parents.add(parentB)
                new_masses = new_masses[new_masses[:,4]!=0]
                a=new_masses[:,0:2]
                # b=np.flatten(a)
                indices = np.unique(a).astype(np.int32)
                
                # locX, locY, mass, velocityX, velocityY
                new_masses = new_masses[:,2:]
                entries = [list(row) for row in new_masses]
                new_masses = np.unique(entries,axis=0)
                
                # delete the masses that made the collision
                self.mass[indices] = 0
                self.coords = self.coords[self.mass[:,0]!=0]
                self.velocity = self.velocity[self.mass[:,0]!=0]
                self.mass = self.mass[self.mass[:,0]!=0]
                
                # add the new masses to the existing masses
                self.mass = np.concatenate((self.mass, new_masses[:,2].reshape(new_masses[:,2].shape[0],1)),axis=0)
                self.coords = np.concatenate((self.coords, new_masses[:,:2]),axis=0)
                self.velocity = np.concatenate((self.velocity, new_masses[:,3:]),axis=0)
                
                assert(self.mass.shape[0]==self.coords.shape[0]==self.velocity.shape[0])
                tot_mass = float(np.sum(self.mass))
                if abs(tot_mass-self.total_mass)>.01:
                    print("float(np.sum(self.mass)): " + str(float(np.sum(self.mass))))
                    print("self.total_mass: " + str(self.total_mass))
                    print("a:\n" + str(a))
                    print("indices:\n" + str(indices))
                    print("new_masses_bak:\n" + str(new_masses_bak))
                    print("new_masses:\n" + str(new_masses))
                    print("self.mass:\n" + str(self.mass))
                    print("self.coords:\n" + str(self.coords))
                    print("self.velocity:\n" + str(self.velocity))
                assert(abs(tot_mass-self.total_mass)<.01)
                
                # and update population count
                self.population = self.mass.shape[0]
                
                # if multi_collision_occurred:
                    # print("self.mass:\n" + str(self.mass))
                    # print("self.coords:\n" + str(self.coords))
                    # print("self.velocity:\n" + str(self.velocity))
                
                self.parent.display.update_count()
