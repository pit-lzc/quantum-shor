import argparse
import subprocess

if __name__ == "__main__":
    times = 100000
    # 构建命令行参数
    main_path = 'E:/graduate-design/Shor/main.py'  # 替换为 main.py 的实际路径
    while times < 1100000000:
        for i in range(1, 50):
            command = 'python ' + main_path + ' ' + str(times)
            # command = ['python', main_path, 'times', str(times)]
            # 打印当前运行的命令
            print(f"Running command: {''.join(command)}")
            # 使用 subprocess 运行命令
            subprocess.run(command)
        times *= 2

