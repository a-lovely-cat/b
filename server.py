"""
name: server.py
purpose: ping pong :)
         it also makes it with threads
"""
import select
import socket
import logging
import threading

import consts
from tennis_client import TennisClient


def accept_client(server_socket):
    """
    this function uses select to only accept the client when possible
    :param server_socket: the server's socket
    :return: the client's socket and address
    """
    select.select([server_socket], [], [])
    client_socket, client_address = server_socket.accept()
    return client_socket, client_address


def ping_pong(client_socket, client_address):
    """
    **multithreading main**
    this function acts as the main for a single connection
    it does the whole ping pon cycle infinitely
    :param client_socket: the client's socket
    :param client_address: the client's address
    """
    tennis_client = TennisClient(client_socket)

    while True:

        try:
            logging.info(f'getting ping {client_address}')
            tennis_client.get_ping()

            logging.info(f'sending pong to {client_address}')
            tennis_client.send_pong()
            logging.info(f'ping pong success with {client_address}')

        except ValueError as err:
            if err.args[0] == consts.ErrorMessages.INVALID_MESSAGE_ERROR_MESSAGE:
                logging.error(f'{client_address} - has failed the ping pong')
            logging.info(f'closing connection with {client_address}')
            client_socket.close()
            return


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((consts.SERVER_IP, consts.SERVER_PORT))
    server_socket.listen(4)

    while True:
        client_socket, client_address = accept_client(server_socket)

        logging.info(f'starting session for {client_address}')
        threading.Thread(target=ping_pong, args=(client_socket, client_address)).start()


if __name__ == '__main__':
    main()
