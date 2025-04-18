#CLIENT 4

import socket
import threading
import os
import logging
import time


class File:
    def __init__(self):
        self.chunks = []
        self.recv_chunks_A = []
        self.recv_chunks_B = []
        self.recv_chunks_C = []

    def split_file(self, file_path, chunk_size):
        # 파일 쪼개기, 쪼갠 파일 리스트에 넣기
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                self.chunks.append(chunk)
        
        return self.chunks

    def append_chunk(self, fileN, chunk):
        if fileN == "A":
            self.recv_chunks_A.append(chunk)
        elif fileN == "A":
            self.recv_chunks_B.append(chunk)
        else:
            self.recv_chunks_C.append(chunk)



class CLIENT04:
    def __init__(self, client_id):
        self.client_socket = None
        self.server_address = ('localhost', 9999)
        self.file_path = '/D:/file/D.file'
        self.fileN = 'D'

        self.chunk_size = 256 * 1024  # 256KB
        self.client_id = client_id



    def handle_receive_data(self, client_socket, lock):
        while True:
            data = client_socket.recv(1024)

    def handle_p2p_connection(self, client_socket, client_id):
        self.connected_clients[client_id] = client_socket

        # 클라이언트 ID 전송
        client_socket.send(str(client_id).encode())

        self.connected_clients[client_id].send("클라이언트 4에서 1로 데이터 전송".encode())

            

    def start_client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       
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
        with self.client_socket as cs:
            cs.connect(self.server_address)
            print("클라이언트4 서버와 연결 완료")
            logging.info(f"클라이언트4 서버와 연결 완료")

            cs.send(str(cs.getsockname()[1]).encode())

            ports_data = cs.recv(1024).decode()
            ports_list = eval(ports_data)
            print("다른 클라이언트들의 포트 번호 리스트:", ports_list)
            logging.info("다른 클라이언트들의 포트 번호 리스트:".format(ports_list))


            try:
                self.server1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server1_socket.bind(('localhost', ports_list[3]))
                self.server1_socket.listen(3)  # 여러 클라이언트와의 연결을 수락하도록 변경

                print(f"클라이언트 4가 클라이언트 1 및 3의 P2P 연결을 대기 중. (포트 {ports_list[3]})")
                logging.info(f"클라이언트 4가 클라이언트 1 및 3의 P2P 연결을 대기 중. (포트 {ports_list[3]})")
                # client1 P2P 연결 수락
                client_connection1, _ = self.server1_socket.accept()
                print("클라이언트 4가  클라이언트 1의 P2P 연결을 수락.")
                logging.info("클라이언트 4가  클라이언트 1의 P2P 연결을 수락.")

                # ckient2 P2P 연결 수락
                client_connection2, _ = self.server1_socket.accept()
                print("클라이언트 4가  클라이언트 2의 P2P 연결을 수락.")
                logging.info("클라이언트 4가  클라이언트 2의 P2P 연결을 수락.")

                # client3 P2P 연결 수락
                client_connection3, _ = self.server1_socket.accept()
                print("클라이언트 4가  클라이언트 3의 P2P 연결을 수락.")
                logging.info("클라이언트 4가  클라이언트 3의 P2P 연결을 수락.")

                # 데이터 통신 시작
                while True:
                    data1 = client_connection1.recv(1024)
                    if not data1:
                        break
                    print(f"수신된 데이터 (client1): {data1.decode()}")
                    logging.info(f"수신된 데이터 (client1): {data1.decode()}")

                while True:
                    data2 = client_connection2.recv(1024)
                    if not data2:
                        break
                    # 수신된 데이터 처리
                    print(f"수신된 데이터 (client2): {data2.decode()}")
                    logging.info(f"수신된 데이터 (client2): {data2.decode()}")

                while True:
                    data3 = client_connection3.recv(1024)
                    if not data3:
                        break
                    # 수신된 데이터 처리
                    print(f"수신된 데이터 (client3): {data3.decode()}")
                    logging.info(f"수신된 데이터 (client3): {data3.decode()}")

            except Exception as e:
                print(f"Error accepting P2P connection on port {ports_list[3]}: {e}")
                logging.error({e})
           
            finally:
                
                self.server1_socket.close()
                

            

if __name__ == "__main__":
    start_cli04 = CLIENT04(client_id=4)
    server_thread = threading.Thread(target=start_cli04.start_client)
    server_thread.start()