

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
        start_msg = client_socket.recv(SIZE).decode() # Server로부터 받은 Start msg를 decode
        lines = [line for line in start_msg.split('\r\n') if line] # Start msg를 line 단위로 split
        if not check_msg(start_msg, MY_IP) or not lines[0].startswith('SEND'): # check_msg가 false이거나(=msg에 오류), 받은 msg가 SEND 가 아니라면 종료
            print("Invalid SEND.")
            exit() 
        header = lines[2] # 세번째 line을 header라고 지정 ( First-Move:{start} )
        val = header[len('First-Move:'):].strip() # First-move: 뒤에서부터 끝까지 잘라서 {start} 만 분리하고 이를 val에 저장
        start = int(val) # val은 정수형 변수가 아니므로 정수형으로 변환 후, 이를 start에 저장
    
        ######################### Fill Out ################################
        # Send ACK 
        # start의 값에 따라, ACK 값으로 보낼 ackstart 값 지정
        if start == 1:
            ackstart = 0
        else:
            ackstart = 1
        
        # 누가 시작인지 알리는 SEND msg를 잘 받았다고 확인하는 ACK msg 전송
        ack_msg = (
            "ACK ETTTP/1.0\r\n"
            f"Host:{SERVER_IP}\r\n"
            f"First-Move:{ackstart}\r\n"
            "\r\n"
        )

        # client_socket에 ack_msg 담아서 전송
        client_socket.sendall(ack_msg.encode())
        
        ###################################################################
        
        # Start game
        root = TTT(target_socket=client_socket, src_addr=MY_IP,dst_addr=SERVER_IP)
        root.play(start_user=start)
        root.mainloop()
        client_socket.close()
        
        