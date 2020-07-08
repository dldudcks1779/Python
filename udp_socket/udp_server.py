import socket

ip = '192.168.1.3' # ip 주소
port = 50001 # port 번호

# 소켓 객체를 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recv_address = (ip, port) # ip와 port로된 튜플
sock.bind(recv_address) # 바인드(bind) : 소켓에 주소, 프로토콜, 포트를 할당
print('서버 실행')

data, sender = sock.recvfrom(1024)
print(sender) # 클라이언트 주소 출력
print(data.decode("UTF-8")) # 데이터 출력

# 소켓 종료
sock.close()
print('close')
