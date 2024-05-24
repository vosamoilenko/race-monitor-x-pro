import redis
import time

redis_host = 'localhost'
redis_port = 6379
r = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)

def check_if_paused():
    # This function checks if the GPS collection should be paused
    return r.get('pause_gps') is not None and r.get('pause_gps') == 'true'

while True:
    print(check_if_paused())
    time.sleep(2)
