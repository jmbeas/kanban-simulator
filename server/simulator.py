from simpy import Environment, Process
from car import Car

class SimulatorEngine(Environment):
    def __init__(self,event_broadcaster):
        self.event_broadcaster = event_broadcaster
        Environment.__init__(self)

    def prepare(self):
        car = Car(env=self)
        self.process(car.driver(self))

    def start(self):
        self.run(until=20)

    def stop(self):
        self.exit()
