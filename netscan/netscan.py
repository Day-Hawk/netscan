#!/usr/bin/env python3
import info
import socket
from typing import Final
from datetime import datetime

from log4python.Log4python import log

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

    # Response dict of parameter
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
        try:
            test_socket.shutdown(socket.SHUT_RDWR)  # Shutdown socket.
        except OSError:
            pass  # Ignore error
        test_socket.close()  # At least close socket.
        __LOGGER.debug('Successfully killed socket.')


class SocketConfiguration(object):
    """
    Configuration for socket.
    """

    host: str
    port: int

    def __init__(self):
        """
        Initialize configuration.
        """
        self.host = ''
        self.port = -1

    # Method to update configuration port.
    def update_port(self, port):
        """
        Update port of this configuration.

        :param port: to update.
        :return: True, if port is a number and in port range.
        """
        unchecked_port = int(port)  # If input is not a number -> Except block

        if 0 < unchecked_port < 65535:  # Check if input is in range.
            self.port = unchecked_port  # If given port is valid use port for scan.
            return True
        return False

    # Connect with local configuration.
    def connect(self):
        """
        Connect with local configuration.

        :return: dict with 'running':<True if service is running> 'ping':<Ping as float>
        """
        validate_connection(address=self.host, port=self.port)  # Scan


# Start statement if this file was called as main
if __name__ == '__main__':
    import sys

    __LOGGER.info('Since "netscan.py" has been executed, it can be operated directly with the input.')
    __LOGGER.info(f'Starting NetScan v{info.VERSION} ...')
    __LOGGER.info(f'OS platform: {sys.platform}. (Py-Version: {sys.version.split(" ")[0]})')
    __LOGGER.info('Commands: clear(Clear configuration) and kill(same as <CTRL + C>)')
    __LOGGER.info('<CTRL + C> to terminate program.')

    connection = None

    __LOGGER.info(f'Enter first host:')
    while True:
        if connection is None:  # Check if configuration is present.
            connection = SocketConfiguration()  # If no configuration is present, create new.

        console_input = ''

        try:
            console_input = input().lower()
        except KeyboardInterrupt:
            exit()  # Exit program.
            pass

        if console_input == 'kill':
            exit()  # Kill task.
        elif console_input == 'clear':
            connection = None
            __LOGGER.info(f'Cleared configuration, to start over enter host:')
            continue

        if connection.host == '':
            connection.host = 'localhost' if console_input == '' else console_input
            __LOGGER.info(f'Set {connection.host} as host, enter port to scan:')
            continue

        if connection.port < 0:
            try:
                if connection.update_port(80 if console_input == '' else console_input):
                    __LOGGER.info(f'Set {connection.port} as port.')
                    connection.connect()  # Scan
                    connection = None  # Reset configuration
                    __LOGGER.info(f'Waiting for next host:')
                else:
                    __LOGGER.error(f'Given port {console_input} is not in range 1...65535.')
            except ValueError:  # Given input was not a number.
                __LOGGER.error(f'{console_input} is not a number.')
            continue
