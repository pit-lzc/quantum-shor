import math
from pyqpanda import QCircuit, H, CNOT, CR


def qft(qlist):
    circ = QCircuit()
    n = len(qlist)
    for i in range(0, n):
        # 每个量子比特的处理首先插入一个H门
        circ.insert(H(qlist[n - 1 - i]))
        for j in range(i + 1, n):
            # 循环插入CR门
            circ.insert(CR(qlist[n - 1 - j], qlist[n - 1 - i], math.pi / (1 << (j - i))))
    # 最后交换高低态
    for i in range(0, n // 2):
        circ.insert(CNOT(qlist[i], qlist[n - 1 - i]))
        circ.insert(CNOT(qlist[n - 1 - i], qlist[i]))
        circ.insert(CNOT(qlist[i], qlist[n - 1 - i]))
    return circ
