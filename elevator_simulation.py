import simpy
import random
import statistics

class Elevator(object):
    def __init__(self, env, num_floors, floor_capacity, move_time, door_time):
        self.env = env
        self.floor_capacity = floor_capacity
        self.current_floor = 0
        self.direction = 1  # 1 for going up, -1 for going down
        self.move_time = move_time
        self.door_time = door_time
        self.waiting_times = []

    def move_to_floor(self, floor):
        floor_difference = abs(floor - self.current_floor)
        move_time = floor_difference * self.move_time
        yield self.env.timeout(move_time)
        self.current_floor = floor
        #print(f"Elevator arrived at floor {floor}")

    def process_request(self, floor):
        if self.direction == 1 and floor >= self.current_floor:
            yield from self.move_to_floor(floor)
        elif self.direction == -1 and floor <= self.current_floor:
            yield from self.move_to_floor(floor)
        else:
            print("Invalid request")

    def run(self):
        while True:
            yield self.env.timeout(self.move_time)
            if len(self.floor_capacity[self.current_floor]) > 0:
                request = self.floor_capacity[self.current_floor].pop(0)
                print(f"Elevator picked up request from floor {self.current_floor}")
                yield from self.process_request(request)

def passenger_arrival(env, num_floors, floor_capacity, inter_arrival_time):
    while True:
        floor = random.randint(1, num_floors-1)
        floor_capacity[floor].append(env.now)
        #print(f"Passenger arrived at floor {floor}")
        yield env.timeout(random.expovariate(1 / inter_arrival_time))

# Simulation setup
num_floors = 21
move_time = 2  # Assume 2 time units per floor
door_time = 10  # Assume 1 time unit to open/close the doors
inter_arrival_time = 0.005 * 20  # Mean inter-arrival time for passengers (Poisson process)

env = simpy.Environment()
floor_capacity = [[] for _ in range(num_floors)]
elevator = Elevator(env, num_floors, floor_capacity, move_time, door_time)

env.process(elevator.run())
env.process(passenger_arrival(env, num_floors, floor_capacity, inter_arrival_time))
env.run(until=100000)  # Run the simulation for 30 time units

# Calculate average waiting time
waiting_times = []
for floor in floor_capacity:
    for request_time in floor:
        waiting_time = env.now - request_time
        waiting_times.append(waiting_time)

average_waiting_time = statistics.mean(waiting_times)

print(f"Average waiting time: {average_waiting_time} time units")