##### 실행 #####
# sudo python3 color_histogram.py --image 이미지 경로
# 예) sudo python3 color_histogram.py --image test.jpg

# 필요한 패키지 import
from matplotlib import pyplot as plt # 데이터를 차트나 그래프로 시각화할 수 있는 라이브러리
import numpy as np # 파이썬 행렬 수식 및 수치 계산 처리 모듈
import argparse # 명령행 파싱(인자를 입력 받고 파싱, 예외처리 등) 모듈
import cv2 # opencv 모듈

# 실행을 할 때 인자값 추가
ap = argparse.ArgumentParser()
# 입력받을 인자값 등록
ap.add_argument("-i", "--image", required=True, help="이미지 경로")
# 입력받은 인자값을 args에 저장
args = vars(ap.parse_args())

# input 이미지 읽기
image = cv2.imread(args["image"])
cv2.imshow("image", image) # 이미지 show

# 이미지 회색조 변환
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray_image", gray_image) # 회색조 이미지 show

# calcHist([images], channels, mask, histSize, ranges) : 히스토그램 계산
# - [images] : 히스토그램을 계산하려는 이미지 배열
# - channels : 채널의 인덱스(Grayscale : [0], Color : [0, 1, 2])
# - mask : 이미지의 특정 영역 계산
# - histSize : x축 요소의 개수
# - range : 하나의 채널에 대한 픽셀값의 범위(0 ~ 255)

##### Grayscale 히스토그램 #####
gray_calchist = cv2.calcHist([gray_image], [0], None, [256], [0, 256]) # Grayscale 히스토그램 계산
plt.figure("Grayscale Histogram") # 그래프를 그리기 위한 Figure 객체 생성
plt.title("Grayscale Histogram") # 그래프 제목 설정
plt.xlabel("Bins") # x 축 레이블
plt.ylabel("Pixels") # y 축레이블
plt.plot(gray_calchist) # Grayscale 히스토그램 그리기
plt.xlim([0, 256]) # x 축의 범위

##### Color 히스토그램 #####
channels = cv2.split(image) # 채널 분할
colors = ("blue", "green", "red") # 색상 튜플
plt.figure("Color Histogram") # 그래프를 그리기 위한 Figure 객체 생성
plt.title("Color Histogram") # 그래프 제목 설정
plt.xlabel("Bins") # x 축 레이블
plt.ylabel("Pixels") # y 축 레이블
# zip : 같은 길이의 리스트를 같은 인덱스끼리 잘라서 리스트로 반환
for (channel, color) in zip(channels, colors): # channels 및 colors의 길이만큼 반복
    color_calchist = cv2.calcHist([channel], [0], None, [256], [0, 256]) # 각 채널에 대한 Color 히스토그램 계산
    plt.plot(color_calchist, color = color) # 각 채널에 대한 Color 히스토그램 그리기
    plt.xlim([0, 256]) # x 축의 범위

##### 2D 히스토그램 #####
figure= plt.figure("Multi-dimensional Histograms") # 그래프를 그리기 위한 Figure 객체 생성
# subplot : Figure 안에 들어가는 plot 하나
# 보간법 : 알려진 데이터 지점 내에서 새로운 데이터 지점을 구성하는 방식
# 최근접 보간법(Nearest Interpolation) : 새로운 지점 또는 한 지점의 값을 결정하는데 있어 주변의 가장 가까운 지점의 값을 분석하여 결정
# Green and Blue 히스토그램
subplot = figure.add_subplot(151) # 1 x 5 grid 에서 첫 번째 subplot
multi_calchist = cv2.calcHist([channels[1], channels[0]], [0, 1], None, [32, 32], [0, 256, 0, 256]) # 2D 히스토그램(Green and Blue) 계산
interpolation = subplot.imshow(multi_calchist, interpolation = "nearest") # 최근접 보간법에 대한 2D 히스토그램을 subplot에 show
subplot.set_title("Green and Blue") # subplot 의 제목 설정
plt.colorbar(interpolation) # 2D 히스토그램에 대한 colorbar 생성
# Green and Red 히스토그램
subplot = figure.add_subplot(153) # 1 x 5 grid 에서 세 번째 subplot
multi_calchist = cv2.calcHist([channels[1], channels[2]], [0, 1], None, [32, 32], [0, 256, 0, 256]) # 2D 히스토그램(Green and Red) 계산
interpolation = subplot.imshow(multi_calchist, interpolation = "nearest") # 최근접 보간법에 대한 2D 히스토그램을 subplot에 show
subplot.set_title("Green and Red") # subplot 의 제목 설정
plt.colorbar(interpolation) # 2D 히스토그램에 대한 colorbar 생성
# Blue and Red 히스토그램
subplot = figure.add_subplot(155) # 1 x 5 grid 에서 다섯 번째 subplot
multi_calchist = cv2.calcHist([channels[0], channels[2]], [0, 1], None, [32, 32], [0, 256, 0, 256]) # 2D 히스토그램(Blue and Red) 계산
interpolation = subplot.imshow(multi_calchist, interpolation = "nearest") # 최근접 보간법에 대한 2D 히스토그램을 subplot에 show
subplot.set_title("Blue and Red") # subplot 의 제목 설정
plt.colorbar(interpolation) # 2D 히스토그램에 대한 colorbar 생성

plt.show() # 생성된 모든 Figure show
cv2.waitKey(0) # 입력 무한 대기
