import time

start = time.time()
old = 0

while True:
    time.sleep(1)
    elapsed = time.time() - start
    millis = elapsed * 1000
    dt = millis - old
    old = millis
    print(millis,dt)