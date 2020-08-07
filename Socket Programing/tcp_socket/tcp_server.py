import socket

ip = '192.168.1.3' # ip 주소
port = 50001 # port 번호

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 소켓 객체를 생성
recv_address = (ip, port) # ip와 port로된 튜플
sock.bind(recv_address) # 바인드(bind) : 소켓에 주소, 프로토콜, 포트를 할당
sock.listen(1) # 연결 수신 대기 상태(리스닝 수(동시 접속) 설정)
print('클라이언트 연결 대기')

# 연결 수락(클라이언트 소켓 주소를 반환)
conn, addr = sock.accept()
print(addr) # 클라이언트 주소 출력

# 클라이언트로부터 1024바이트만큼 데이터를 받음
data = conn.recv(1024).decode("UTF-8")
print(data) # 데이터 출력

# 클라이언트에게 데이터를 돌려줌
conn.send(data.encode("UTF-8"))

# 연결 종료
conn.close()
print('close')
