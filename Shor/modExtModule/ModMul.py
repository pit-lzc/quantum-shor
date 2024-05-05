from pyqpanda import QCircuit, CNOT
from .ModAdd import mod_add


# C: 模指线路传过来的常数。2^0~~2^(2n-1)
# N: 模数
# qy: 量子比特y，模加模块的控制比特，并保存结果，传递给后续模乘线路使用
# qa_add: mod_add里的qa，用于绑定常数x的一组比特，加法辅助比特
# qb_add: mod_add里的qb，最终保存加法结果的比特，乘法辅助比特
# qi: 加法辅助比特，两个
def mod_mul(C, N, qy, qa_add, qb_add, qi):
    cicr = QCircuit()
    n = len(qy)
    # 这里实现了(y,0) --> (y,CymodN)
    for i in range(0, n):
        mul_cicr = QCircuit()
        const_num = C * pow(2, i) % N
        mul_cicr.insert(mod_add(const_num, N, qa_add, qb_add, qi))
        mul_cicr = mul_cicr.control(qy[i])
        cicr.insert(mul_cicr)

    # 做swap操作，此时qb_add保存了加法后的结果，交换到qy, (y,0) --> (CymodN,y)
    for i in range(0, n):
        cicr.insert(CNOT(qy[i], qb_add[i]))
        cicr.insert(CNOT(qb_add[i], qy[i]))
        cicr.insert(CNOT(qy[i], qb_add[i]))

    Crev = mod_reverse(C, N)
    tmp2_circ = QCircuit()
    for i in range(0, n):
        tmp = Crev * pow(2, i)
        tmp = tmp % N
        tmp_circ = QCircuit()
        tmp_circ.insert(mod_add(tmp, N, qa_add, qb_add, qi))
        tmp_circ = tmp_circ.control(qy[i])
        tmp2_circ.insert(tmp_circ)
    cicr.insert(tmp2_circ.dagger())
    # 需要把qb_add从y还原为0
    return cicr


def mod_reverse(c, m):
    if c == 1:
        return 1
    m1 = m
    quotient = []
    quo = m // c
    remainder = m % c
    quotient.append(quo)
    while (remainder != 1):
        m = c
        c = remainder
        quo = m // c
        remainder = m % c
        quotient.append(quo)
    if (len(quotient) == 1):
        return m - quo
    if (len(quotient) == 2):
        return 1 + quotient[0] * quotient[1]
    rev1 = 1
    rev2 = quotient[-1]
    reverse_list = quotient[0:-1]
    reverse_list.reverse()
    for i in reverse_list:
        rev1 = rev1 + rev2 * i
        temp = rev1
        rev1 = rev2
        rev2 = temp
    if (len(quotient) % 2) == 0:
        return rev2
    return m1 - rev2
