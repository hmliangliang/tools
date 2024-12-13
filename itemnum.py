# -*-coding: utf-8 -*-
# @Time    : 2024/9/6 10:31
# @File    : itemnum.py
# @Software: PyCharm

# 统计序列中各个元素的数目

import datetime
import os
import argparse
import time

import numpy as np
import pandas as pd

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_output', help='Output file path', type=str, default='')
    parser.add_argument('--data_input', help='map_feature_file', type=str, default='')
    parser.add_argument('--item_num', help='item的最大数量', type=int, default=74)
    parser.add_argument("--tb_log_dir", help="日志位置", type=str, default='')
    args = parser.parse_args()
    # 读取数据
    path = args.data_input.split(',')[0]
    input_files = sorted([file for file in os.listdir(path) if file.find("part-") != -1])
    n_files = len(input_files)
    count = 0
    for file in input_files:
        count += 1
        print("一共{}个文件,当前正在处理第{}个文件,文件路径:{}......".format(n_files, count,
                                                                             "cfs://" + path + "/" + file))
        # 读取数据数据最后一列为序列数据
        data = pd.read_csv(os.path.join(path, file), sep=';', header=None).astype(object)
        n, m = data.shape
        result = np.zeros((n, args.item_num))
        for i in range(n):
            item_list = str(data.iloc[i, -1]).split(",")
            if len(item_list) > 0:
                for item in item_list:
                    try:
                        index = int(item)  # 尝试将 item 转换为整数
                        if 0 <= index < args.item_num:  # 检查 index 是否在有效范围内
                            result[i, index - 1] += 1  # 增加计数
                        else:
                            print("{} 超出范围!".format(item))  # 如果 index 超出范围
                    except ValueError:
                        print("{} 转换整数失败!".format(item))  # 捕获转换失败的情况
        data = pd.concat([data, pd.DataFrame(result)], axis=1)
        # 写入数据
        starttime = time.time()
        data.to_csv(os.path.join(args.data_output, 'output_{}.csv'.format(count)), index=False, header=False, sep=';')
        endtime = time.time()
        print("第{}个文件写入完成，耗时:{} {}".format(count, endtime - starttime, datetime.datetime.now()))
