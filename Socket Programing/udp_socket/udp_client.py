import socket

ip = '192.168.1.3' # ip 주소
port = 50001 # port 번호

# 소켓 객체를 생성
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 서버로 데이터 전송
msg = "생각을 코딩하다" # 전송할 메시지
sock.sendto(msg.encode("UTF-8"), (ip, port))

# 소켓 종료
sock.close()
print('close')
