# 필요한 패키지 import
import imutils # 파이썬 OpenCV가 제공하는 기능 중 복잡하고 사용성이 떨어지는 부분을 보완(이미지 또는 비디오 스트림 파일 처리 등)
import cv2 # opencv 모듈

# 이미지 파일
image = "test_image.jpg"

# 저장할 이미지 파일
result_path = "result_image.jpg"

# 이미지 읽기
image = cv2.imread(image)

# 이미지 정보
h, w, c = image.shape # h : 높이, w : 너비, c : 채널(색상정보) - 3일 경우 다색, 1일 경우 단색
print("높이", h)
print("너비", w)

# 이미지 자르기
image = image.copy()
image = image[int(h*0.3) : int(h*0.9), int(w*0.2) : int(w*0.7)] # [시작 height : 끝 height, 시작 width : 끝 width]

# 이미지 저장
cv2.imwrite(result_path, image) # 파일로 저장, 포맷은 확장자에 따름

# 이미지 show
cv2.imshow("image", image)
cv2.waitKey(0)
