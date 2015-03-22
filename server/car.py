import simpy

class Car(object):

    def __init__(self,env,event_broadcaster):
        print "Creating a new car"
        self.env = env
        self.event_broadcaster = event_broadcaster
        self.action = env.process(self.run())

    def run(self):
        while True:
            self.event_broadcaster.inform({'type':'charging','text':'Start parking and charging','timestamp':'%d' % self.env.now})
            charge_duration = 5
            try:
                yield self.env.process(self.charge(charge_duration))
            except simpy.Interrupt:
                self.event_broadcaster.inform({'type':'interruption','text':'Was interrupted. Hope, the battery is full enough ...','timestamp':'%d' % self.env.now})
            self.event_broadcaster.inform({'text':'Start driving','timestamp':'%d' % self.env.now})
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self,duration):
        yield self.env.timeout(duration)
