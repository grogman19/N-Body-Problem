import math
import plotly.express as px
from scipy.spatial.transform import Rotation as R
import numpy as np

class vector:
    def __init__(self, x,y):
        self.x = x
        self.y = y
    def vector_sum(self, vector_2):
        self.x += vector_2.x
        self.y += vector_2.y

class body:
    def __init__(self, position, velocity, mass = 1, phase = 0, id = ''):
        position_vec = [position.x,position.y,0]
        rotation = R.from_rotvec(np.radians(phase) * np.array([0, 0, 1]))
        rotated_position = rotation.apply(position_vec)
        self.position = vector(rotated_position[0],rotated_position[1])
        velocity_vec = [velocity.x,velocity.y,0]
        rotated_velocity = rotation.apply(velocity_vec)
        self.velocity = vector(rotated_velocity[0],rotated_velocity[1])
        self.mass = mass
        self.id = id

# Function to calculate the acceleration of body_1 due to the gravitational attraction of body_2
def acceleration_calculation(body_1, body_2):
    G = 6.67408e-11 #m3 kg-1 s-2
    accel_vector = vector(0,0)
    # We calculate the distance between the bodies
    distance = math.sqrt((body_1.position.x - body_2.position.x)**2 + (body_1.position.y - body_2.position.y)**2)
    # We calculate the acceleration vector components in each dimension
    accel_vector.x = (body_2.mass * G / distance**3) * (body_2.position.x - body_1.position.x)
    accel_vector.y = (body_2.mass * G / distance**3) * (body_2.position.y - body_1.position.y)
    return accel_vector

# Function to update the speed of a body based on it's acceleration vector
def velocity_calculation(body, accel_vector, time_step = 1):
    body.velocity.x += accel_vector.x * time_step
    body.velocity.y += accel_vector.y * time_step
    return body.velocity

# Function to update the position of a body based on it's speed vector
def position_calculation(body, time_step = 1):
    body.position.x += body.velocity.x * time_step
    body.position.y += body.velocity.y * time_step
    return body.position

# Function to run the simulation over a list of bodies in a number of time steps of a certain size, plotting each n time steps
def compute_n_body_problem(bodies, time_step_size = 1, time_steps_number = 10000, frequency = 100):
    position_data=[[],[],[],[]]
    for time_step in range(1,time_steps_number):
        for body_1 in bodies:
            accel_vector = vector(0,0)
            for body_2 in bodies:
                if body_1.id != body_2.id:
                    accel_vector.vector_sum(acceleration_calculation(body_1,body_2))
            body_1.velocity = velocity_calculation(body_1,accel_vector,time_step_size)
            body_1.position = position_calculation(body_1,time_step_size)
            if time_step % frequency == 0:
                position_data[0].append(body_1.position.x)
                position_data[1].append(body_1.position.y)
                position_data[2].append(body_1.id)
                position_data[3].append(time_step)
    return position_data

# Define the data and run the simulation
if __name__ == "__main__":
    bodies = [
        body(vector(0,0),vector(0,0),2e30,0,'Sun'),
        body(vector(0,1.5e11),vector(30000,0),6e24,0,'Earth'),
        body(vector(0,1.501e11),vector(39010,0),1e3,0,'Probe'),
        body(vector(0,7.78e11),vector(13000,0),1.898e27,-101,'Jupiter'),
        #body(vector(0,(1.5e11-3.85e8)),vector(31000,0),7.34e22,0,'Moon')
    ]
    solution_data = compute_n_body_problem(bodies,100,3200000,1000)
    fig = px.line(x=solution_data[0],y=solution_data[1],color=solution_data[2])
    fig.show()

