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
# cicr_cost: 构造线路cost
# run_cost: 运行cost
# measure_cost: 测量cost
# total_cost: 总cost，包括量子＋经典
def get_excel_costTime_Shor(times: int, cicr_cost, run_cost, measure_cost, total_cost):
    path = 'C://Users//lizichen//Desktop//graduate_data//cost_time//Shor_cost_n=15.xlsx'
    df = pd.read_excel(path)
    # 检查是否有当前行
    mask = df['times'] == times
    if mask.any():
        # 假设你有类似的操作
        old_cicr_cost = df[mask]['cicr_cost(ms)'].values[0]
        old_run_cost = df[mask]['run_cost(ms)'].values[0]
        old_measure_cost = df[mask]['measure_cost(ms)'].values[0]
        old_total_cost = df[mask]['total_cost(ms)'].values[0]
        # 对每个参数进行处理
        cicr_cost = (old_cicr_cost + cicr_cost) / 2
        run_cost = (old_run_cost + run_cost) / 2
        measure_cost = (old_measure_cost + measure_cost) / 2
        total_cost = (old_total_cost + total_cost) / 2
        # 更新DataFrame中对应的值
        df.loc[mask, 'cicr_cost(ms)'] = cicr_cost
        df.loc[mask, 'run_cost(ms)'] = run_cost
        df.loc[mask, 'measure_cost(ms)'] = measure_cost
        df.loc[mask, 'total_cost(ms)'] = total_cost
    else:
        new_data = pd.DataFrame({'times': times,
                                 'cicr_cost(ms)': [cicr_cost],
                                 'run_cost(ms)': [run_cost],
                                 'measure_cost(ms)': [measure_cost],
                                 'total_cost(ms)': [total_cost]})
        df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel(path, index=False)
