# SERVER

import socket
import time
import threading
import logging
import os
import numpy as np
import random
import json
import itertools

HOST = ''
PORT = 9999


# 행과 열 정보를 받아 처리하는 클래스
class MATRIX:
    def __init__(self):
        self.result_matrix_12 = np.zeros((10, 10), dtype=int)
        self.result_matrix_13 = np.zeros((10, 10), dtype=int)
        self.result_matrix_14 = np.zeros((10, 10), dtype=int)
        self.result_matrix_23 = np.zeros((10, 10), dtype=int)
        self.result_matrix_24 = np.zeros((10, 10), dtype=int)
        self.result_matrix_34 = np.zeros((10, 10), dtype=int)
        
        
    def decide_matrix(self, row_cli, col_cli, result, x, y):
        
        if row_cli == "cli1":
            if col_cli == "cli2":
                self.result_matrix_12[x, y] = result
                print("result_matrix_12\n")
                print(self.result_matrix_12)
                logging.info(self.result_matrix_12)
                
            elif col_cli == "cli3":
                self.result_matrix_13[x, y] = result
                print("result_matrix_13\n")
                print(self.result_matrix_13)
                logging.info(self.result_matrix_13)
                
            elif col_cli == "cli4":
                self.result_matrix_14[x, y] = result
                print("result_matrix_14\n")
                print(self.result_matrix_14)
                logging.info(self.result_matrix_14)
        
        elif row_cli == "cli2":
            if col_cli == "cli3":
                self.result_matrix_23[x, y] = result
                print("result_matrix_23\n")
                print(self.result_matrix_23)
                logging.info(self.result_matrix_23)
                
            elif col_cli == "cli4":
                self.result_matrix_24[x, y] = result
                print("result_matrix_24\n")
                print(self.result_matrix_24)
                logging.info(self.result_matrix_24)
        
        elif row_cli == "cli3":
            self.result_matrix_34[x, y] = result
            print("result_matrix_34\n")
            print(self.result_matrix_34)
            logging.info(self.result_matrix_34)
            
    def IsMatrixFull(self):
        matrix12_full = np.all(self.result_matrix_12 != 0, axis=1)
        matrix13_full = np.all(self.result_matrix_13 != 0, axis=1)
        matrix14_full = np.all(self.result_matrix_14 != 0, axis=1)
        matrix23_full = np.all(self.result_matrix_23 != 0, axis=1)
        matrix24_full = np.all(self.result_matrix_24 != 0, axis=1)
        matrix34_full = np.all(self.result_matrix_34 != 0, axis=1)
        
        if matrix12_full and matrix13_full and matrix14_full and matrix23_full and matrix24_full and matrix34_full:
            return 1
             
    def PrintMatrix(self):
        print("result_matrix_12\n")
        print(self.result_matrix_12)
        
        print("result_matrix_13\n")
        print(self.result_matrix_13)  
        
        print("result_matrix_14\n")
        print(self.result_matrix_14)  
        
        print("result_matrix_23\n")
        print(self.result_matrix_23)   
        
        print("result_matrix_24\n")
        print(self.result_matrix_24) 
        
        print("result_matrix_34\n")
        print(self.result_matrix_34)
    
    
