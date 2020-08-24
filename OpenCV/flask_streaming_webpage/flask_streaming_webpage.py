##### 실행 #####
# sudo python3 flask_streaming_webpage.py --ip ip 주소 --port port 번호
# 예) sudo python3 flask_streaming_webpage.py --ip 192.168.1.123 --port 3000

# 필요한 패키지 import
from flask import Response
from flask import Flask
from flask import render_template
import threading
import argparse # 명령행 파싱(인자를 입력 받고 파싱, 예외처리 등) 모듈
import cv2 # opencv 모듈
import imutils # 파이썬 OpenCV가 제공하는 기능 중 복잡하고 사용성이 떨어지는 부분을 보완(이미지 또는 비디오 스트림 파일 처리 등)

# 클라이언트에게 제공될 프레임
outputFrame = None

# 스레드 안전 동작 보장(하나의 스레드가 업데이트되는 동안 프레임을 읽으려고 시도하지 않는지 확인)
lock = threading.Lock()

# flask 객체 초기화
app = Flask(__name__)

print("[webcam 시작]")
vs = cv2.VideoCapture(0)

# @ : 장식자(decorator)
# URL 연결에 활용
# route 메소드 : flask 서버로 '/URL' 요청이 들어오면 어떤 함수를 호출할 것인지 조정
@app.route("/")
# '/' : index 함수와 연결
def index():
    # 렌더링된 index.html 반환
    # return the rendered template
    return render_template("index.html")

# webcam 함수
def webcam():
    global vs, outputFrame, lock
    
    # 비디오 스트림 프레임 반복
    while True:
        # 프레임 읽기
        ret, frame = vs.read()

        # 프레임 크기 지정
        frame = imutils.resize(frame, width=1000)
        
        # 스레드 동시성을 지원하는데 필요한 lock
        with lock:
            outputFrame = frame.copy() # 출력 프레임 설정

# 출력 프레임을 jpeg 형식으로 인코딩하는 함수
def generate():
    global outputFrame, lock

    # 출력 프레임 반복
    while True:
        # 스레드 동시성을 지원하는데 필요한 lock
        with lock:

            # 출력 프레임 확인
            if outputFrame is None:
                continue
            
            # 프레임을 jpeg 형식으로 인코딩
            (flag, encodedImage) = cv2.imencode(".jpg", outputFrame)
            
            # 프레임 인코딩 성공 확인
            if not flag:
                continue

        # 출력 프레임을 바이트 형식으로 제공
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n')

@app.route("/video_feed")
# '/video_feed' : video_feed 함수와 연결
def video_feed():
    # 특정 메시지 유형과 함께 생성된 응답 반환
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

# 프로그램의 시작점
if __name__ == '__main__':
    # 실행을 할 때 인자값 추가
    ap = argparse.ArgumentParser() # 인자값을 받을 인스턴스 생성
    # 입력받을 인자값 등록
    ap.add_argument("-i", "--ip", type=str, required=True, help="ip 주소") 
    ap.add_argument("-o", "--port", type=int, required=True, help="port 번호(1024 ~ 65535)")
    # 입력받은 인자값을 args에 저장
    args = vars(ap.parse_args())

    # webcam 스레드 시작
    t = threading.Thread(target=webcam, args=())
    t.daemon = True
    t.start()

    # flask 앱 시작
    app.run(host=args["ip"], port=args["port"], debug=True, threaded=True, use_reloader=False)

# webcam 정지
vs.stop()
