
import random
import tkinter as tk
from socket import *
import _thread

SIZE=1024

class TTT(tk.Tk):
    def __init__(self, target_socket,src_addr,dst_addr, client=True):
        super().__init__()
        
        self.my_turn = -1

        self.geometry('500x800')

        self.active = 'GAME ACTIVE'
        self.socket = target_socket
        
        self.send_ip = dst_addr
        self.recv_ip = src_addr
        
        self.total_cells = 9
        self.line_size = 3
        
        
        # Set variables for Client and Server UI
        ############## updated ###########################
        if client:
            self.myID = 1   #0: server, 1: client
            self.title('34743-01-Tic-Tac-Toe Client')
            self.user = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Won!', 'text':'O','Name':"YOU"}
            self.computer = {'value': 1, 'bg': 'orange',
                             'win': 'Result: You Lost!', 'text':'X','Name':"ME"}   
        else:
            self.myID = 0
            self.title('34743-01-Tic-Tac-Toe Server')
            self.user = {'value': 1, 'bg': 'orange',
                         'win': 'Result: You Won!', 'text':'X','Name':"ME"}   
            self.computer = {'value': self.line_size+1, 'bg': 'blue',
                     'win': 'Result: You Lost!', 'text':'O','Name':"YOU"}
        ##################################################

            
        self.board_bg = 'white'
        self.all_lines = ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                          (0, 3, 6), (1, 4, 7), (2, 5, 8),
                          (0, 4, 8), (2, 4, 6))

        self.create_control_frame()

    def create_control_frame(self):
        '''
        Make Quit button to quit game 
        Click this button to exit game

        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.control_frame = tk.Frame()
        self.control_frame.pack(side=tk.TOP)

        self.b_quit = tk.Button(self.control_frame, text='Quit',
                                command=self.quit)
        self.b_quit.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    def create_status_frame(self):
        '''
        Status UI that shows "Hold" or "Ready"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.status_frame = tk.Frame()
        self.status_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_status_bullet = tk.Label(self.status_frame,text='O',font=('Helevetica',25,'bold'),justify='left')
        self.l_status_bullet.pack(side=tk.LEFT,anchor='w')
        self.l_status = tk.Label(self.status_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_status.pack(side=tk.RIGHT,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_result_frame(self):
        '''
        UI that shows Result
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.result_frame = tk.Frame()
        self.result_frame.pack(expand=True,anchor='w',padx=20)
        
        self.l_result = tk.Label(self.result_frame,font=('Helevetica',25,'bold'),justify='left')
        self.l_result.pack(side=tk.BOTTOM,anchor='w')
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def create_debug_frame(self):
        '''
        Debug UI that gets input from the user
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.debug_frame = tk.Frame()
        self.debug_frame.pack(expand=True)
        
        self.t_debug = tk.Text(self.debug_frame,height=2,width=50)
        self.t_debug.pack(side=tk.LEFT)
        self.b_debug = tk.Button(self.debug_frame,text="Send",command=self.send_debug)
        self.b_debug.pack(side=tk.RIGHT)
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    
    def create_board_frame(self):
        '''
        Tic-Tac-Toe Board UI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.board_frame = tk.Frame()
        self.board_frame.pack(expand=True)

        self.cell = [None] * self.total_cells
        self.setText=[None]*self.total_cells
        self.board = [0] * self.total_cells
        self.remaining_moves = list(range(self.total_cells))
        for i in range(self.total_cells):
            self.setText[i] = tk.StringVar()
            self.setText[i].set("  ")
            self.cell[i] = tk.Label(self.board_frame, highlightthickness=1,borderwidth=5,relief='solid',
                                    width=5, height=3,
                                    bg=self.board_bg,compound="center",
                                    textvariable=self.setText[i],font=('Helevetica',30,'bold'))
            self.cell[i].bind('<Button-1>',
                              lambda e, move=i: self.my_move(e, move))
            r, c = divmod(i, self.line_size)
            self.cell[i].grid(row=r, column=c,sticky="nsew")
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def play(self, start_user=1):
        '''
        Call this function to initiate the game
        
        start_user: if its 0, start by "server" and if its 1, start by "client"
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.last_click = 0
        self.create_board_frame()
        self.create_status_frame()
        self.create_result_frame()
        self.create_debug_frame()
        self.state = self.active
        if start_user == self.myID:
            self.my_turn = 1    
            self.user['text'] = 'X'
            self.computer['text'] = 'O'
            self.l_status_bullet.config(fg='green')
            self.l_status['text'] = ['Ready']
        else:
            self.my_turn = 0
            self.user['text'] = 'O'
            self.computer['text'] = 'X'
            self.l_status_bullet.config(fg='red')
            self.l_status['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def quit(self):
        '''
        Call this function to close GUI
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.destroy()
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
    def my_move(self, e, user_move):    
        '''
        Read button when the player clicks the button
        
        e: event
        user_move: button number, from 0 to 8 
        '''
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        
        # When it is not my turn or the selected location is already taken, do nothing
        if self.board[user_move] != 0 or not self.my_turn:
            return
        # Send move to peer 
        valid = self.send_move(user_move)
        
        # If ACK is not returned from the peer or it is not valid, exit game
        if not valid:
            self.quit()
            
        # Update Tic-Tac-Toe board based on user's selection
        self.update_board(self.user, user_move)
        
        # If the game is not over, change turn
        if self.state == self.active:    
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

    def get_move(self): # 상대방의 이동 수신 및 보드 갱신
        '''
        Function to get move from other peer
        Get message using socket, and check if it is valid
        If is valid, send ACK message
        If is not, close socket and quit
        '''
        ###################  Fill Out  #######################
        msg = self.socket.recv(SIZE).decode() # 상대방의 메시지를 수신
        lines = [line for line in msg.split('\r\n') if line] # 수신한 msg를 line 단위로 split

        val = lines[0].split() # 첫 번째 line을 split해서 이를 val에 저장 ( = SEND ETTTP/1.0 )
        msg_valid_check = not(check_msg(msg, self.recv_ip) and (val[0] == "SEND")) # msg가 valid한지 check, boolean 값으로 리턴 
        
        if msg_valid_check: # msg 형식이 올바르지 않거나 SEND가 아닌 경우, 종료
            self.socket.close()   
            self.quit()
            return
        else:  # 메시지가 올바른 경우, 좌표 추출
            point = lines[2][len('New-Move:'):].strip() # 세번째 line에서 New-Move: 뒤부터 끝까지 잘라서 point에 저장
            row, col = map(int, point.strip('()').split(',')) # ex) (1,2)에서 괄호와 쉼표를 제거하고, 정수형 변수로 변환해서 row, col에 저장
            loc = row * self.line_size + col # 좌표를 1차원 인덱스로 변환해서 loc에 저장
            
            # ACK msg를 상대방에게 전송
            ack_msg = (
            "ACK ETTTP/1.0\r\n"
            f"Host:{self.send_ip}\r\n"
            f"New-Move:({row},{col})\r\n"  
            "\r\n"
            )
            self.socket.sendall(ack_msg.encode())
            ######################################################   
            
            
            #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
            self.update_board(self.computer, loc, get=True)
            if self.state == self.active:  
                self.my_turn = 1
                self.l_status_bullet.config(fg='green')
                self.l_status ['text'] = ['Ready']
            #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                

    def send_debug(self): # 텍스트 박스를 이용해 수동 명령 전송
        '''
        Function to send message to peer using input from the textbox
        Need to check if this turn is my turn or not
        '''

        if not self.my_turn:
            self.t_debug.delete(1.0,"end")
            return
        # get message from the input box
        d_msg = self.t_debug.get(1.0,"end")
        d_msg = d_msg.replace("\\r\\n","\r\n")   # msg is sanitized as \r\n is modified when it is given as input
        self.t_debug.delete(1.0,"end")
        
        ###################  Fill Out  #######################
        '''
        Check if the selected location is already taken or not
        '''

        '''
        Send message to peer
        '''
        
        '''
        Get ack
        '''
        lines = [line for line in d_msg.split('\r\n') if line] # 받은 d_msg를 line 단위로 split

        val = lines[0].split() # 첫 번째 line을 split해서 이를 val에 저장 ( = SEND ETTTP/1.0 )

        d_msg_valid_check = not(check_msg(d_msg, self.recv_ip) and (val[0] == "SEND")) # d_msg가 valid한지 check, boolean 값으로 리턴 
        
        if d_msg_valid_check: # d_msg 형식이 올바르지 않거나 SEND가 아닌 경우, 종료
            self.t_debug.delete(1.0,"end")
            return

        else:
            point = lines[2][len('New-Move:'):].strip() # 세 번째 라인에서 New-Move: 뒤부터 끝까지 분리
            row, col = map(int, point.strip('()').split(',')) # 좌표 문자열을 (row, col) 정수로 변환
            selection = row * 3 + col # 좌표를 1차원 인덱스로 변환
        
            # 이미 놓인 자리인지 확인: 놓여있다면 종료
            if self.board[selection] != 0:
                return
            # 상대에게 메시지 전송 및 ACK 확인 실패 시 종료
            if not self.send_move(selection):
                return
            # 유효한 위치일 시 해당 위치를 이동으로 처리
            loc = selection

        ######################################################  
        
        #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
        self.update_board(self.user, loc)
            
        if self.state == self.active:    # always after my move
            self.my_turn = 0
            self.l_status_bullet.config(fg='red')
            self.l_status ['text'] = ['Hold']
            _thread.start_new_thread(self.get_move,())
            
        #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        
        
    def send_move(self,selection): # 이동 좌표 전송 및 ACK 확인
        '''
        Function to send message to peer using button click
        selection indicates the selected button
        '''
        row,col = divmod(selection,3)
        ###################  Fill Out  #######################
        
        # SEND 메시지를 구성 후 상대방에게 send
        msg = (
            "SEND ETTTP/1.0\r\n"
            f"Host:{self.send_ip}\r\n"
            f"New-Move:({row},{col})\r\n"
            "\r\n"
        )
        self.socket.sendall(msg.encode())
        
        ack = self.socket.recv(SIZE).decode() # ACK 수신
        lines = [line for line in ack.split('\r\n') if line] # 수신한 ack msg를 line 단위로 split
        # ACK 메시지가 정상 형식인지 확인(형식에 어긋나거나 ACK 메시지가 아니면 False)
        if not check_msg(ack, self.recv_ip) or not lines[0].startswith('ACK'):
            return False
        # 정상 수신 시 Ture 리턴
        return True
        ######################################################  

    
    def check_result(self,winner,get=False): # 승리 확인 후 결과 공유
        '''
        Function to check if the result between peers are same
        get: if it is false, it means this user is winner and need to report the result first
        '''
        # no skeleton
        ###################  Fill Out  #######################
        if not get: # 내가 이겼울 경우: 결과 전송 후 상대의 확인 결과 수신신
            msg = (
            "RESULT ETTTP/1.0\r\n"
            f"Host:{self.send_ip}\r\n"
            f"Winner:{winner}\r\n"
            "\r\n"
            )
            self.socket.sendall(msg.encode()) # 승리 결과 전송
        
            data = self.socket.recv(SIZE).decode() # 상대의 ACK 응답 수신
            lines = [line for line in data.split('\r\n') if line]

            # 메시지 유효성 및 결과 일치 여부 확인
            if not check_msg(data, self.recv_ip) or not lines[0].startswith('RESULT'):
                return False
            return (lines[2][len('Winner:'):].strip() == winner)
        else:
            # 상대가 이겼으니 상대가 보낸 메세지를 수신
            data = self.socket.recv(SIZE).decode()
            lines = [line for line in data.split('\r\n') if line]

            # 메시지 유효성 및 결과 일치 여부 확인
            if not check_msg(data, self.recv_ip) or not lines[0].startswith('RESULT'):
                return False
            if lines[2][len('Winner:'):].strip() != winner:
                return False
            # RESULT 응답, 확인 메시지 전송( = 너가 이긴 것 확인했어 )
            msg = (
            "RESULT ETTTP/1.0\r\n"
            f"Host:{self.send_ip}\r\n"
            f"Winner:{winner}\r\n"
            "\r\n"
            )
            self.socket.sendall(msg.encode())
            return True

        ######################################################  

        
    #vvvvvvvvvvvvvvvvvvv  DO NOT CHANGE  vvvvvvvvvvvvvvvvvvv
    def update_board(self, player, move, get=False):
        '''
        This function updates Board if is clicked
        
        '''
        self.board[move] = player['value']
        self.remaining_moves.remove(move)
        self.cell[self.last_click]['bg'] = self.board_bg
        self.last_click = move
        self.setText[move].set(player['text'])
        self.cell[move]['bg'] = player['bg']
        self.update_status(player,get=get)

    def update_status(self, player,get=False):
        '''
        This function checks status - define if the game is over or not
        '''
        winner_sum = self.line_size * player['value']
        for line in self.all_lines:
            if sum(self.board[i] for i in line) == winner_sum:
                self.l_status_bullet.config(fg='red')
                self.l_status ['text'] = ['Hold']
                self.highlight_winning_line(player, line)
                correct = self.check_result(player['Name'],get=get)
                if correct:
                    self.state = player['win']
                    self.l_result['text'] = player['win']
                else:
                    self.l_result['text'] = "Somethings wrong..."

    def highlight_winning_line(self, player, line):
        '''
        This function highlights the winning line
        '''
        for i in line:
            self.cell[i]['bg'] = 'red'

    #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# End of Root class

def check_msg(msg, recv_ip): # 메시지 유효성 여부 확인
    '''
    Function that checks if received message is ETTTP format
    '''
    ###################  Fill Out  #######################
    # 받은 msg를 line 단위로 나누고, 공백 제거
    lines = [line for line in msg.split('\r\n') if line]

    # 만약 line의 개수가 3개 미만이라면, 유효하지 않은 메시지이므로 False 리턴
    if len(lines) < 3:
        return False

    # 첫 줄 검사 : TYPE ETTTP/1.0 형태인지 확인
    val = lines[0].split() # line[0]을 공백 기준으로 split
    # val의 항목이 2개가 아니라면, False 리턴(TYPE, ETTTP/1.0 으로 2개여야 함)
    if len(val) != 2: 
        return False
    # val[0]을 msg_type, val[1]을 version에 저장
    msg_type, version = val
    # 메시지 타입이 SEND, ACK, RESULT 이외의 것일 경우( = 허용된 타입이 아닐 경우), False
    if msg_type not in ('SEND','ACK','RESULT'):
        return False
    # 프로토콜의 버전이 ETTTP/1.0이 아니라면, False
    if version != 'ETTTP/1.0':
        return False
    
    # 두 번째 줄 검사: Host 헤더 확인
    if not lines[1].startswith('Host:'): # lines[1]이 Host: 로 시작하지 않는다면, False
        return False
    # Host: 뒤의 IP destination 추출
    dst = lines[1][len('Host:'):].strip()
    # 목적지 주소가 다르면, False
    if dst != recv_ip:
        return False

    # 세 번째 줄 검사: msg_type에 따른 본문 확인
    if msg_type == 'SEND': # msg_type이 SEND일 경우, 본문이 First-Move 또는 New-Move 여야 함
        # lines[2]를 공백 기준으로 split
        body = lines[2].strip()

        # First-move: 는 본문이 0 또는 1이어야 함
        if body.startswith('First-Move:'):
            val = body[len('First-Move:'):].strip()
            if val not in ('0', '1'):
                return False

        # New-Move:는 본문이 좌표값이 와야 함
        elif not body.startswith('New-Move:'):
            return False

    elif msg_type == 'ACK': # msg_type이 ACK일 경우, 본문이 First-Move 또는 New-Move 여야 함
        # lines[2]를 공백 기준으로 split
        body = lines[2].strip()

        # First-move: 는 본문이 0 또는 1이어야 함
        if body.startswith('First-Move:'):
            val = body[len('First-Move:'):].strip()
            if val not in ('0', '1'):
                return False

        # New-Move:는 본문이 좌표값이 와야 함
        elif body.startswith('New-Move:'):
            point = body[len('New-Move:'):].strip()
            row, col = map(int, point.strip('()').split(','))

        # msg_type이 ACK인데 본문이 First-Move와 New-Move 이외의 값이 오면, False
        else:
            return False

    elif msg_type == 'RESULT': # msg_type이 RESULT일 경우, 본문이 Winner여야 함
        # "Winner:ME" or "Winner:YOU" 가 아니라면, False
        if not lines[2].startswith('Winner:'):
            return False
        val = lines[2][len('Winner:'):].strip()
        if val not in ('ME', 'YOU'):
            return False

    return True # 모든 조건 만족 시 유효한 메시지임을 리턴
    ######################################################  