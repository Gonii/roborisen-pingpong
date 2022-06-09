import sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 폴더 경로 가져오기

from pingpongthread import PingPongThread
import keyboard # keyboard==0.13.4
import time

# ARDUINO PIN: 1번 갈색, 2번 빨간색, 3번 주황색, 4번 없음.

PingPongThreadInstance = PingPongThread(number=1) # n개 로봇 연결
PingPongThreadInstance.start() # 쓰레드 시작
PingPongThreadInstance.wait_until_full_connect() # 전부 연결될 때까지 기다림

cube_ID = 1 # 큐브 번호
servo_schedule = [[180, 0, 90, 180]] # 속도 스케줄
servo_duration = 1 # 회전 스케줄

while not keyboard.is_pressed("q"): # q가 눌리기 전까지 쓰레드 유지
    while PingPongThreadInstance.play_once_full_connect(): # 연결 되어있는 동안, 한 번만 실행
        ### single
        PingPongThreadInstance.run_single_servo(cube_ID, 0) # 모터 돌림 (스케줄 모드)
        time.sleep(1)
        PingPongThreadInstance.run_single_servo(cube_ID, 180) # 모터 돌림 (스케줄 모드)
        time.sleep(3)
        ### schedule
        PingPongThreadInstance.run_servo_schedule(cube_ID, servo_schedule, servo_duration)
        print(PingPongThreadInstance.get_robot_status()) # 상태 확인

PingPongThreadInstance.run_motor("all", "stop") # 모터 끔
PingPongThreadInstance.end() # 쓰레드 종료