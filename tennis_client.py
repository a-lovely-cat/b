"""
name: tennis_client.py
purpose: handles all the connections of ping pong clients
"""
import select
import consts
import logging
import time
import socket

logging.basicConfig(level=logging.DEBUG)


class TennisServer:

    def __init__(self, server_socket):
        self.server_socket = server_socket
        self.client_sockets = {}
        self.clients_poll = select.poll()

    def get_pings(self):
        """
        this function recieves pings and sends pongs to all clients available
        """
        for sock in self.clients_poll.poll():
            client_answer = None
            if sock[1] == select.POLLIN:
                client_sock = socket.socket(fileno=sock[0])
                client_answer = client_sock.recv(consts.MAX_RECEIVE_AMOUNT)
            if client_answer != consts.PING_MESSAGE_VALUE and client_answer is not None:
                logging.error(f'{self.client_sockets[sock]} has been disconnected')
                del self.client_sockets[sock]
                self.clients_poll.unregister(sock[0])
                client_sock.close()
            else:
                client_sock.send(consts.PONG_MESSAGE_VALUE)

    def accept_client(self):
        """
        this function uses select to only accept the client when possible
        it adds them to the list
        """
        if self.client_sockets == {}:
            client_socket, client_address = self.server_socket.accept()
            self.client_sockets[client_socket] = client_address

        time.sleep(0.1)
        while select.select([self.server_socket], [], [], 0)[0] != []:
            print(1)
            client_socket, client_address = self.server_socket.accept()
            self.client_sockets[client_socket] = client_address
            self.clients_poll.register(client_socket)
            time.sleep(0.13)
