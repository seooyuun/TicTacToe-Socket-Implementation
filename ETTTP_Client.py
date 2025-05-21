

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe import TTT, check_msg
    


if __name__ == '__main__':

    SERVER_IP = '127.0.0.1'
    MY_IP = '127.0.0.1'
    SERVER_PORT = 12000
    SIZE = 1024
    SERVER_ADDR = (SERVER_IP, SERVER_PORT)

    
    with socket(AF_INET, SOCK_STREAM) as client_socket:
        client_socket.connect(SERVER_ADDR)  
        
        ###################################################################
        # Receive who will start first from the server
        start_msg = client_socket.recv(SIZE).decode()
        lines = [l for l in start_msg.split('\r\n') if l]
        if not check_msg(start_msg, MY_IP) or not lines[0].startswith('SEND'):
            print("Invalid START message. Exiting.")
            exit()
        header = lines[2]                  
        val = header[len('First-Move:'):].strip()
        start = int(val)
    
        ######################### Fill Out ################################
        # Send ACK 
        ack_msg = (
            "ACK ETTTP/1.0\r\n"
            f"Host:{SERVER_IP}\r\n"
            "\r\n"
        )
        client_socket.sendall(ack_msg.encode())
        
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        