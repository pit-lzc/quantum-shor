import argparse
import math
import Shor
import pyqpanda as pq
from pyqpanda import *
from modExtModule.Transform import transform_data
from modExtModule.ModAdd import mod_add
from modExtModule.ModMul import mod_mul
from Shor_quantum import shor_quantum
from QFTModule.QFT import qft
from classicalModule.get_r import get_r
from utilModule.DataExecuteUtil import get_excel_value_times
from pyqpanda import Shor_factorization

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument('times', type=str, help='An integer for the accumulator')
    args = parser.parse_args()
    times = int(args.times)
    # for i in range(1, 10):
    #     times = 1000000
    #     while times < 100000000:
    # times = 1000
    Shor.shor(15, times)
    # times *= 2
    # print(math.gcd(170, 21))
    #
    # 1.测试modAdd
    # machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    # prog = pq.QProg()
    # qa = machine.qAlloc_many(4)
    # qb = machine.qAlloc_many(4)
    # # 模加需要的辅助比特
    # qs3 = machine.qAlloc_many(2)
    # prog.insert(transform_data(qb, 0))
    # # 构建量子程序
    # prog.insert(mod_add(1, 13, qa, qb, qs3))
    # directly_run(prog)
    # result = quick_measure(qa, 100)
    # print(result)
    # result = quick_measure(qb, 100)
    # print(result)
    # result = quick_measure(qs3, 100)
    # print(result)
    #
    #
    # my_dict: Dict[str, int] = {'00000000': 2594, '01000000': 2471, '10000000': 2485, '11000000': 2450}
    # print(get_r(my_dict, 15, 10))

    # 3.测试模乘
    # machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    # prog = QProg()
    # qy = machine.qAlloc_many(4)
    # qa = machine.qAlloc_many(4)
    # qb = machine.qAlloc_many(4)
    # # 模加需要的辅助比特
    # qs3 = machine.qAlloc_many(2)
    # # prog.insert(X(qy[0]))
    # prog.insert(X(qy[3]))
    # prog.insert(mod_mul(1, 13, qy, qa, qb, qs3))
    # directly_run(prog)
    # result = quick_measure(qy, 100)
    # print(result)
    # result = quick_measure(qa, 100)
    # print(result)
    # result = quick_measure(qb, 100)
    # print(result)
    # result = quick_measure(qs3, 100)
    # print(result)

    # 4. 测试模指
    # shor_quantum(5,13,100)

    # 5. 测试QFT
    # machine = pq.init_quantum_machine(pq.QMachineType.CPU)
    # prog = QProg()
    # q = machine.qAlloc_many(4)
    # prog.insert(qft(q))
    # directly_run(prog)
    # result = quick_measure(q, 10000)
    # print(result)

