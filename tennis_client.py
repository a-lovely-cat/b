"""
name: tennis_client.py
purpose: handler a single tennis connection's actions with select
"""
import select
import consts


class TennisClient:

    def __init__(self, client_socket):
        self.client_socket = client_socket

    def get_ping(self):
        """
        this function uses select to get the client's ping when possible
        :except ValueError: in the case when there is a timeout or a bad message (not ping)
        """
        select.select([self.client_socket], [], [])
        client_answer = self.client_socket.recv(consts.MAX_RECEIVE_AMOUNT)
        if client_answer != consts.PING_MESSAGE_VALUE:
            raise ValueError(consts.ErrorMessages.INVALID_MESSAGE_ERROR_MESSAGE)

    def send_pong(self):
        """
        this function sends the client a pong when he can accept it
        :except ValueError: in the case when there is a timeout
        """
        select.select([], [self.client_socket], [])
        self.client_socket.send(consts.PONG_MESSAGE_VALUE)
