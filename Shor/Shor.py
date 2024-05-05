import time

from Shor_quantum import shor_quantum
from classicalModule.get_r import get_r
from classicalModule.math_util import is_prime
from math import gcd
from utilModule.DataExecuteUtil import get_excel_value_times, get_excel_costTime_Shor
import random

SHOR_QUANTUM_TIMES = 1000000


def shor(N: int, times: int):
    start_time = int(time.time() * 1000)
    has_tried = set()
    if N % 2 == 0:
        print('SPECIAL CASE')
        return {2, N / 2}
    if is_prime(N):
        print('N can not be prime')
        return -1
    while True:
        print('----------start----------')
        a = random.randint(2, N - 1)
        if a in has_tried:
            print('FAIL: ' + str(a) + ' has been tried')
            continue
        a = 2
        print('try:a =', a)
        has_tried.add(a)
        if gcd(a, N) != 1:
            print('FAIL: gcd(a, N) != 1,retry')
            continue
        c, cicr_cost, run_cost, measure_cost = shor_quantum(a, N, times)
        print('c:', c)
        r = get_r(c, N, times)
        print('r:', r)
        if r % 2 == 1:
            print('FAIL: r是奇数,retry')
            continue
        b = pow(a, r // 2, N)
        if b == N - 1:
            print('FAIL: a^(r/2) + 1 == 0modN')
            continue
        A = int(gcd(b - 1, N))
        B = int(N / A)
        if A == 1 or A == N:
            print('FAIL: A == 1 or A == N，retry')
            continue
        result = {A, B}
        end_time = int(time.time() * 1000)
        total_cost = end_time - start_time
        # 生成对应量子结果
        # get_excel_value_times(c, a, N)
        # 生成Shor不同次数消耗时间
        print("total cost: " + str(total_cost))
        print("result: " + str(result))
        print('----------SUCCESS----------')
        get_excel_costTime_Shor(times, cicr_cost, run_cost, measure_cost, total_cost)
        return result
