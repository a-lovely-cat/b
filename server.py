"""
name: server.py
purpose: ping pong :)
"""
import socket
import logging

import consts
from tennis_client import TennisServer


def ping_pong(server_socket):
    """
    this function acts as the main for a single connection
    it does the whole ping pon cycle infinitely
    :param server_socket: the server's socket
    """
    tennis_server = TennisServer(server_socket)

    while True:
        tennis_server.accept_client()

        logging.info(f'ping ponging')
        tennis_server.get_pings()


def main():
    logging.basicConfig(level=logging.DEBUG)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((consts.SERVER_IP, consts.SERVER_PORT))
    server_socket.listen(4)

    ping_pong(server_socket)


if __name__ == '__main__':
    main()
