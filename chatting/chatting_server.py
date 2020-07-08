import socketserver 
import threading 
 
HOST = '192.168.1.3' # ip 주소
PORT = 50001 # port 번호
lock = threading.Lock() # 쓰레드에서 데이터 경쟁을 막으려면 Lock을 사용

class UserManager: # 사용자관리 및 채팅 메세지 전송을 담당하는 클래스
                   # 1) 채팅 서버로 입장한 사용자의 등록
                   # 2) 채팅을 종료하는 사용자의 퇴장 관리
                   # 3) 사용자가 입장하고 퇴장하는 관리
                   # 4) 사용자가 입력한 메세지를 채팅 서버에 접속한 모두에게 전송
                   
   # Dictionary, 변경 가능, 키, 값
   def __init__(self):
      self.users = {} # 사용자의 등록 정보를 담을 사전 {사용자 이름:(소켓,주소),...}

   def addUser(self, username, conn, addr): # 사용자 ID를 self.users에 추가하는 함수
      if username in self.users: # 이미 등록된 사용자라면
         # 현재 접속자에게 문자열 송신
         conn.send('이미 등록된 사용자입니다.\n'.encode()) 
         return None
 
      # 새로운 사용자를 등록함
      lock.acquire() # 스레드 동기화를 막기위한 락 # Lock
      self.users[username] = (conn, addr) # Connection, IP tuple 저장
      lock.release() # 업데이트 후 락 해제 # Unlock

      # 모든 사용자에게 메시지 전송
      self.sendMessageToAll('[%s]님이 입장했습니다.' %(username))
      print('대화 참여자 수 [%d]' %len(self.users))
         
      return username

   def removeUser(self, username): #사용자를 제거하는 함수
       # 삭제하려는 ID가 없으면 아무일도 안함
      if username not in self.users:
         return
 
      lock.acquire() # Lock
      del self.users[username]  # Dictionary에서 아이디에 해당하는 항목 삭제
      lock.release() # Unlock
 
      self.sendMessageToAll('[%s]님이 퇴장했습니다.' % username)
      print('대화 참여자 수 [%d]' %len(self.users))
 
   def messageHandler(self, username, msg): # 전송한 msg를 처리하는 부분
      if msg[0] != '/': # 보낸 메세지의 첫문자가 '/'가 아니면
         self.sendMessageToAll('[%s] %s' %(username, msg))
         return
 
      if msg.strip() == '/exit': # 보낸 메세지가 '/exit'이면
         self.removeUser(username) # 사용자 삭제
         return -1

   def sendMessageToAll(self, msg):
      # Dictionary 값 2개 추출 : Connection, IP로 구성된 tuple
      for conn, addr in self.users.values():
         conn.send(msg.encode()) # 각각의 사용자에게 메시지 전송
      
 
class MyTcpHandler(socketserver.BaseRequestHandler): # 한 번만 객체 생성됨
   userman = UserManager() # 사용자 관리 객체 생성
   def handle(self): # 클라이언트가 접속시 클라이언트 주소 출력 # 사용자 접속시마다 계속 자동 실행
      username = self.registerUsername() # 사용자 id 처리
      print('[%s] 연결됨 >> %s' %(self.client_address[0], username))
 
      try:
         msg = self.request.recv(1024) # 접속된 사용자로부터 입력대기
         while msg:
            print('[%s] %s : %s'% (self.client_address[0], username, msg.decode())) # 서버 화면에 출력
            if self.userman.messageHandler(username, msg.decode()) == -1:
               self.request.close() # Connection close
               break # 메시지 수신 대기 종료
            msg = self.request.recv(1024) # 메시지 수신 대기
                 
      except Exception as e:
         print(e)
 
      print('[%s] 접속종료' %self.client_address[0])
      self.userman.removeUser(username)
      
   def registerUsername(self): # 접속자의 이름 받기
      while True:
         self.request.send('로그인ID >>'.encode()) # 신규 현재 접속자에게 전송
         username = self.request.recv(1024) # 수신 대기
         username = username.decode().strip() # strip() : 공백 제거
         if self.userman.addUser(username, self.request, self.client_address):
            return username


# socketserver.ThreadingMixIn : 독립된 스레드로 처리하도록 접속시 마다 새로운 스레드 생성
# ThreadingMixIn, TCPServer class 상속
class ChatingServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

def runServer():
   print('>> 채팅 서버를 시작합니다.')
   print('>> 채텅 서버를 끝내려면 Ctrl-C를 누르세요.')
 
   try:
      server = ChatingServer((HOST, PORT), MyTcpHandler)
      server.serve_forever() # 무한 실행
   except KeyboardInterrupt: # Ctrl + C 입력시 종료
      print('>> 채팅 서버를 종료합니다.') 
      server.shutdown() # 서버 종료
      server.server_close() # 메모리 해제

runServer()
