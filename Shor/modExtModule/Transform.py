from pyqpanda import *


def transform_data(qbit, data):
    cicr = QCircuit()
    index = 0
    while data >= 1:
        if data % 2 == 1:
            cicr.insert(X(qbit[index]))
        data >>= 1
        index = index + 1
    return cicr
