import math
import random

class vector:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z
    def vector_sum(self, vector_2):
        self.x += vector_2.x
        self.y += vector_2.y
        self.z += vector_2.z

class body:
    def __init__(self, position, velocity, mass = 1, id = '', colour = ''):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.id = id
        self.plot_color = colour

# Function to calculate the acceleration of body_1 due to the gravitational attraction of body_2
def acceleration_calculation(body_1, body_2):
    G = 6.67408e-11 #m3 kg-1 s-2
    accel_vector = vector(0,0,0)
    # We calculate the distance between the bodies
    distance = math.sqrt((body_1.position.x - body_2.position.x)**2 + (body_1.position.y - body_2.position.y)**2 + (body_1.position.z - body_2.position.z)**2)
    # We calculate the acceleration vector components in each dimension
    accel_vector.x = (body_2.mass * G / distance**3) * (body_2.position.x - body_1.position.x)
    accel_vector.y = (body_2.mass * G / distance**3) * (body_2.position.y - body_1.position.y)
    accel_vector.z = (body_2.mass * G / distance**3) * (body_2.position.z - body_1.position.z)
    return accel_vector

# Function to update the speed of a body based on it's acceleration vector
def velocity_calculation(body, accel_vector, time_step = 1):
    body.velocity.x += accel_vector.x * time_step
    body.velocity.y += accel_vector.y * time_step
    body.velocity.z += accel_vector.z * time_step
    return body.velocity

# Function to update the position of a body based on it's speed vector
def position_calculation(body, time_step = 1):
    body.position.x += body.velocity.x * time_step
    body.position.y += body.velocity.y * time_step
    body.position.z += body.velocity.z * time_step
    return body.position

# Function to run the simulation over a list of bodies in a number of time steps of a certain size, plotting each n time steps
def compute_n_body_problem(bodies, time_step_size = 1, time_steps_number = 10000, frequency = 100):
    for time_step in range(1,time_steps_number):
        for body_1 in bodies:
            accel_vector = vector(0,0,0)
            for body_2 in bodies:
                if body_1.id != body_2.id:
                    accel_vector.vector_sum(acceleration_calculation(body_1,body_2))
            body_1.velocity = velocity_calculation(body_1,accel_vector,time_step_size)
            body_1.position = position_calculation(body_1,time_step_size)
        #if time_step % frequency == 0:
    return bodies

def animate_scatters(iteration, data, scatters):
    """
    Update the data held by the scatter plot and therefore animates it.
    Args:
        iteration (int): Current iteration of the animation
        data (list): List of the data positions at each iteration.
        scatters (list): List of all the scatters (One per element)
    Returns:
        list: List of scatters (One per element) with new coordinates
    """
    for i in range(data[0].shape[0]):
        scatters[i]._offsets3d = (data[iteration][i,0:1], data[iteration][i,1:2], data[iteration][i,2:])
    return scatters



# Define the data and run the simulation
if __name__ == "__main__":
    bodies = [
        body(vector(0,0,0),vector(0,0,0),1,'Star1','r'),
        body(vector(1,0,0),vector(0,0,0),1,'Star2','b')
    ]

    solution = compute_n_body_problem(bodies,100,80000,1000)

