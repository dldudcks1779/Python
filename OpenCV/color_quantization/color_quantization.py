##### 실행 #####
# sudo python3 color_quantization.py --image 이미지 경로 --clusters 클러스터 수
# 예) sudo python3 color_quantization.py --image image.jpg --clusters 5

# 필요한 패키지 import
# sklearn : 머신러닝 라이브러리(머신러닝 알고리즘 제공)
# K-평균 클러스터링 알고리즘(K-Means Clustering Algorithm)
# - 주어진 데이터를 K개의 클러스터로 묶는 알고리즘
# - 클러스터(cluster) : 비슷한 특성을 가진 데이터 세트를 구성하는 단위
# - 각 클러스터와 거리 차이의 분산을 최소화하는 방식
# 미니배치 K-평균 클러스터링 알고리즘(Mini-Batch K-Means Clustering Algorithm)
# - 데이터를 미니배치 크기만큼 무작위로 분리하여 K-평균 클러스터링 적용
# - K-평균 클러스터링 알고리즘에 중심 위치와 모든 데이터 사이의 거리를 계산해야 하기 때문에 데이터의 갯수가 많아지면 계산량도 늘어남
# - 데이터의 수가 너무 많을 때는 미니배치 K-평균 클러스터링 알고리즘을 사용하면 계산량을 줄일 수 있음
from sklearn.cluster import MiniBatchKMeans # Mini-Batch K-Means Clustering 모듈
import numpy as np # 파이썬 행렬 수식 및 수치 계산 처리 모듈
import argparse # 명령행 파싱(인자를 입력 받고 파싱, 예외처리 등) 모듈
import cv2 # opencv 모듈

# 실행을 할 때 인자값 추가
ap = argparse.ArgumentParser()
# 입력받을 인자값 등록
ap.add_argument("-i", "--image", required=True, help="이미지 경로")
ap.add_argument("-c", "--clusters", required = True, type = int, help = "생성할 클러스터 수")
# 입력받은 인자값을 args에 저장
args = vars(ap.parse_args()) 

# input 이미지 읽기
image = cv2.imread(args["image"])

# 이미지의 높이(h)와 너비(w) 추출
(h, w) = image.shape[:2]

# 이미지를 RGB 픽셀 배열로 재구성(3 차원 배열 -> 2 차원 배열)
image = image.reshape((image.shape[0] * image.shape[1], 3))

# Mini-Batch K-Means Clustering 알고리즘 생성
# n_clusters : 클러스터 수 지정
minibatchkmeans = MiniBatchKMeans(n_clusters = args["clusters"])

# image를 Mini-Batch K-Means Clustering 알고리즘에 적용
labels = minibatchkmeans.fit_predict(image)

# 색상 정량화(Color Quantization)
# - 이미지의 고유한 색상의 수를 줄임
# cluster_centers_ : 클러스터 중심
# astype : 데이터 형 변환
quantization = minibatchkmeans.cluster_centers_.astype("uint8")[labels]

# RGB 픽셀 배열을 이미지로 재구성(2 차원 배열 -> 3 차원 배열)
image = image.reshape((h, w, 3)) # 원본 이미지
quantization = quantization.reshape((h, w, 3)) # 색상 정량화된 이미지

# 이미지 show
cv2.imshow("image", image) # 원본 이미지
cv2.imshow("quantization", quantization) # 색상 정량화된 이미지

# 입력 무한 대기
cv2.waitKey(0)
