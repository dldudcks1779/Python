import sys, socket
from threading import Thread

HOST = '192.168.1.3' # ip 주소
PORT = 50001 # port 번호

def rcvMsg(sock):
    while True: # 연속성 스레드
        try:
            data = sock.recv(1024) # 서버로부터 문자열 수신
            if not data: # 문자열 없으면 종료
                break
            print(data.decode())
        except:
            pass # 예외 원인 무시

def runChat(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((host, port)) # 소켓 연결
        # rcvMsg 함수를 연속 실행하는 스레드 생성
        # sock 소켓 객체를 tuple 형식으로 전달
        t = Thread(target = rcvMsg, args = (sock,))
        t.daemon = True # 스레드를 생성한 메인 스레드가 종료되면 자동으로 종료됨
        t.start() # 스레드 시작

        while True:
            msg = input() # 키보드 입력
            if msg == '/exit': # 종료
                sock.send(msg.encode())
                break # while 종료
 
            sock.send(msg.encode()) # 입력 메시지 전송

runChat(HOST, PORT)