class SERVER:
    
    def __init__(self):
        self.clients = []
        self.select_clients = []
        self.calc_clients = [] 
        self.MATRIX = MATRIX()
        self.n = 1
        self.i = 1
        self.server_socket = None
    
    def accept_client(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # 푸티에서 돌아가게 하기 위한 로그 파일 경로
        # log_file_folder = '/home/ubuntu/logfile'
        # log_file_name = 'client01.txt'
        # log_file_path = os.path.join(log_file_folder, log_file_name)
        
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
        
        with server_socket as ss:
            ss.bind((HOST, PORT))
            ss.listen(4)
            print("서버 시작\n")
            print("클라이언트 접속 준비\n")

            while True:
                try:
                    client_socket, addr = ss.accept()
                    client_info = (f"client {self.n}", client_socket)
                    self.clients.append(client_info)
                    self.n += 1
                    
                    data = client_socket.recv(1024).decode('utf-8')     # 클라이언트n 접속완료
                    print(data)
                    logging.info(f"client{addr} 접속 완료")
                    print(f"접속 클라이언트 주소 : {addr}\n")
                    
                except Exception as e:
                    ss.close()
                    print(f"오류발생, {e}")
                    logging.error(f"오류 발생: {e}")
                    server_socket.close()

                    break
                
                thread = threading.Thread(target=self.handle_client, args=(client_socket, addr))
                thread.daemon = True
                thread.start()
                
                    
    
    def handle_client(self, client_socket, addr):      
        while True:       
            if len(self.clients) == 4:          # 4명의 클라이언트들이 접속하면
                
                self.make_clients_pair = list(itertools.combinations(self.clients, 2))
                use_clients_pair = self.make_clients_pair.copy()
                
                while use_clients_pair:
                    # 한 round 안에서 동작할 것들
                    
                    select_pair = random.choice(use_clients_pair)
                    
                    
                    self.select_clients = sorted(select_pair, key=lambda x: int(x[0].split()[1]))
                    
                    self.calc_clients = [calc_cli for calc_cli in self.clients if calc_cli not in self.select_clients]
                    calc_cli = random.choice(self.calc_clients)                     # 행 보낼 클라이언트
                    calc_cli_name, calc_cli_socket = calc_cli
                    
                    
                    for client_info in self.select_clients:
                        
                        if client_info == self.select_clients[0]:
                            client_name, select_client_socket = self.select_clients[0]      # 선택된 클라이언트
                            
                            print(f"\n행을 보낼 클라이언트 : {client_name}")
                            # 선택된 클라이언트에게 메세지 전송.
                            select_client_socket.sendall("row".encode('utf-8'))
                            
                            # 받은 행 처리하는 부분
                            data_row = select_client_socket.recv(1024).decode('utf-8')     
                            print(f"{client_name} 받은 데이터 : {data_row}")         
                            
                            calc_cli_socket.sendall(f"{data_row}".encode('utf-8'))             
                            
                            cli_name, row, row_num, row_data_json = data_row.split(',', 3)      
                            row_data_list = json.loads(row_data_json)                   
                            row_data = np.array(row_data_list)                             
                            
                            row_info = [cli_name, row, row_num, row_data]   
                            print(f"행 정보 : {row_info}")
                            logging.info(f"행 정보 : {row_info}")
                            print(f"계산위해 행, 열 보낼 클라이언트 : {calc_cli_name}\n")
                            logging.info(f"계산위해 행, 열 보낼 클라이언트 : {calc_cli_name}\n")
                            
                            
                        else:
                            client_name, select_client_socket = self.select_clients[1]  
                            
                            print(f"\n열을 보낼 클라이언트 : {client_name}")
                            logging.info(f"\n열을 보낼 클라이언트 : {client_name}")
                            select_client_socket.sendall("col".encode('utf-8'))
                            
                            # 받은 열 처리하는 부분
                            data_col = select_client_socket.recv(1024).decode('utf-8')   
                            print(f"{client_name} : {data_col}")        
                            calc_cli_socket.sendall(f"{data_col}".encode('utf-8'))    
                            
                            cli_name, col, col_num, col_data_json = data_col.split(',', 3)    
                            col_data_list = json.loads(col_data_json)
                            col_data = np.array(col_data_list)
                            
                            col_info = [cli_name, col, col_num, col_data]          
                            print(f"열 정보 : {col_info}")
                            logging.info(f"열 정보 : {col_info}")
                            
                            print(f"계산위해 행, 열 보낼 클라이언트 : {calc_cli_name}\n")
                            logging.info(f"계산위해 행, 열 보낼 클라이언트 : {calc_cli_name}\n")
                                
                    # 계산한 결과값을 받는다.
                    time.sleep(2)
                    receive_data = calc_cli_socket.recv(1024).decode('utf-8')
                    result_data = int(receive_data)
                    print(f"계산한 결과값 = {result_data}")
                    logging.info(f"계산한 결과값 = {result_data}")
                    self.MATRIX.decide_matrix(row_info[0], col_info[0], result_data, int(row_num), int(col_num))
                    
                    use_clients_pair.remove(select_pair)
                    
            if MATRIX.IsMatrixFull:
                MATRIX.PrintMatrix()
                print("모든 라운드 종료")
                logging.info("모든 라운드 종료")
                client_socket.close()
                self.server_socket.close()
                
                break
                    
    
    def end_conn(self, client_socket,):
        
        time.sleep(1)
        client_socket.close()
        self.clients.remove(client_socket)

        if len(self.clients) == 0:
            self.server_socket.close()
            
        

if __name__ == "__main__":
    start_server = SERVER()
    server_thread = threading.Thread(target=start_server.accept_client)
    server_thread.start()
    