import time

from sympy import factorint

if __name__ == "__main__":
    start_time = int(time.time() * 1000)
    for i in range(1, 1000000):
        factorint(15)
    end_time = int(time.time() * 1000)
    print(end_time - start_time)
