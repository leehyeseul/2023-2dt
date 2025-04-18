# CLIENT01

import socket
import threading
import os
import logging
import time

class File:
    def __init__(self):
        self.chunks = []
        self.recv_chunks_B = []
        self.recv_chunks_C = []
        self.recv_chunks_D = []

    def split_file(self, file_path, chunk_size):
        # 파일 쪼개기, 쪼갠 파일 리스트에 넣기
        with open(file_path, 'rb') as file:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                self.chunks.append(chunk)
        
        return self.chunks
    
    def receive_chunk(self, fileN, Csocket, chunk):
        while True:
            self.append_chunk(fileN, chunk)

            if not chunk:
                Csocket.sendall("end".encode('utf-8'))
                break

    def append_chunk(self, fileN, chunk):
        if fileN == "B":
            self.recv_chunks_B.append(chunk)
        elif fileN == "C":
            self.recv_chunks_C.append(chunk)
        else:
            self.recv_chunks_D.append(chunk)




class CLIENT01:
    def __init__(self, client_id):
        self.client_socket = None
        self.server_address = ('localhost', 9999)
        self.file_path = 'C:/file/A.file'
        self.chunk_size = 256 * 1024  # 256KB
        self.fileN = 'A'
        self.connected_clients = {} 
        self.client_id = client_id


    def handle_receive_data(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            if not data:
                break

            # 수신된 데이터 처리
            decoded_data = data.decode()

            if decoded_data.isdigit():
                connected_client_id = int(decoded_data)
                print(f"Connected to Client {connected_client_id}")
                logging.info(f"Connected to Client {connected_client_id}")

                if connected_client_id == 4:
                    self.handle_p2p_connection(client_socket, client_id=4)

            print(f"수신된 데이터: {decoded_data}")

    def handle_p2p_connection(self, client_socket, client_id):
        self.connected_clients[client_id] = client_socket
        # 이후 특정 클라이언트에 데이터를 전송할 때
        self.connected_clients[client_id].send("클라이언트1에서 4로 전송".encode())
        print("클라이언트 4에게 데이터 전송 완료")

    def connect_to_peers(self, ports_list):
        for port in ports_list:
            # 자신과 연결하지 않도록 확인
            if port != self.client_socket.getsockname()[1]:
                print(f"Trying to connect to peer on port {port}")
                logging.info(f"Trying to connect to peer on port {port}")
                peer_address = ('localhost', port)
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    # 클라이언트들끼리 P2P 연결 시도
                    peer_socket.connect(peer_address)
                    print(f"Connected to peer on port {port}")
                    logging.info(f"Connected to peer on port {port}")
                except Exception as e:
                    print(f"Error connecting to peer on port {port}: {e}")
                    logging.info(f"Error connecting to peer on port {port}: {e}")
                finally:
                    peer_socket.close()

    def start_client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        log_file_path = '/logfile/client01.txt'

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
            print("클라이언트1 서버와 연결 완료")
            logging.info(f"클라이언트1 서버와 연결 완료")

            cs.send(str(cs.getsockname()[1]).encode())

            ports_data = cs.recv(1024).decode()
            ports_list = eval(ports_data)
            print("다른 클라이언트들의 포트 번호 리스트:", ports_list)
            logging.info("다른 클라이언트들의 포트 번호 리스트:".format(ports_list))

            self.connect_to_peers(ports_list)

            receive_thread = threading.Thread(target=self.handle_receive_data, args=(cs,))
            receive_thread.start()


            receive_thread.join()


if __name__ == "__main__":
    start_cli01 = CLIENT01(client_id=1)
    server_thread = threading.Thread(target=start_cli01.start_client)
    server_thread.start()
