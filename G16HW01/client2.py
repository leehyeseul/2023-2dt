import socket
import os
import logging
import time


log_file_path = '/logfile/client2.txt'

log_directory = os.path.dirname(log_file_path)
os.makedirs(log_directory, exist_ok=True)


logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s]: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    encoding='utf-8'

)

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.bind(('localhost', 49152))

server_address = ('localhost', 9999)

with client_socket as cs:
    cs.connect(server_address)
    
    data = cs.recv(1024).decode('utf-8')
    print(f'\n클라이언트 접속 완료. {data}sec')
    logging.info(f'\n클라이언트 접속 완료.')
    
    try:
        while True:
            
            data = cs.recv(1024).decode('utf-8')
            
            if data == "종료":
                break
            
            que = data
            print(que)
            logging.info(f'{que}')
            
            start_time = time.time()
            answer = input("사칙연산에 대한 정답 입력 : ")
            logging.info(f'사칙연산에 대한 정답 입력 : {answer}')
            end_time = time.time()
            elapsed_time = end_time - start_time
            
            cs.sendall(f'{answer}, {elapsed_time:.2f}'.encode('utf-8'))
            
            data = cs.recv(1024).decode('utf-8')
            logging.info(f'서버응답 : {data}')
            print(f'서버응답 : {data}')
            
            if data == "종료":
                break
            
            else:
                if data == '오답':
                    print('다시 계산')
                elif data == '정답':
                    print('새로운 문제 출제')
                elif data == '5sec':
                    print('다시 작성')
        
                
        print(f'서버응답 : {data}')
        logging.info('클라이언트2 연결 종료')
        print(f'클라이언트2 연결 종료')
        cs.close()          

                    
    except Exception as e:
        logging.error(f'오류발생: {e}')