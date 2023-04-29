#!/usr/bin/env python3
import info

import socket
import os

from typing import Final
from log4python.Log4python import log

from datetime import datetime

"""
Default logger for system.
"""
__LOGGER: Final[log] = log(module_name='NetScan')  # Create logger


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
        return response(True, delta_time)  # Build response with running=True and no ping=delta_time
    except socket.error:
        __LOGGER.error(f'The connection({address}:{port}) is not available!')
        return response(False)  # Build response with running=False and no ping=-1(invalid)
        pass

    finally:
        __terminate_socket(test_socket)  # Close and kill socket with method


# Response dict of parameters.
def response(running: bool, ping: float = -1):
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


def port_in_range(port_to_check: int):
    """

    :param port_to_check:
    :return:
    """
    return 0 < port_to_check < 65535


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


# Start statement if this file was called as main
if __name__ == '__main__':
    import sys

    __LOGGER.info('Since "netscan.py" has been executed, it can be operated directly with the input')
    __LOGGER.info(f'Starting NetScan v{info.VERSION} ...')
    __LOGGER.info(f'OS platform: {sys.platform}. (Py-Version: {sys.version.split(" ")[0]})')

    __LOGGER.info('<CTRL + C> or type "kill" to terminate program.')
    __LOGGER.info('Type "clear" to remove configuration.')

    host: str = ''
    port: int = -1

    __LOGGER.info(f'Enter host:')
    while True:
        console_input = input().lower()
        if console_input == 'kill':
            exit()
        elif console_input == 'clear':
            host = ''
            port = -1
            __LOGGER.info(f'Cleared configuration, to start over enter host:')
            continue

        if host == '':
            host = console_input
            __LOGGER.info(f'Set {host} as host, enter port to scan:')
            continue

        if port is not port_in_range(port):
            try:
                port_input = int(console_input)

                if port_in_range(port_input):
                    port = port_input
                    __LOGGER.info(f'Set {port} as port.')

                    validate_connection(address=host, port=port)
                    host = ''
                    port = -1
                    __LOGGER.info(f'Waiting for next host:')
                else:
                    __LOGGER.error(f'Given port {port_input} is not in range 1...65535.')
            except ValueError:
                __LOGGER.error(f'{console_input} is not a number.')
            continue
