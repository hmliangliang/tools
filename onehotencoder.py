# -*-coding: utf-8 -*-
# @Time    : 2024/11/26 21:50
# @File    : onehotencoder.py
# @Software: PyCharm
import datetime

import pandas as pd
import argparse
import os

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_output', help='Output file path', type=str, default='')
    parser.add_argument('--data_input', help='map_feature_file', type=str, default='')
    parser.add_argument('--start_col', help='开始one-hot的列号(从0开始)', type=int, default=0)
    parser.add_argument('--end_col', help='终止one-hot的列号(从0开始)', type=int, default=10)
    parser.add_argument("--tb_log_dir", help="日志位置", type=str, default='')
    args = parser.parse_args()
    # 读取数据
    path = args.data_input.split(',')[0]
    input_files = sorted([file for file in os.listdir(path) if file.find("part-") != -1])
    count = 0
    for file in input_files:
        count += 1
        print("一共{}个文件,当前正在处理第{}个训练文件,文件路径:{}......".format(
            len(input_files), count, os.path.join(path, file)))
        data_temp = pd.read_csv(os.path.join(path, file), sep=';', header=None).astype(str)
        if count == 1:
            data = data_temp
        else:
            data = pd.concat([data, data_temp], axis=0)
    n, _ = data.shape
    columns_to_encode = data.columns[args.start_col:args.end_col]

    # 对每一列进行 One-Hot 编码并替换原有值
    for col in columns_to_encode:
        # 进行 One-Hot 编码
        one_hot = pd.get_dummies(data[col], prefix=col)

        # 拼接 One-Hot 编码结果
        data[col] = one_hot.astype(str).agg(';'.join, axis=1)
    output_file = os.path.join(args.data_output, 'output_{}.csv'.format(count))
    data.to_csv(output_file, index=False, header=False, sep=',')
    print("第{}个文件写入完成，共写入{}行  {}".format(count, n, datetime.datetime.now()))
