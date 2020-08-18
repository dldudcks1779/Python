# 필요한 패키지 import
import imutils # 파이썬 OpenCV가 제공하는 기능 중 복잡하고 사용성이 떨어지는 부분을 보완(이미지 또는 비디오 스트림 파일 처리 등)
import cv2 # opencv 모듈

# 비디오 파일
video = "test_video.mp4" # "" 일 경우 webcam 사용

# 저장할 비디오 파일 경로 및 이름
result_path = "result_video.avi"

# 비디오 경로가 제공되지 않은 경우 webcam
if video == "":
    print("[webcam 시작]")
    vs = cv2.VideoCapture(0)

# 비디오 경로가 제공된 경우 video
else:
    print("[video 시작]")
    vs = cv2.VideoCapture(video)

# 프레임 크기
w = vs.get(cv2.CAP_PROP_FRAME_WIDTH) # 너비
h = vs.get(cv2.CAP_PROP_FRAME_HEIGHT) # 높이
print("높이", w)
print("너비", h)

writer = None

# 비디오 스트림 프레임 반복
while True:
    # 프레임 읽기
    ret, frame = vs.read()

    # 읽은 프레임이 없는 경우 종료
    if frame is None:
        break

    # 프레임 자르기
    frame = frame[int(h*0.2) : int(h*0.8), int(w*0.2) : int(w*0.8)] # [시작 height : 끝 height, 시작 width : 끝 width]

    # 프레임 출력
    cv2.imshow("frame", frame)
    key = cv2.waitKey(1) & 0xFF
    
    # 'q' 키를 입력하면 종료
    if key == ord("q"):
        break
                                    
    # video 설정
    if writer is None:
        fourcc = cv2.VideoWriter_fourcc(*"MJPG")
        writer = cv2.VideoWriter(result_path, fourcc, 25, (frame.shape[1], frame.shape[0]), True)

    # 비디오 저장
    if writer is not None:
        writer.write(frame)

# 종료
vs.release()
cv2.destroyAllWindows()
