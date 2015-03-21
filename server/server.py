from tornado import websocket, web, ioloop
import time, datetime
import threading
import simpy
from car import Car

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebsocketHandler(websocket.WebSocketHandler):

    def broadcaster(self):
        return event_broadcaster

    def open(self):
        print 'new connection'
        msg = {'text':'Starting simulation'}
        self.broadcaster().open(self)
        self.write_message(msg)
        env.run(until=15)

    def on_close(self):
        print 'connection closed'
        self.broadcaster().close(self)
        simulator.stop()

    def check_origin(self, origin):
        return True

class EventBroadcaster(object):

    def __init__(self):
        self.cl = []

    def open(self,c):
        if c not in self.cl:
             self.cl.append(c)

    def close(self,c):
        if c in self.cl:
            self.cl.remove(c)

    def inform(self,msg):
        print msg
        for c in self.cl:
            c.write_message(msg)



def driver(env, car):
    yield env.timeout(3)
    car.action.interrupt()

env = simpy.Environment()
event_broadcaster = EventBroadcaster()
car = Car(env,event_broadcaster)
env.process(driver(env,car))

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', WebsocketHandler),
    (r'/public/(.*)', web.StaticFileHandler, {'path': 'public'}),
])

if __name__ == "__main__":
    app.listen(8888)
    ioloop.IOLoop.instance().start()
