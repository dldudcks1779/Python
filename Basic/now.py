import datetime # 날짜 및 시간 기능을 제공하는 모듈

today = datetime.date.today() # 날짜 정보
now = datetime.datetime.now() # 날짜 및 시간 정보

print("today :", today)
# today : 2021-01-22

print("now :", now)
# now : 2021-01-22 15:31:21.155027

print("연 월 요일 : ", today.strftime('%Y %B %A'))
# 연 월 요일 :  2021 January Friday

print("연 월 요일(단축 표기) : ", today.strftime('%Y %b %a'))
# 연 월 요일(단축 표기) :  2021 Jan Fri

print("연중 몇 번째 일 :", today.strftime('%j'))
# 연중 몇 번째 일 : 022

print("연중 몇 번째 주(일요일 기준) :", today.strftime('%U'))
# 연중 몇 번째 주(일요일 기준) : 03

print("연중 몇 번째 주(월요일 기준) :", today.strftime('%W'))
# 연중 몇 번째 주(월요일 기준) : 03

print("현재 시간 :", now.strftime('%Y-%m-%d %H:%M:%S'))
# 현재 시간 : 2021-01-22 15:33:13
