from simpy import Environment, Process, Interrupt

class Car(Process):

    def __init__(self,env):
        print "Creating a new car"
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        while True:
            self.env.event_broadcaster.inform({'type':'charging','text':'Start parking and charging','timestamp':'%d' % self.env.now})
            charge_duration = 5
            try:
                yield self.env.process(self.charge(charge_duration))
            except Interrupt:
                self.env.event_broadcaster.inform({'type':'interruption','text':'Was interrupted. Hope, the battery is full enough ...','timestamp':'%d' % self.env.now})
            self.env.event_broadcaster.inform({'text':'Start driving','timestamp':'%d' % self.env.now})
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self,duration):
        yield self.env.timeout(duration)

    def driver(self, env):
        yield env.timeout(3)
        self.action.interrupt()
