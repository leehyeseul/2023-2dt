import socket
import random
import time
import logging
import os
import threading

HOST = ''
PORT = 9999

class System_Clock:
    def __init__(self):
        self.time = 0
        self.running = True
        self.lock = threading.Lock()
        self.update_thread = threading.Thread(target=self.update)
        self.update_thread.daemon = True
        self.update_thread.start()
            
    def update(self):
        while self.running:
            time.sleep(1)
            with self.lock:
                self.time += 1
    
    def get(self):
        with self.lock:
           return self.time

def make_question():    
    num1 = random.randint(1,100)
    num2 = random.randint(1,100)
    num3 = random.randint(1,100)
    
    operators = ['+', '-', '*', '/']
    oper1 = random.choice(operators)
    oper2 = random.choice(operators)
    
    que = f"{num1} {oper1} {num2} {oper2} {num3}"
    answer = eval(que)
    res = int(answer) 
    
    return que, res

class ServerWithClock:
    def __init__(self):
        self.system_clock = System_Clock()
        self.SUM = 0
        self.wrong_que = ""
        self.wrong_res = 0
        self.server_socket = None
        self.running = True
        self.thread_list = []

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        now_time = self.system_clock.get()
        
        log_file_path='/logfile/server.txt'
        
        log_directory = os.path.dirname(log_file_path)
        os.makedirs(log_directory, exist_ok=True)
        
        logging.basicConfig(
            filename=log_file_path,
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            encoding='utf-8'
        )
        
        with self.server_socket as ss:
            ss.bind((HOST, PORT))    
            ss.listen(4)              
            print(f'서버가 시작됨. system clock : {now_time}sec')
            
            while self.running:
                conn, addr = ss.accept()
                
                now_time = self.system_clock.get()         
                print(f'클라이언트 접속 : {addr}. system clock : {now_time}sec')
                conn.sendall(f'접속시간 : {now_time}'.encode('utf-8'))
                logging.info(f'클라이언트 접속 : {addr}. system clock : {now_time}sec')
                
                threading.Thread(target=server.handle, args=(conn, addr)).start()
                self.thread_list.append(conn)
            
            
    def handle(self, conn:socket.socket, addr):
           
        try:
            while self.running:
                now_time = self.system_clock.get()
                print(f'system clock : {now_time}sec\n')
                
                if self.wrong_que:
                    conn.sendall(f'이전문제 : {self.wrong_que}'.encode('utf-8'))
                    logging.info(f'이전문제 : {self.wrong_que}')
                else: 
                    wait_time = random.uniform(0,5)
                    time.sleep(wait_time)
                    
                    que, res = make_question()
                    conn.sendall(f'새 문제 : {que}'.encode('utf-8'))
                    logging.info(f'새 문제 : {que}')
                    
                data = conn.recv(1024).decode('utf-8')
                get_answer, get_time = data.split(', ')
                elapsed_time = float(get_time)
                
                # print(f'답, 경과시간 : {get_answer}, {elapsed_time}sec') 
                logging.info(f'답, 경과시간 : {get_answer}, {elapsed_time}sec')
                
                try:
                    client_answer = int(get_answer)
                except ValueError:
                    # 숫자가 아닌 값을 입력하면 올바르지 않다고 뜸
                    conn.sendall(f'입력값이 올바르지 않습니다.'.encode('utf-8'))
                    logging.error(f'입력값이 올바르지 않습니다.')
                    self.wrong_que, self.wrong_res = que, res
            
                now_time = self.system_clock.get()
            
                if client_answer == res and elapsed_time <= 5:
                    self.SUM = self.SUM + res
                    conn.sendall(f'정답'.encode('utf-8'))
                    logging.info(f'정답! 지금까지 정답 합 : {self.SUM}')
                    logging.info(f'system clock3 : {now_time}sec')
                    self.wrong_que, self.wrong_res = "", 0
                else:
                    if client_answer != res:
                        conn.sendall('오답'.encode('utf-8'))
                        logging.info('오답')
                        logging.info(f'system clock : {now_time}sec\n')
                        self.wrong_que, self.wrong_res = que, res
                    
                    elif elapsed_time > 5:
                        conn.sendall(f'5sec'.encode('utf-8'))
                        logging.info(f'5sec 이상 경과, system clock : {now_time}sec\n')
                        self.wrong_que, self.wrong_res = que, res
                
                if now_time >= 15:
                    for socket_thread in self.thread_list:
                        conn.sendall('종료'.encode('utf-8'))
                        
                        conn.close()
                        self.thread_list.remove(socket_thread)
                        
                        print(f'클라이언트 {addr} 연결 종료')
                        logging.info(f'클라이언트 {addr} 연결 종료')
                    
                    print(f'모든 연산 결과 누적합 : {self.SUM}')
                    logging.info(f'모든 연산 결과 누적합 : {self.SUM}')
                    

                    self.server_socket.close()
                    
                    break
            
                        
        except Exception as e:
            print(f'클라이언트 오류 : {e}')
        
        
                    
if __name__=="__main__":
    server = ServerWithClock()
    server_thread = threading.Thread(target=server.run)
    server_thread.start()