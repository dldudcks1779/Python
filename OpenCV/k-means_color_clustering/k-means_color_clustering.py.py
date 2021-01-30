##### 실행 #####
# sudo python3 k-means_color_clustering.py --image 이미지 경로
# 예) sudo python3 k-means_color_clustering.py --image test1.jpg --clusters 3

# 필요한 패키지 import
# sklearn : 머신러닝 라이브러리(머신러닝 알고리즘 제공)
# K-평균 클러스터링 알고리즘(K-Means Clustering Algorithm)
# - 주어진 데이터를 K개의 클러스터로 묶는 알고리즘
# - 클러스터(cluster) : 비슷한 특성을 가진 데이터 세트를 구성하는 단위
# - 각 클러스터와 거리 차이의 분산을 최소화하는 방식
from sklearn.cluster import KMeans # K-Means Clustering 모듈
import matplotlib.pyplot as plt # 데이터를 차트나 그래프로 시각화할 수 있는 라이브러리
import numpy as np # 파이썬 행렬 수식 및 수치 계산 처리 모듈
import argparse # 명령행 파싱(인자를 입력 받고 파싱, 예외처리 등) 모듈
import cv2 # opencv 모듈

# 각 클러스터에 속한 픽셀 수를 계산한 히스토그램
def create_histogram(kmeans):
    # np.arange : numpy 배열 생성
    # np.unique : numpy 배열에서 고유 값을 검색하고 정렬
    cluster_number = np.arange(0, len(np.unique(kmeans.labels_)) + 1) # 클러스터 수 추출(도수 분포 구간)
    
    # np.histogram(도수분포의 각 구간에 있는 data 수, 도수분포 구간) : 도수 분포로부터 histogram 생성
    # 도수 분포 : 특정 구간에 속하는 자료의 분포
    (histogram, bins) = np.histogram(kmeans.labels_, bins = cluster_number) # 각 클러스터에 할당된 픽셀 수를 기준으로 히스토그램 생성

    # 히스토그램의 합이 1이 되도록 정규화
    histogram = histogram.astype("float") # astype : 데이터 형 변환
    histogram /= histogram.sum() # sum : 모든 요소의 합

    # 히스토그램 반환
    return histogram

# 각 클러스터에 할당된 픽셀 수를 나타내는 colorbar 생성
        
def plot_colorbar(histogram, centroids):
    # colorbar 초기화(80 x 500의 직사각형)
    # np.zeros : 모든 요소를 0으로 초기화된 numpy 배열 생성
    colorbar = np.zeros((80, 500, 3), dtype = "uint8")
    startX = 0 # colorbar가 시작되는 지점

    # 각 cluster의 백분율과 색상 길이만큼 반복
    # zip : 같은 길이의 리스트를 같은 인덱스끼리 잘라서 리스트로 반환
    for (percentage, color) in zip(histogram, centroids):
        # 현재 색상의 이미지에 비율만큼 colorbar에 채움
        endX = startX + (percentage * 500) # colorbar 가 종료되는 지점
        # tolist : 배열로 변환
        cv2.rectangle(colorbar, (int(startX), 0), (int(endX), 80), color.astype("uint8").tolist(), -1) # 사각형 그리기(colorbar 에 색상을 채움)
        startX = endX # 다음 색상을 이어 그리기위해 종료되는 지점을 시작되는 지점으로 변경

    # colorbar 반환
    return colorbar

# 실행을 할 때 인자값 추가
ap = argparse.ArgumentParser()
# 입력받을 인자값 등록
ap.add_argument("-i", "--image", required=True, help="image 이미지 경로")
ap.add_argument("-c", "--clusters", required = True, type = int, help = "생성할 클러스터 수")
# 입력받은 인자값을 args에 저장
args = vars(ap.parse_args()) 

# input 이미지 읽기
image = cv2.imread(args["image"])

# 이미지 RGB 변환(OpenCV에서 BGR로 저장 -> matplotlib에서 RGB로 저장)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.figure("image") # Figure 객체 생성
plt.axis("off") # axis : x 축의 범위 지정("off" : x 축과 레이블을 사용하지 않음)
plt.imshow(image) # Figure 객체에 image 그리기

# 이미지를 RGB 픽셀 배열로 재구성(3 차원 배열 -> 2 차원 배열)
image = image.reshape((image.shape[0] * image.shape[1], 3))

# K-Means Clustering 알고리즘 생성
# n_clusters : 클러스터 수 지정
kmeans = KMeans(n_clusters = args["clusters"]) 

# image를 K-Means Clustering 알고리즘에 적용
kmeans.fit(image)

# K-Means Color Clustering 히스토그램 생성
histogram = create_histogram(kmeans)

# K-Means Color Clustering 히스토그램에 대한 colorbar(각 레이블(색상)에 대한 픽셀 수) 생성
# cluster_centers_ : 클러스터 중심
colorbar = plot_colorbar(histogram, kmeans.cluster_centers_)

plt.figure("colorbar") # Figure 객체 생성
plt.axis("off") # axis : x 축의 범위 지정("off" : x 축과 레이블을 사용하지 않음)
plt.imshow(colorbar) # Figure 객체에 colorbar 그리기

# 생성된 모든 Figure show
plt.show()
