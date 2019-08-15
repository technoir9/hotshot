from utils import schedule
import time

if __name__ == '__main__':
    schedule.init_scheduler()
    for x in range(0, 20 * 60):
        time.sleep(1)
