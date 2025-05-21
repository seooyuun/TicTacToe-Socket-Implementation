

import random
import tkinter as tk
from socket import *
import _thread

from ETTTP_TicTacToe import TTT, check_msg

    
if __name__ == '__main__':
    
    global send_header, recv_header
    SERVER_PORT = 12000
    SIZE = 1024
    server_socket = socket(AF_INET,SOCK_STREAM)
    server_socket.bind(('',SERVER_PORT))
    server_socket.listen()
    MY_IP = '127.0.0.1'
    
    while True:
        client_socket, client_addr = server_socket.accept()
        
        start = random.randrange(0,2)   # select random to start
        
        ###################################################################
        # Send start move information to peer
        start_msg = (
            "SEND ETTTP/1.0\r\n"
            f"Host:{client_addr[0]}\r\n"
            f"First-Move:{start}\r\n"
            "\r\n"
        )
           
        client_socket.sendall(start_msg.encode())
    
        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game
        ack_msg = client_socket.recv(SIZE).decode()

        lines = [line for line in ack_msg.split('\r\n') if line]

        if not check_msg(ack_msg, MY_IP) or not lines[0].startswith('ACK'):
            print("Invalid ACK. Closing connection.")
            client_socket.close()
            server_socket.close()
            exit()

        
        ###################################################################
        
        root = TTT(client=False,target_socket=client_socket, src_addr=MY_IP,dst_addr=client_addr[0])
        root.play(start_user=start)
        root.mainloop()
        
        client_socket.close()
        
        break
    server_socket.close()