import time

from pyqpanda import init_quantum_machine, QProg, QMachineType, X, H, single_gate_apply_to_all, directly_run, \
    quick_measure,QCloud
from modExtModule.ModExt import mod_ext
from QFTModule.QFT import qft


# shor的量子部分，最后测量出c的结果，需要连分数分解得到最后的r
def shor_quantum(base: int, N: int, times: int):
    machine = init_quantum_machine(QMachineType.CPU)
    # machine = QCloud()
    # machine.set_configure(72, 72)
    # machine.init_qvm("3041020100301306072a8648ce3d020106082a8648ce3d0301070427302502010104206f586490152171e23c73fe0d13e4455f730ebfdaf8b4f6fbf44f43936be9a6aa/32523")
    # 初始化各种比特
    quantum_start_time = int(time.time() * 1000)
    n = 0
    temp_N = N
    # 根据模数取
    while temp_N > 0:
        n = n + 1
        temp_N = temp_N >> 1
    qx = machine.qAlloc_many(n * 2)
    qy = machine.qAlloc_many(n)
    qa_add = machine.qAlloc_many(n)
    qb_add = machine.qAlloc_many(n)
    qi = machine.qAlloc_many(2)

    prog = QProg()
    prog.insert(X(qy[0]))

    ############# 测试ext使用
    # prog.insert(X(qx[1]))
    # prog.insert(X(qx[0]))
    #############
    prog.insert(single_gate_apply_to_all(H, qx))
    prog.insert(mod_ext(base, N, qx, qy, qa_add, qb_add, qi))
    prog.insert(qft(qx).dagger())

    directly_run(prog)
    # result = machine.full_amplitude_measure(prog, times)
    result = quick_measure(qx, times)
    quantum_end_time = int(time.time() * 1000)
    ############# 测试ext使用
    # directly_run(prog)
    # result2 = quick_measure(qy, times)
    # print('qy:' + str(result1))
    # print('qx:' + str(result2))
    #############
    return result
