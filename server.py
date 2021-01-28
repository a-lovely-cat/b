"""
name: server.py
purpose: ping pong :)
"""
import select
import socket
import logging
import os

SERVER_IP = '0.0.0.0'
SERVER_PORT = 1337

PING_MESSAGE_VALUE = 'ping'.encode()
PONG_MESSAGE_VALUE = 'pong'.encode()

MAX_RECEIVE_AMOUNT = 15000
PING_PONG_TIMEOUT = float(5)

INVALID_MESSAGE_ERROR_MESSAGE = 'invalid message received'
TIMEOUT_REACHED_ERROR_MESSAGE = 'timeout reached'


def accept_client(server_socket):
    """
    this function uses select to only accept the client when possible
    :param server_socket: the server's socket
    :return: the client's socket and address
    """
    select.select([server_socket], [], [])
    client_socket, client_address = server_socket.accept()
    return client_socket, client_address


def get_ping(client_socket):
    """
    this function uses select to get the client's ping when possible
    :param client_socket: the client's socket
    :except ValueError: in the case when there is a timeout or a bad message (not ping)
    """
    client_select = select.select([client_socket], [], [], PING_PONG_TIMEOUT)
    if client_select == ([], [], []):
        raise ValueError(TIMEOUT_REACHED_ERROR_MESSAGE)
    client_answer = client_socket.recv(MAX_RECEIVE_AMOUNT)
    if client_answer != PING_MESSAGE_VALUE:
        raise ValueError(INVALID_MESSAGE_ERROR_MESSAGE)


def send_pong(client_socket):
    """
    this function sends the client a pong when he can accept it
    :param client_socket: the client's socket
    :except ValueError: in the case when there is a timeout
    """
    client_select = select.select([], [client_socket], [], PING_PONG_TIMEOUT)
    client_socket.send(PONG_MESSAGE_VALUE)
    if client_select == ([], [], []):
        raise ValueError(TIMEOUT_REACHED_ERROR_MESSAGE)


def main():
    logging.basicConfig(filename=f'{os.getcwd()}\\logs.txt')
    logging.disable(level=logging.NOTSET)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(1)

    while True:
        client_socket, client_address = accept_client(server_socket)

        try:
            logging.info(f'getting ping {client_address}')
            get_ping(client_socket)

            logging.info(f'sending pong to {client_address}')
            send_pong(client_socket)
            logging.info(f'ping pong success with {client_address}')

        except ValueError as err:
            if err.args[0] == INVALID_MESSAGE_ERROR_MESSAGE:
                logging.error(f'{client_address} - has failed the ping pong')
            elif err.args[0] == TIMEOUT_REACHED_ERROR_MESSAGE:
                logging.error(f'{client_address} - has timed out before the ping')

        logging.info(f'closing connection with {client_address}')
        client_socket.close()


if __name__ == '__main__':
    main()
