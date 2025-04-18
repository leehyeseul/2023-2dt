#server

import os
import logging
import socket
import threading

HOST = ''
PORT = 9999



class SERVER:
    
    def __init__(self):
        self.clients = []   #서버에 연결된 모든 클라이언트 정보 저장
        self.client_ports = []  # 클라이언트 포트 번호 저장
        self.server_socket = None
        self.lock = threading.Lock()
        # self.system_clock = System_Clock()
    
    def accept_client(self):

        log_file_path = '/logfile/server.txt'
        log_directory = os.path.dirname(log_file_path)
        os.makedirs(log_directory, exist_ok=True)

        logging.basicConfig(
            filename=log_file_path,
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            encoding='utf-8'
        )
                
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 서버 소켓 바인딩 및 리스닝
        server_socket.bind((HOST, PORT))
        server_socket.listen(4)
        print("서버 시작\n")
        logging.info("서버시작")
        print("클라이언트 접속 준비\n")
        logging.info("클라이언트 접속 준비")


        while True:
            client_socket, addr = server_socket.accept()
            print(f"클라이언트 연결: {addr}")
            logging.info(f"클라이언트 연결: {addr}")

            # 클라이언트의 포트 번호를 저장
            client_port = int(client_socket.recv(1024).decode())

            self.clients.append(client_socket)
            self.client_ports.append(client_port)

            if len(self.clients) == 4:
                for c in self.clients:
                    c.send(str(self.client_ports).encode())
                    logging.info(f"포트 번호 리스트 : {self.client_ports}")
                    print(f"포트 번호 리스트 : {self.client_ports}")
                    logging.info("포트번호 리스트 전송완료")
                    print("포트번호 리스트 전송완료")

            client_handler = threading.Thread(target=self.handle_client, args=(client_socket, client_port))
            client_handler.start()

    def handle_client(self, client_socket, client_port):
        try:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                # 받은 데이터를 다른 클라이언트에게 전송
                self.broadcast_data(data, client_port)
        except Exception as e:
            print(f"Error handling client {client_port}: {e}")
            logging.error(f"Error handling client {client_port}: {e}")
        finally:
            with self.lock:
                # 클라이언트가 연결을 끊으면 해당 클라이언트의 정보를 삭제
                if client_port in self.client_ports:
                    self.client_ports.remove(client_port)
                if client_socket in self.clients:
                    self.clients.remove(client_socket)
                client_socket.close()

    def broadcast_data(self, data, sender_port):
        for port, socket in zip(self.client_ports, self.clients):
            if port != sender_port:
                try:
                    # 다른 클라이언트에게 데이터를 전송
                    socket.send(data)
                except Exception as e:
                    print(f"Error broadcasting data to port {port}: {e}")
                    logging.error(f"Error broadcasting data to port {port}: {e}")


if __name__ == "__main__":
    start_server = SERVER()
    server_thread = threading.Thread(target=start_server.accept_client)
    server_thread.start()
    