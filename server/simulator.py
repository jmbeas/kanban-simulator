from simpy import Environment, Process
from car import Car

class SimulatorEngine(Environment):
    def __init__(self,event_broadcaster):
        self.event_broadcaster = event_broadcaster
        Environment.__init__(self)

    def prepare(self):
        car = Car(env=self)
        self.process(self.driver(car))

    def start(self):
        self.run(until=20)

    def stop(self):
        self.exit()

    def driver(self, car):
        yield self.timeout(3)
        car.action.interrupt()

## ---- Bank Simulation

# class Customer(Process):
#     def __init__(self,name,sim):
#         self.name = name
#         self.sim = sim
#
#     def visits(self):
#         print("%2.1f %s entra" % (self.sim.now, self.name))
#         yield self.sim.timeout(10)
#         print("%2.1f %s se marcha" % (self.sim.now, self.name))
#
# class BankModel(Environment):
#     def start(self):
#         c = Customer(name="Klaus", sim=self)
#         print "Customer %s created" % c.name
#         self.process(c.visits())
#         self.run(until=100)
#
# bank_model = BankModel()
# bank_model.start()
