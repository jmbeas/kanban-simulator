import simpy
from car import Car

class SimulatorEngine(object):
    def __init__(self):
        self.env = simpy.Environment()

    def prepare(self, event_broadcaster):
        car = Car(self.env,event_broadcaster)
        self.env.process(self.driver(self.env,car))

    def start(self):
        self.env.run(until=15)

    def stop(self):
        pass

    def driver(self, env, car):
        yield env.timeout(3)
        car.action.interrupt()
