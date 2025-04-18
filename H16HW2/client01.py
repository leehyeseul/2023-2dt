# CLIENT1

import socket
import os
import logging
import time
import numpy as np
import json

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(('localhost', 4911))

server_address = ('localhost', 9999)

cli_name = "cli1"
calc_row = []
calc_col = []

# 푸티에서 돌아가게 하기 위한 로그 파일 경로
# log_file_folder = '/home/ubuntu/logfile'
# log_file_name = 'client01.txt'
# log_file_path = os.path.join(log_file_folder, log_file_name)

log_file_path='/logfile/client01.txt'

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
# 클라이언트1은 행만 필요함 >> 행만 추출
class MATRIX:
    
    def make_matrix():
        ran_matrix = np.random.randint(1, 101, size=(10, 10))
        
        return ran_matrix
    
    def pick_row(matrix):
        random_row_index= np.random.randint(0,10)
        selected_row = matrix[random_row_index]
        
        return random_row_index, selected_row
    
    def multiply_and_add(row_info, col_info):
        multi_result = np.dot(row_info, col_info)
        return multi_result


with client_socket as cs:
    cs.connect(server_address)
    cs.sendall(f"클라이언트1 접속완료. 행, 열 전송 대기중".encode('utf-8'))
    
    try:
        ran_matrix = MATRIX.make_matrix()
        print(ran_matrix)
        print('\n')

        while True:
            
            data = client_socket.recv(1024).decode('utf-8')
            
            if data == "row":
                print("\n랜덤으로 행을 선택한 후 전송하세요.")
                time.sleep(1)
                row_num, row_data = MATRIX.pick_row(ran_matrix)
                
                row_data_list = row_data.tolist()
                row_data_json = json.dumps(row_data_list)
                cli_name = "cli1"
                mat_info = "row"
                print(f"{cli_name}, {mat_info}, {row_num}, {row_data_json}")
                cs.sendall(f"{cli_name},{mat_info},{row_num},{row_data_json}".encode('utf-8'))
                print("행 정보 잘 보냄\n")
            
            else:                           # 계산할 행, 열을 받는다면
                print(f"\n\n{data}")
                cli_name, rec_mat, mat_num, mat_data_json = data.split(',', 3)
                mat_data_list = json.loads(mat_data_json)
                mat_data = np.array(mat_data_list)
                recv_mat_info = [cli_name, rec_mat, mat_num, mat_data]
                
                if rec_mat == "row":
                    calc_row.append(mat_data)
                    print(f"calc_row = {calc_row[0]}")
                else:
                    calc_col.append(mat_data)
                    print(f"calc_col = {calc_col[0]}")
                
                # 만약 행과 열을 모두 받았으면
                if len(calc_row) == 1 and len(calc_col) == 1:
                    calc_result = MATRIX.multiply_and_add(calc_row[0], calc_col[0])
                    print(f"행, 열 계산 결과 = {calc_result}\n")
                    cs.sendall(f"{calc_result}".encode('utf-8'))
                else:
                    continue
        
            if data == "ok":
                client_socket.close()     


    except Exception as e:
        print(f"오류발생, {e}")
        logging.error(f"오류 발생: {e}")