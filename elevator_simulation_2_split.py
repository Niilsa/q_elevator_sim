import simpy
import random

class Elevator:
    def __init__(self, env, floors):
        self.env = env
        self.floors = floors
        self.current_floor = 22
        self.current_queue = []
        self.waiting_queue = []
        self.action = env.process(self.run())
        self.current_time_tick = 150
        self.total_time_spend = 0  # summation of (the time in the system of all people)
        self.total_arrival = 0

    def run(self):
        while True:
            if self.current_queue:
                destination = self.current_queue.pop()
                num_of_people_leave_this_floor = 1
                while self.current_queue and self.current_queue[-1] == destination:
                    num_of_people_leave_this_floor += 1
                    self.current_queue.pop()

                if self.current_floor == 1 and self.floors == 10:
                    self.current_time_tick += 11*2

                yield self.env.timeout(2 * abs(destination - self.current_floor))  # Time to move between floors
                self.current_time_tick += 2 * abs(destination - self.current_floor)
                self.total_time_spend += self.current_time_tick * num_of_people_leave_this_floor

                yield self.env.timeout(10)  # Time for opening and closing doors
                self.current_time_tick += 10

                self.current_floor = destination

            else:
                if self.current_time_tick == 0:
                    self.total_time_spend += 1
                else:
                    yield self.env.timeout(self.current_time_tick)
                    self.total_time_spend += len(self.waiting_queue)*self.current_time_tick  # The mean time that people wait in the first floor equals to current_time_tick (because the elevator just arrive the highest floor now)
                    self.current_time_tick = 0

                    self.current_queue += self.waiting_queue
                    self.total_arrival += len(self.waiting_queue)
                    self.current_queue = sorted(self.current_queue, reverse=True)
                    self.waiting_queue = []

                    self.current_floor = 1

    def request_elevator(self, floor):
        self.waiting_queue.append(floor)


def passenger_arrival(env, elevator, lambda_sum):
    while True:
        yield env.timeout(random.expovariate(lambda_sum))  # Inter-arrival time follows a Poisson process
        floor = random.randint(13, 22)  # Randomly select a destination floor
        elevator.request_elevator(floor)


def solver(lambda_sum):
    random.seed(42)
    env = simpy.Environment()
    elevator = Elevator(env, floors=10)

    env.process(passenger_arrival(env, elevator, lambda_sum))

    env.run(until=100000)  # Run the simulation for n time units

    avg_time_in_system = elevator.total_time_spend / elevator.total_arrival

    return avg_time_in_system


if __name__ == "__main__":
    avg_time_in_system = solver(0.1)
    print(f'ET: {avg_time_in_system}')