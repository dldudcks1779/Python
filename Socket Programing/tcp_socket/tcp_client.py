import socket

ip = '192.168.1.3' # ip 주소
port = 50001 # port 번호

# 소켓 객체를 생성 및 연결
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((ip, port))
print('연결 성공')

# 서버로 데이터 전송
msg = "생각을 코딩하다" # 전송할 메시지
sock.send(msg.encode("UTF-8"))

# 서버로부터 1024바이트만큼 데이터를 받음
data = sock.recv(1024).decode("UTF-8")
print(data) # 데이터 출력

# 소켓 종료
sock.close()
print('close')
