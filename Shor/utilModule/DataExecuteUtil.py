from pyqpanda import Dict
import pandas as pd
from datetime import datetime


# 生成是值、次数对应的excel文件
# a: 指数基底，用于excel文件列
# N: 待分解数，用于excel文件列
# qb_k: 对应量子计算的结果
def get_excel_value_times(qb_k: Dict[str, int], a: int, N: int):
    data = []
    for value_binary, appear_times in qb_k.items():
        value = int(value_binary, 2)
        data.append({'value_binary': value_binary, 'value': value, 'appear_times': appear_times})

    # 创建 DataFrame
    dateFrame = pd.DataFrame(data)

    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    # 构造文件名
    filename = f'output_{current_time}_a={a}_N={N}.xlsx'
    # 写入 Excel 文件
    path = 'C://Users//lizichen//Desktop//graduate_data//' + filename
    dateFrame.to_excel(path, index=False)
    print('excel文件:' + path + '已生成')


# 生成Shor算法对应次数消耗时间的excel文件
def get_excel_costTime_Shor(startTime, endTime, times: int):
    date = []
    path = 'C://Users//lizichen//Desktop//graduate_data//cost_time//Shor_cost_n=15.xlsx'
    df = pd.read_excel(path)
    # 检查是否有当前行
    mask = df['times'] == times
    cost_time = endTime - startTime
    print('cost_time: ' + str(cost_time) + 'times: ' + str(times))
    if mask.any():
        old_value = df[mask]['cost_time(ms)'].values[0]
        new_value = endTime - startTime
        mean_value = (old_value + new_value) / 2
        df.loc[mask, 'cost_time(ms)'] = mean_value
    else:
        new_data = pd.DataFrame({'times': times, 'cost_time(ms)': [endTime - startTime]})
        df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(path, index=False)
