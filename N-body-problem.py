import math
import plotly.express as px

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
    def __init__(self, position, velocity, mass = 1, id = ''):
        self.position = position
        self.velocity = velocity
        self.mass = mass
        self.id = id

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
    position_data=[[],[],[],[],[]]
    for time_step in range(1,time_steps_number):
        for body_1 in bodies:
            accel_vector = vector(0,0,0)
            for body_2 in bodies:
                if body_1.id != body_2.id:
                    accel_vector.vector_sum(acceleration_calculation(body_1,body_2))
            body_1.velocity = velocity_calculation(body_1,accel_vector,time_step_size)
            body_1.position = position_calculation(body_1,time_step_size)
            if time_step % frequency == 0:
                position_data[0].append(body_1.position.x)
                position_data[1].append(body_1.position.y)
                position_data[2].append(body_1.position.z)
                position_data[3].append(body_1.id)
                position_data[4].append(time_step)
    return position_data

# Define the data and run the simulation
if __name__ == "__main__":
    bodies = [
        body(vector(0,0,0),vector(0,0,0),2e30,'Sun'),
        body(vector(0,-7.78e11,0),vector(-13000,0,0),2e30,'Sun2'),
        body(vector(0,1.5e11,0),vector(30000,0,0),6e24,'Earth'),
        body(vector(0,(1.5e11-3.85e8),0),vector(31000,0,0),7.34e22,'Moon')
    ]
    solution_data = compute_n_body_problem(bodies,100,960000,1000)
    #fig = px.scatter_3d(x=solution_data[0],y=solution_data[1],z=solution_data[2],color=solution_data[3],animation_frame=solution_data[4])
    fig = px.line_3d(x=solution_data[0],y=solution_data[1],z=solution_data[2],color=solution_data[3])
    fig.update_layout(
    scene = dict(
        xaxis = dict(nticks=4, range=[min(solution_data[0]),max(solution_data[0])],autorange=False),
        yaxis = dict(nticks=4, range=[min(solution_data[1]),max(solution_data[1])],autorange=False),
        zaxis = dict(nticks=4, range=[min(solution_data[2]),max(solution_data[2])],autorange=False),),
        margin = dict(r=20, l=10, b=10, t=10))
    fig.update_layout(scene_aspectmode='cube')
    #fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 10
    fig.show()

