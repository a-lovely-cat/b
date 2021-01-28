"""
name: tennis_client.py
purpose: handles all the connections of ping pong clients
"""
import select
import consts
import logging

logging.basicConfig(level=logging.DEBUG)


class TennisServer:

    def __init__(self, server_socket):
        self.server_socket = server_socket
        self.client_sockets = {}

    def get_pings(self):
        """
        this function recieves pings and sends pongs to all clients available
        """
        for sock in select.select([*self.client_sockets.keys()], [], [], consts.TIMEOUT)[0]:
            client_answer = sock.recv(consts.MAX_RECEIVE_AMOUNT)
            if client_answer != consts.PING_MESSAGE_VALUE:
                logging.error(f'{self.client_sockets[sock]} has been disconnected')
                del self.client_sockets[sock]
                sock.close()
            else:
                sock.send(consts.PONG_MESSAGE_VALUE)

    def accept_client(self):
        """
        this function uses select to only accept the client when possible
        it adds them to the list
        """
        if self.client_sockets == {}:
            client_socket, client_address = self.server_socket.accept()
            self.client_sockets[client_socket] = client_address

        for sock in select.select([self.server_socket], [], [], 0)[0]:
            client_socket, client_address = sock.accept()
            self.client_sockets[client_socket] = client_address
