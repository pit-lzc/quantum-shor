from .Adder import MAJ
from pyqpanda import QCircuit,CNOT


# 进位器组件

# a，b为输入，c为辅助比特，carry为保存进位项的辅助比特
# 由一个MAJ,一个CNOT门,一个逆MAJ构成，在Adder中编写的MAJ为单比特输入，这里a，b为多位
# 多个MAJ组成一起，可以判断进位情况
def MulMAJ(a, b, c):
    cicr = QCircuit()
    # 输入比特数为n
    n = len(a)
    # 首先对第一个MAJ单独插入，c为辅助比特
    cicr.insert(MAJ(a[0], b[0], c))
    # 循环插入MAJ单元
    for i in range(1, n):
        cicr.insert(MAJ(a[i], b[i], a[i - 1]))
    return cicr


def judge_carry(a, b, c, carry_in):
    cicr = QCircuit()
    n = len(a)
    cicr.insert(MulMAJ(a, b, c))
    cicr.insert(CNOT(a[n - 1], carry_in))
    cicr.insert(MulMAJ(a, b, c).dagger())
    return cicr
