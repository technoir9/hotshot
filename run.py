from utils import schedule
import time

if __name__ == '__main__':
    schedule.init_scheduler()
    while True:
        time.sleep(1)
