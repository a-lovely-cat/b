import socket, time

sockets = [socket.socket() for i in xrange(900)]
for sock in sockets:
    sock.connect(("localhost", 1337))

time.sleep(5)
