from pyqpanda import Dict
from .math_util import lcm
import fractions


# qb_k是一个 Dict[str, int] 类型：{'00': 100}，key表示测量结果，value表示次数
def get_r(qb_k: Dict[str, int], N: int, times: int):
    # 这里实际是做连分数分解，拿到最终的分母，可以认为是 r 或者 r 的约数
    final_r = 0
    s = set()
    for key in qb_k.keys():
        if int(key, 2) == 0:
            continue
        # 筛选出出现次数过少的错误数据
        if qb_k.get(key) < times / (len(qb_k) + 1):
            continue
        n = len(key)
        c = int(key, 2)
        if c == 0:
            continue
        q = 1 << n
        # 这里拿到在一定范围内距离最近的分数
        fen_shu = fractions.Fraction(c, q).limit_denominator(N)
        # print(fen_shu)
        r = fen_shu.denominator
        s.add(r)
    # 遍历所有分母，拿到最小公倍数
    for r in s:
        if final_r == 0:
            final_r = r
            continue
        if final_r != r:
            final_r = lcm(final_r, r)
    return final_r
