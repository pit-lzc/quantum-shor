from pyqpanda import QCircuit,X
from .Adder import adder
from .CarryIn import judge_carry
from .Transform import transform_data


# x:待加常数
# N:模数
# qa:用于绑定常数x的一组比特
# qb:绑定初始输入y的一组比特，并保存结果，可以传递给下一个模加模块使用
# qi:两个辅助比特，qi[0]表示进位器辅助比特carry，qi[1]表示MAJ辅助比特c
def mod_add(x, N, qa, qb, qi):
    cicr = QCircuit()
    n = len(qa)
    # 处理x，变为 2^n + x- N,用于进位器判断和加法器模块
    handled_value = (1 << n) + x - N
    # 首先经过进位器线路，会对qi[0]造成影响，若进位qi[0]为变为1
    cicr.insert(transform_data(qa, handled_value))
    cicr.insert(judge_carry(qa, qb, qi[1], qi[0]))
    # 再次绑定的目的是为了将所有位重新置0，不然后面绑定会受影响
    cicr.insert(transform_data(qa, handled_value))

    # 下面构造成功进位时使用的加法器，此时令qa=2^n+x-N，进位后2^n溢出，变为x+y-N
    add_cicr_carryIn = QCircuit()
    add_cicr_carryIn.insert(transform_data(qa, handled_value))
    add_cicr_carryIn.insert(adder(qa, qb, qi[1]))
    add_cicr_carryIn.insert(transform_data(qa, handled_value))
    add_cicr_carryIn = add_cicr_carryIn.control(qi[0])
    cicr.insert(add_cicr_carryIn)

    # 对进位器辅助比特carry取反，作为未成功进位时的加法器的控制比特
    cicr.insert(X(qi[0]))

    # 未成功进位时使用的加法器
    add_cicr_notCarryIn = QCircuit()
    # # 重新为qa赋值，值为x
    add_cicr_notCarryIn.insert(transform_data(qa, x))
    add_cicr_notCarryIn.insert(adder(qa, qb, qi[1]))
    add_cicr_notCarryIn.insert(transform_data(qa, x))
    add_cicr_notCarryIn = add_cicr_notCarryIn.control(qi[0])
    cicr.insert(add_cicr_notCarryIn)

    # 若进位成功，此时控制比特为0，进位失败则为1，之后考虑一段线路，使进位失败时的控制比特恢复为0，进位成功时控制比特不受影响
    # 进位成功后的 qb = x+y-N，0<=y<=N，因此y<N，y-N<0，qb < x --- qb - x < 0
    # 进位失败后的 qb = x+y，0<=y<=N，qb > x --- qb - x > 0
    # 因此类比上面，以 qb+2^n-x 作为区分，再次通过进位器。
    handled_value_2 = (1 << n) - x
    cicr.insert(transform_data(qa, handled_value_2))
    cicr.insert(judge_carry(qa, qb, qi[1], qi[0]))
    cicr.insert(transform_data(qa, handled_value_2))
    return cicr
