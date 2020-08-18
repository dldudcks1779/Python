# 필요한 패키지 import
import imutils # 파이썬 OpenCV가 제공하는 기능 중 복잡하고 사용성이 떨어지는 부분을 보완(이미지 또는 비디오 스트림 파일 처리 등)
import cv2 # opencv 모듈

# 이미지 파일
image = "test_image.jpg"

# 저장할 이미지 파일
result_path = "result_image.jpg"

# 이미지 읽기
image = cv2.imread(image)

# 이미지 resize
image = imutils.resize(image, width=500)

# 이미지 저장
cv2.imwrite(result_path, image) # 파일로 저장, 포맷은 확장자에 따름

# 이미지 show
cv2.imshow("image", image)
cv2.waitKey(0)
