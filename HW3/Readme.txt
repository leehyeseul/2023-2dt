조 이름 : 16조
 
#역할
조원 :  통계학과 20212086 소연우
   역할 : 코드 작성, 리드미 파일 작성
 
         통계학과 20212196 이혜슬
   역할 :  코드 작성 (클라이언트 P2P 연결), 제출 파일 정리 

         수학과 20202279 박송원     	
   역할 : 외부서버 AWS 이용한 putty 연결, 코드 작성(chunk 전송), 설명용 영상 촬영
 
#프로그램 구성요소 :
-서버 
class SERVER : 
def __init__(self):
>> 서버에 연결된 모든 클라이언트 정보 저장 리스트와 클라이언트 주소 정보 저장 리스트 생성
def accept_client(self):
>> 로그 설정(파일 경로, 디렉토리 생성), 서버 소켓 설정, 서버에서 클라이언트 연결 대기 후 클라이언트의 정보(소켓과 주소)를 리스트에 추가하고 모든 클라이언트가 연결되면 포트 리스트를 클라이언트들에게 전송, 클라이언트 처리 스레드 시작
def handle_client(self, client_socket, client_port):
>> 클라이언트로부터 데이터 수신해 다른 클라이언트에게 전송(에러 발생 시 에러 출력문 출력), 클라이언트가 연결 끊으면 해당 클라이언트 정보 삭제
def broadcast_data(self, data, sender_port):
>> 다른 클라이언트에게 데이터 전송

-클라이언트
class File:
def __init__(self):
>>  청크 파일 리스트 생성
def split_file(self, file_path, chunk_size):
>> chunk 파일을 지정된 크기로 나눔
def append_chunk(self, fileN, chunk):
>> 소켓 통해 데이터 chunk 전송

class CLIENT01:
def __init_(self, client_id):
>> 클라이언트 id 설정으로 p2p 연결한 클라이언트 2, 3, 4 각각 구별
def handle_receive_data(self, client_socket):
>> 다른 각 클라이언트들에게 전송된 데이터 수신
def connect_to_peers(self, ports_list):
>> 클라이언트 간 p2p연결 
>> 클라이언트 1 -  클라이언트 2, 3, 4 에게 p2p 요청
>> 클라이언트 2 - 클라이언트 3, 4 에게 p2p 요청
>> 클라이언트 3- 클라이언트 4에게 p2p 요청
def start_client(self):
>> 로그 파일 설정 및 서버 소켓 연결
>> 서버 통해서 다른 클라이언트들의 port 리스트 받음

#소스코드 컴파일 방법 명시

#프로그램 실행 환경 및 실행방법 설명
외부서버 AWS를 이용해 putty를 연결하고 코드 실행

#구현한 최적의 알고리즘 제시 및 설명(Psuedo Code 작성 및 설명)
- 서버
서버 클래스 생성(SERVER):
    필수 속성 초기화:

        서버에 연결된 클라이언트 소켓 정보 저장 리스트
        클라이언트 주소 정보 저장 리스트
        서버 소켓 객체
        스레드 간 동기화 위한 락 객체
    accept_client 메서드:
        로그 파일 경로 설정 및 디렉토리 생성
        로그 설정(파일 이름, 로그 레벨, 포맷, 날짜 형식, 인코딩)
        서버 소켓 생성 및 설정
        서버 소켓 바인딩 및 리스닝
        클라이언트 연결 대기 루프
            클라이언트가 연결되면 클라이언트 소켓과 주소 받음
            클라이언트 정보 리스트에 추가
            모든 클라이언트가 연결되면 주소 리스트 클라이언트에게 전송
            클라이언트 처리할 스레드 시작
    handle_client 메서드:
        클라이언트로부터 데이터를 지속적으로 수신해 다른 클라이언트에게 전송
        클라이언트가 연결을 끊으면 해당 클라이언트 정보 삭제
    broadcast_data 메서드:
        데이터 받은 클라이언트 제외한 모든 클라이언트에게 데이터 전송
서버 객체 생성 및 실행:
    SERVER 클래스의 인스턴스 생성
    서버 객체의 accept_client 메서드를 실행하는 스레드 시작

- 클라이언트
클라이언트 클래스 생성:
    필수 속성 초기화:
        클라이언트 소켓 객체
        서버 주소 및 포트
        전송할 파일 경로
        파일 이름 또는 식별자
        데이터 나누는 크기
        스레드 간 동기화 위한 락 객체
    start_client 메서드:
        클라이언트 소켓 생성 및 서버에 연결
        로그 파일 경로 설정 및 디렉토리 생성
        로그 설정(파일 이름, 로그 레벨, 포맷, 날짜 형식, 인코딩)
        서버에서 받은 다른 클라이언트 포트 리스트 수신
        다른 클라이언트들과 P2P 연결 수행
             

구현한 최적의 알고리즘
=> 서버와 같은 곳에 위치하는 클라이언트 1,2 에게 클라이언트1이 파일 A, C를, 클라이언트 2가 B, D를 갖도록 한 후 클라이언트 1, 2끼리 통신 / 또다른 곳에 위치하는 클라이언트 3, 4에게 동일하게 클라이언트3이 파일 A, C를, 클라이언트4가 B, D를 갖도록 한 후 클라이언트 3,4끼리 통신

#Error or Additional Message Handling 에 대한 사항 설명
- 실제 시간과 동일한 system clock 구현 실패
- client_id 설정 실패로 파일 전송 실패

#Additional Comments
- 저희 조는 컴퓨터공학과가 아닌 통계학과 2명과 수학과 1명으로 진행하였습니다. 

통계학과 이혜슬, 소연우

올해부터 연계전공으로 데이터 통신을 수강하게 되어 컴퓨터공학과의 1, 2학년 기초 수업을 수강하지 않은 상태였습니다. 때문에 thread, P2P, socket 통신 등에 대해 대부분 이번 2학기에 처음 직접 다루어보고 사용해 보게 되었습니다. 처음 과제를 받았을 땐 해낼 수 있을지 막막하기도 하였고, 실제로도 과제를 진행하면서 순조롭게 진행되지 않았습니다. 아는 지인도 없어 맨땅에 헤딩 하는 격으로 진행하다 앞의 두 과제의 제출기한을 놓쳐버리는 큰 실수도 해버리며 이번 과제는 포기하고 재수강까지도 솔직히 생각 했었습니다. 그래도 과제를 아예 놔버릴 순 없었기에 나름의 최선을 다했습니다. 이것도 컴퓨터공학과의 3학년 학생들만큼의 수준에는 못 미칠거라고 생각하지만 저희의 노력은 알아 주셨으면 합니다. 그래도 과제를 진행하며 통신 코드도 처음 구현해보고, thread도 말로만 들어봤지 처음 다루어보는 등 덕분에 저희가 해오던것과는 다른, 완성도 높은 프로그램 코드를 짜며 많이 성장 할 수 있었던 것 같습니다. 부족한만큼 더 노력하여 더 잘 할 수 있도록 하겠습니다. 감사합니다. 

수학과 박송원

