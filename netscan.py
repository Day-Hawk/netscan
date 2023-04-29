#!/usr/bin/env python3
import socket
import os

from typing import Final
from log4python.Log4python import log

from datetime import datetime

"""
Default logger for system.
"""
__LOGGER: Final[log] = log(module_name='NetScan')  # Create logger

#  Version of server
__VERSION: Final[str] = '1.0.0'


def validate_connection(address: str, port: int = 80, timeout: int = 1):
    """
    If the timeout time is reached, the connection is considered as not possible.

    :param address: addressed by the request.
    :param port: of the application from the address.
    :param timeout: Time to wait for response of partner.
    :return:
    """
    test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Instance of socket.
    request_time = datetime.now()
    try:
        __LOGGER.debug(f'Try to connect to {address}, {port}. [Timeout: {timeout}s]')
        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create socket instance.
        test_socket.settimeout(timeout)  # Define timeout parameter.
        test_socket.connect((address, port))  # Use socket to connect to given address and port.

        delta_time = (datetime.now() - request_time).total_seconds() * 1000
        __LOGGER.info(f'The connection({address}:{port}) can be established! [{delta_time:.3f}ms ping.]')
        return __build_response(True, delta_time)  # Build response with running=True and no ping=delta_time
    except socket.error:
        __LOGGER.error(f'The connection({address}:{port}) is not available!')
        return __build_response(False)  # Build response with running=False and no ping=-1(invalid)
        pass

    finally:
        __terminate_socket(test_socket)  # Close and kill socket with method


def __build_response(running: bool, ping: float = -1):
    """
    Create dict with parameters.

    :param running: True, if connection is valid. False if connection is not available or valid.
    :param ping: Given time for request and response in ms.
    :return: Object combining running and ping.
    """
    return {
        'running': running,
        'ping': ping
    }


def __terminate_socket(socket_to_kill: socket.socket):
    """
    Shutdown and close an existing connection.

    :param socket_to_kill: socket to disconnect and kill.
    :return: None, no return value.
    """

    if socket_to_kill is None:  # No socket to kill. Ignore call.
        return

    try:
        socket_to_kill.shutdown(socket.SHUT_RDWR)  # Shutdown socket.
    except OSError:
        pass  # Ignore error
    socket_to_kill.close()  # At least close socket.
    __LOGGER.debug('Successfully killed socket.')


# Main start method
def __start():
    """
    Start method with parameters.
    :return: None
    """
    __LOGGER.info(f'Starting NetScan v{__VERSION} ...')

    import sys
    __LOGGER.info(f'OS platform: {sys.platform}. (Py-Version: {sys.version.split(" ")[0]})')

    host: str = 'localhost'
    port: int = 8529

    validate_connection(address=host, port=port)


"""
    __LOGGER.info('Waiting for input with valid host.')
    while host == '':
        try:
            __input = str(input())

            if __input == '':
                __input = 'localhost'

            host = __input
        except:
            continue

    __LOGGER.info(f'Waiting for input with valid port for host {host}.')

    while port < 0:
        try:
            __input = str(input())

            __input_int = 80 if __input == '' else int(input())

            port = __input_int
        except:
            continue
"""

__ENV_HOST: Final[str] = 'NETSCAN_HOST'
__ENV_PORT: Final[str] = 'NETSCAN_PORT'


def __collect_environment():
    """

    :return:
    """

    host = os.getenv(__ENV_HOST)
    port = os.getenv(__ENV_PORT)

    if host is None or port is None:
        raise RuntimeError('Can not build from environment.')

    try:
        return {'host': str(host), 'port': int(port)}
    except ValueError:
        raise RuntimeError('Port is not a number.')


def __build_object(host: str, port: int):
    """

    :param host:
    :param port:
    :return:
    """
    return {'host': host, 'port': port}


# Start statement
if __name__ == '__main__':
    __start()  # Call start
