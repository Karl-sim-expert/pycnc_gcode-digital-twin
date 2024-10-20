

import os
import sys
import readline
import atexit

import cnc.logging_config as logging_config
from cnc.gcode import GCode, GCodeException
from cnc.gmachine import GMachine, GMachineException

import socket

# [CHG] socket client setting 
HOST = '127.0.0.1'  
PORT = 65432       

try:  # python3 compatibility
    type(raw_input)
except NameError:
    # noinspection PyShadowingBuiltins
    raw_input = input


# configure history file for interactive mode
# [CHG] change the directory for storage 
curr_dir = os.getcwd()
his_dir = os.path.join(curr_dir, 'history')
history_file = os.path.join(his_dir, '.pycnc_history')
try:
    readline.read_history_file(history_file)
except IOError:
    pass
readline.set_history_length(1000)
atexit.register(readline.write_history_file, history_file)

machine = GMachine()

#  [CHG] Add client socket variable to the function argument (do_line, do_command) 
def do_line(line, client_socket):
    try:
        g = GCode.parse_line(line)
        res = machine.do_command(g, client_socket)
    except (GCodeException, GMachineException) as e:
        print('ERROR ' + str(e))
        return False
    if res is not None:
        print('OK ' + res)
    else:
        print('OK')
    return True

#  [CHG] Add client socket variable to the main function
def main(client_socket):
    logging_config.debug_disable()
    try:
        if len(sys.argv) > 1:
            # Read file with gcode
            print(f"Received file path: {sys.argv[1]}")
            with open(sys.argv[1], 'r') as f:
                for line in f:
                    line = line.strip()
                    print('> ' + line)
                    if not do_line(line, client_socket):
                        break
                #[CHG] handle quit command 
                if (client_socket != None):
                    client_socket.sendall(''.encode('utf-8'))
        else:
            # Main loop for interactive shell
            # Use stdin/stdout, additional interfaces like
            # UART, Socket or any other can be added.
            print("*************** Welcome to PyCNC! ***************")
            while True:
                line = raw_input('> ')
                if line == 'quit' or line == 'exit':
                    #[CHG] handle quit command 
                    if (client_socket != None):
                        client_socket.sendall(''.encode('utf-8'))
                    break
                do_line(line, client_socket)
    except KeyboardInterrupt:
        pass
    print("\r\nExiting...")
    machine.release()


if __name__ == "__main__":
    #  [CHG] server connection setup
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT)) 
        main(client_socket)
    #  [CHG] If there's error on the connection , execute in the local mode.
    except:
        print("-----Seems to have socket problem, act in local mode -----")
        main(None)