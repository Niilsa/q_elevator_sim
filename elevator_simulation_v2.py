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
        self.current_time_tick = 60
        self.total_time_spend = 0  # summation of (the time in the system of all people)
        self.total_arrival = 0

    def run(self):
        while True:
            if self.current_queue:
                destination = self.current_queue.pop()
                if destination != self.current_floor:
                    yield self.env.timeout(10)  # Time for opening and closing doors
                    self.current_time_tick += 10
                    yield self.env.timeout(2 * abs(destination - self.current_floor))  # Time to move between floors
                    self.current_time_tick += 2 * abs(destination - self.current_floor)
                    self.current_floor = destination
                self.total_time_spend += self.current_time_tick
            else:
                # yield self.env.timeout(10)
                # yield self.env.timeout(2 * abs(self.current_floor - 1))
                yield self.env.timeout(self.current_time_tick)
                self.total_time_spend += len(self.waiting_queue)*self.current_time_tick/2  # The mean time that people wait in the first floor equals to current_time_tick/2 (because the elevator just arrive the highest floor now)
                self.current_time_tick = 0
                self.current_queue += self.waiting_queue
                self.total_arrival += len(self.waiting_queue)
                self.current_queue = sorted(self.current_queue, reverse=True)
                self.waiting_queue = []

    def request_elevator(self, floor):
        self.waiting_queue.append(floor)


def passenger_arrival(env, elevator):
    while True:
        yield env.timeout(random.expovariate(0.105))  # Inter-arrival time follows a Poisson process
        floor = random.randint(2, 22)  # Randomly select a destination floor
        elevator.request_elevator(floor)


def main():
    random.seed(42)
    env = simpy.Environment()
    elevator = Elevator(env, floors=22)

    env.process(passenger_arrival(env, elevator))

    env.run(until=100000)  # Run the simulation for n time units

    avg_time_in_system = elevator.total_time_spend / elevator.total_arrival
    print(f'ET: {avg_time_in_system}')

    # # Calculate average time in current_queue and average time in the whole system
    # total_service_time = 0
    # total_time_in_system = 0
    # num_passengers = len(elevator.current_queue)
    #
    # for floor in elevator.current_queue:
    #     total_service_time += (2 * abs(floor - 1) + 20)  # Time to move to the floor and open/close doors
    #
    # total_time_in_system = total_service_time + num_passengers * (20 + 2 * abs(1 - elevator.current_floor))
    #
    # avg_service_time = total_service_time / num_passengers if num_passengers > 0 else 0
    # avg_time_in_system = total_time_in_system / num_passengers if num_passengers > 0 else 0
    #
    # print("Average Service Time:", round(avg_service_time))
    # print("Average Time in System:", round(avg_time_in_system))


if __name__ == "__main__":
    main()
