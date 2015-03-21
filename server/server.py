from tornado import websocket, web, ioloop
import time, datetime
import threading
import simpy

cl = []

def inform(msg):
    print msg
    for c in cl:
        c.write_message(msg)


class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebsocketHandler(websocket.WebSocketHandler):
    def open(self):
        print 'new connection'
        msg = {'text':'Starting simulation'}
        if self not in cl:
             cl.append(self)
        self.write_message(msg)
        env.run(until=15)

    def on_close(self):
        print 'connection closed'
        if self in cl:
            cl.remove(self)
        simulator.stop()

    def check_origin(self, origin):
        return True


class Car(object):

    def __init__(self,env):
        print "Creating a new car"
        self.env = env
        self.action = env.process(self.run())

    def run(self):
        while True:
            inform({'text':'Start parking and charging at %d' % self.env.now})
            charge_duration = 5
            try:
                yield self.env.process(self.charge(charge_duration))
            except simpy.Interrupt:
                inform({'text':'Was interrupted. Hope, the battery is full enough ...'})

            inform({'text':'Start driving at %d' % self.env.now})
            trip_duration = 2
            yield self.env.timeout(trip_duration)

    def charge(self,duration):
        yield self.env.timeout(duration)


def driver(env, car):
    yield env.timeout(3)
    car.action.interrupt()

env = simpy.Environment()
car = Car(env)
env.process(driver(env,car))

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', WebsocketHandler),
    (r'/public/(.*)', web.StaticFileHandler, {'path': 'public'}),
])

if __name__ == "__main__":
    app.listen(8888)
    ioloop.IOLoop.instance().start()
