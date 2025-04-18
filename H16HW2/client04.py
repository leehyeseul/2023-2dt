# CLIENT4

import socket
import os
import logging
import time
import numpy as np
import json

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(('localhost', 4914))

server_address = ('localhost', 9999)


calc_row = []
calc_col = []

# 푸티에서 돌아가게 하기 위한 로그 파일 경로
# log_file_folder = '/home/ubuntu/logfile'
# log_file_name = 'client04.txt'
# log_file_path = os.path.join(log_file_folder, log_file_name)
log_file_path='/logfile/client04.txt'

log_directory = os.path.dirname(log_file_path)
os.makedirs(log_directory, exist_ok=True)


logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'
)

# 랜덤으로 행렬을 만들고, 행(또는 열)을 추출하는 함수
class MATRIX:
    
    def make_matrix():
        ran_matrix = np.random.randint(1, 101, size=(10, 10))  #랜덤 행렬 추출
        
        return ran_matrix
    
    def pick_col(matrix):
        random_col_index= np.random.randint(0,10)  #랜덤 col 선택
        selected_col = matrix[random_col_index]
        
        return random_col_index, selected_col
    
    # 받은 행과 열의 곱셈연산을 하는 함수
    def multiply_and_add(row_info, col_info):
        multi_result = np.dot(row_info, col_info)
        return multi_result


with client_socket as cs:
    cs.connect(server_address)
    cs.sendall(f"클라이언트4 접속완료. 행, 열 전송 대기중".encode('utf-8'))    
    
    try:
        ran_matrix = MATRIX.make_matrix()
        print(ran_matrix)
        print('\n')

        while True:

            data = client_socket.recv(1024).decode('utf-8')
            
            if data == "col":
                print("랜덤으로 열을 선택한 후 전송하세요.")
                logging.info("랜덤으로 열을 선택한 후 전송.")
                time.sleep(1)
                
                col_num, col_data = MATRIX.pick_col(ran_matrix)
                
                col_data_list = col_data.tolist()
                col_data_json = json.dumps(col_data_list)
                cli_name = "cli4"
                mat_info = "col"
                print(f"{cli_name}, {mat_info}, {col_num}, {col_data_json}")
                logging.info(f"{cli_name}, {mat_info}, {col_num}, {col_data_json}")
                cs.sendall(f"{cli_name},{mat_info},{col_num},{col_data_json}".encode('utf-8'))
                print("열 정보 잘 보냄")
                logging.info("열 정보 잘 보냄")
            
            else:                           # 계산할 행, 열을 받는다면
                print(f"\n\n{data}")
                cli_name, rec_mat, mat_num, mat_data_json = data.split(',', 3)
                mat_data_list = json.loads(mat_data_json)                       
                mat_data = np.array(mat_data_list)                              
                recv_mat_info = [cli_name, rec_mat, mat_num, mat_data]           
                
                if rec_mat == "row":
                    calc_row.append(mat_data)
                    print(f"calc_row = {calc_row[0]}")
                    logging.info(f"calc_row = {calc_row[0]}")
                else:
                    calc_col.append(mat_data)
                    print(f"calc_col = {calc_col[0]}")
                    logging.info(f"calc_col = {calc_col[0]}")

                # 만약 행과 열을 모두 받았으면
                if len(calc_row) == 1 and len(calc_col) == 1:
                    calc_result = MATRIX.multiply_and_add(calc_row[0], calc_col[0])
                    print(f"행, 열 계산 결과 = {calc_result}\n")
                    logging.info(f"행, 열 계산 결과 = {calc_result}\n")
                    cs.sendall(f"{calc_result}".encode('utf-8'))
                else:
                    continue
            
            if data == "ok":
                client_socket.close() 
            

    except Exception as e:
        print(f"오류발생, {e}")
        logging.error(f"오류 발생: {e}")