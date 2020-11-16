import os # 운영체제 기능 모듈

# 파일 이름 변경 함수
def change_file_name(path, name, form):
    count = 1 # 이름 마지막에 넣을 숫자
    for filename in os.listdir(path): # path 안에 있는 파일들을 list로 읽어 한 번씩 반복
        if filename[-4:] == str(form): # 변경할 파일들의 형식이 같을 경우
            print('파일 변경 전 :', path + filename, ' =====> ', '파일 변경 후 :', path + str(name) + str(count) + str(form))
            os.rename(path + filename, path + str(name) + str(count) + str(form)) # os.rename 메소드로 파일 이름 변경
            count += 1 # 숫자 증가

# 함수 실행('파일 경로', '새로 변경할 파일 이름', '파일 형식(.txt, .jpg, .png 등)')
change_file_name('./image_path/', 'test', '.jpg')
