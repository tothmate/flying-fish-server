import SocketServer

class FlyingFishHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print self.data

server = SocketServer.TCPServer(("localhost", 6767), FlyingFishHandler)
server.serve_forever()