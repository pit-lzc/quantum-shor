from pyqpanda import QCircuit
from .ModMul import mod_mul


# base: 指数基底a
# N: 模数N
# qx: 输入x，一组控制比特
# qy: 低位比特，最终实现 (x,y) -> (x,a^x mod N)，保存一系列模加后的模乘值和最终的模指值
# qa_add: 模加中的辅助比特，用于绑定数值，对应qa
# qb_add: 模乘中的辅助比特，用于模加保存值，最后将值swap给qy
# qi: 模加辅助比特
def mod_ext(base, N, qx, qy, qa_add, qb_add, qi):
    cicr = QCircuit()
    n = len(qx)
    for i in range(0, n):
        const_num = pow(base, pow(2, i)) % N
        cicr.insert(mod_mul(const_num, N, qy, qa_add, qb_add, qi).control(qx[i]))
    return cicr
