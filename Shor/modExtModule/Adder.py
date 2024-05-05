from pyqpanda import QCircuit, CNOT, Toffoli


# 加法器组件

# 所有组件都以从下到上a，b，c顺序输入
# MAJ由两个Cnot门和一个Toffoli门构成，用于求进位
# c表示辅助比特
def MAJ(a, b, c):
    cicr = QCircuit()
    cicr.insert(CNOT(a, c))
    cicr.insert(CNOT(a, b))
    cicr.insert(Toffoli(b, c, a))
    return cicr


# UMA由一个Toffoli门和两个Cnot门构成，用于恢复状态和求和
# a,b,c与MAJ一一对应
def UMA(a, b, c):
    cicr = QCircuit()
    cicr.insert(Toffoli(b, c, a))
    cicr.insert(CNOT(a, c))
    cicr.insert(CNOT(c, b))
    return cicr


# c为辅助比特,用于第一个MAJ单元和最后一个UMA单元的进位
# b最后保存和，a经过MAJ后保存进位，最后保持不变
def adder(a, b, c):
    cicr = QCircuit()
    # 输入比特数为n
    n = len(a)
    # 首先对第一个MAJ单独插入，c为辅助比特
    cicr.insert(MAJ(a[0], b[0], c))
    # 循环插入MAJ单元
    for i in range(1, n):
        cicr.insert(MAJ(a[i], b[i], a[i - 1]))

    # 循环插入UMA单元
    for i in range(n - 1, 0, -1):
        cicr.insert(UMA(a[i], b[i], a[i - 1]))
    # 最后一个UMA单元，需要用到c辅助比特
    cicr.insert(UMA(a[0], b[0], c))
    return cicr
