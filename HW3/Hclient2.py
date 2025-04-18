#CLIENT2

import socket
import threading
import os
import logging
import time


class File:
    def __init__(self):
        self.chunks = []
        self.recv_chunks_A = []
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

    def append_chunk(self, fileN, chunk):
        if fileN == "A":
            self.recv_chunks_A.append(chunk)
        elif fileN == "C":
            self.recv_chunks_C.append(chunk)
        else:
            self.recv_chunks_D.append(chunk)



class CLIENT02:
    def __init__(self, client_id):
        self.client_socket = None
        self.server_address = ('localhost', 9999)
        self.file_path = '/D:/file/B.file'
        self.client1_listen_port = 0
        self.chunk_size = 256 * 1024  # 256KB
        self.fileN = 'B'

        self.client_id = client_id

    def handle_receive_data(self, client_socket):
        while True:
            data = client_socket.recv(1024)
            print("클라이언트 2에서 수신된 데이터:", data.decode())
            logging.info("클라이언트 2에서 수신된 데이터:", data.decode())

    def connect_to_peer3(self, ports_list):
                print(f"Trying to connect to peer on port {ports_list[2]}")
                peer_address = ('localhost', ports_list[2])
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    # 클라이언트들끼리 P2P 연결 시도
                    peer_socket.connect(peer_address)
                    print(f"Connected to peer on port 3 {ports_list[2]}")
                    logging.info(f"Connected to peer on port 3 {ports_list[2]}")
                except Exception as e:
                    print(f"Error connecting to peer on port 3 {ports_list[2]}: {e}")
                    logging.error(f"Error connecting to peer on port 3 {ports_list[2]}: {e}")
                finally:
                    peer_socket.close()


    def connect_to_peer4(self, ports_list):
                print(f"Trying to connect to peer on port {ports_list[3]}")
                logging.info(f"Trying to connect to peer on port {ports_list[3]}")
                peer_address = ('localhost', ports_list[3])
                peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    # 클라이언트들끼리 P2P 연결 시도
                    peer_socket.connect(peer_address)
                    print(f"Connected to peer on port 4 {ports_list[3]}")
                    logging.info(f"Connected to peer on port 4 {ports_list[3]}")
                except Exception as e:
                    print(f"Error connecting to peer on port 4 {ports_list[3]}: {e}")
                    logging.info(f"Error connecting to peer on port 4 {ports_list[3]}: {e}")
                finally:
                    peer_socket.close()
            

    def start_client(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

        log_file_path='/logfile/client02.txt'

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
            print("클라이언트2 서버와 연결 완료")
            logging.info(f"클라이언트2 서버와 연결 완료")

            cs.send(str(cs.getsockname()[1]).encode())

            ports_data = cs.recv(1024).decode()
            ports_list = eval(ports_data)
            logging.info("다른 클라이언트들의 포트 번호 리스트:".format(ports_list))
            print("다른 클라이언트들의 포트 번호 리스트:", ports_list)

            #for port in ports_list:
            #    if port != cs.getsockname()[1]:
            try:
            # 클라이언트들끼리 P2P 연결 대기
                self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.server_socket.bind(('localhost', ports_list[1]))
                self.server_socket.listen(1)

                print(f"클라이언트 2가 클라이언트 1의 P2P 연결 대기 중. (포트 {ports_list[1]})")
                logging.info(f"클라이언트 2가 클라이언트 1의 P2P 연결 대기 중. (포트 {ports_list[1]})")
                client_connection, _ = self.server_socket.accept()
                print("클라이언트 2가 클라이언트 1의 P2P 연결을 수락.")
                logging.info("클라이언트 2가 클라이언트 1의 P2P 연결을 수락.")

                # 데이터 통신 시작
                while True:
                    data = client_connection.recv(1024)
                    if not data:
                        break
                    # 수신된 데이터 처리
                    print(f"수신된 데이터: {data.decode()}")
                    logging.info(f"수신된 데이터: {data.decode()}")


                self.connect_to_peer3(ports_list)
                self.connect_to_peer4(ports_list)

                receive_thread = threading.Thread(target=self.handle_receive_data, args=(cs,))
                receive_thread.start()


                receive_thread.join()
            except Exception as e:
                        print(f"Error accepting P2P connection on port {ports_list[1]}: {e}")
                        logging.error(f"Error accepting P2P connection on port {ports_list[1]}: {e}")
            finally:
                self.server_socket.close()
            



if __name__ == "__main__":
    start_cli02 = CLIENT02(client_id=2)
    server_thread = threading.Thread(target=start_cli02.start_client)
    server_thread.start()