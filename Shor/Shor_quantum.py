import time

from pyqpanda import init_quantum_machine, QProg, QMachineType, X, H, single_gate_apply_to_all, directly_run, \
    quick_measure, QCloud
from modExtModule.ModExt import mod_ext
from QFTModule.QFT import qft


# shor的量子部分，最后测量出c的结果，需要连分数分解得到最后的r
def shor_quantum(base: int, N: int, times: int):
    machine = init_quantum_machine(QMachineType.CPU)
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
    prog.insert(single_gate_apply_to_all(H, qx))
    prog.insert(mod_ext(base, N, qx, qy, qa_add, qb_add, qi))
    prog.insert(qft(qx).dagger())

    quantum_execute_time = int(time.time() * 1000)
    print("execute quantum circle cost:", str(quantum_execute_time - quantum_start_time))

    directly_run(prog)
    quantum_run_end_time = int(time.time() * 1000)
    print("run quantum circle cost:", str(quantum_run_end_time - quantum_execute_time))

    result = quick_measure(qx, times)
    quantum_end_time = int(time.time() * 1000)
    print("measure quantum result cost:", str(quantum_end_time - quantum_run_end_time))

    return (result,
            quantum_execute_time - quantum_start_time,
            quantum_run_end_time - quantum_execute_time,
            quantum_end_time - quantum_run_end_time)
