from tornado import websocket, web, ioloop
import threading
from simulator import SimulatorEngine

class IndexHandler(web.RequestHandler):
    def get(self):
        self.render("index.html")

class WebsocketHandler(websocket.WebSocketHandler):

    def broadcaster(self):
        return event_broadcaster

    def simulator(self):
        return simulator

    def open(self):
        print 'new connection'
        msg = {'text':'Starting simulation'}
        self.broadcaster().open(self)
        self.simulator().start()
        self.write_message(msg)

    def on_close(self):
        print 'connection closed'
        self.broadcaster().close(self)
        self.simulator().stop()

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


event_broadcaster = EventBroadcaster()
simulator = SimulatorEngine()
simulator.prepare(event_broadcaster)

app = web.Application([
    (r'/', IndexHandler),
    (r'/ws', WebsocketHandler),
    (r'/public/(.*)', web.StaticFileHandler, {'path': 'public'}),
])

if __name__ == "__main__":
    app.listen(8888)
    ioloop.IOLoop.instance().start()
