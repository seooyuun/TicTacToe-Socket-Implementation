

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
        # start 정보가 담긴 SEND msg 생성
        start_msg = (
            "SEND ETTTP/1.0\r\n"
            f"Host:{client_addr[0]}\r\n"
            f"First-Move:{start}\r\n"
            "\r\n"
        )
        
        # client_socket에 start_msg를 담아서 전송
        client_socket.sendall(start_msg.encode())
    
        ######################### Fill Out ################################
        # Receive ack - if ack is correct, start game

        # Client가 보낸 ack_msg( = START 정보가 담긴 SEND msg를 잘 받았다고 확인한 ACK msg)를 받아서 decode
        ack_msg = client_socket.recv(SIZE).decode()

        lines = [line for line in ack_msg.split('\r\n') if line] # ack_msg를 line 단위로 split

        if not check_msg(ack_msg, MY_IP) or not lines[0].startswith('ACK'): # check_msg가 false이거나(=msg에 오류), 받은 msg가 ACK 가 아니라면 종료
            print("Invalid ACK.")
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