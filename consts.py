"""
name: consts.py
purpose: provides the consts for this thingy
"""
SERVER_IP = '0.0.0.0'
SERVER_PORT = 1337

PING_MESSAGE_VALUE = 'ping'.encode()
PONG_MESSAGE_VALUE = 'pong'.encode()

TIMEOUT = float(5)
MAX_RECEIVE_AMOUNT = 15000


class ErrorMessages:
    INVALID_MESSAGE_ERROR_MESSAGE = 'invalid message received'
